"""Models.

Changes affecting results or their presentation should also update
parameters.py `change_date`, so users can see when results have last
changed
"""

from __future__ import annotations

from typing import Dict, Generator, Tuple

import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import streamlit as st
from penn_chime.parameters import Parameters
from statsmodels.tsa.api import SimpleExpSmoothing, Holt
import os
import datetime
from seirsplus.models import *
import networkx


class SimSirModel:

    def __init__(self, p: Parameters) -> SimSirModel:
        # TODO missing initial recovered value
        susceptible = p.susceptible
        recovered = 0.0
        recovery_days = p.recovery_days

        rates = {
            key: d.rate
            for key, d in p.dispositions.items()
        }

        lengths_of_stay = {
            key: d.length_of_stay
            for key, d in p.dispositions.items()
        }

        # Note: this should not be an integer.
        # We're appoximating infected from what we do know.
        # TODO market_share > 0, hosp_rate > 0
        infected = (
                p.current_hospitalized / p.market_share / p.hospitalized.rate
        )

        detection_probability = (
            p.known_infected / infected if infected > 1.0e-7 else None
        )

        intrinsic_growth_rate = \
            (2.0 ** (1.0 / p.doubling_time) - 1.0) if p.doubling_time > 0.0 else 0.0

        gamma = 1.0 / recovery_days

        # Contact rate, beta
        beta = (
                (intrinsic_growth_rate + gamma)
                / susceptible
                * (1.0 - p.relative_contact_rate)
        )  # {rate based on doubling time} / {initial susceptible}

        # r_t is r_0 after distancing
        r_t = beta / gamma * susceptible

        # Simplify equation to avoid division by zero:
        # self.r_naught = r_t / (1.0 - relative_contact_rate)
        r_naught = (intrinsic_growth_rate + gamma) / gamma
        doubling_time_t = 1.0 / np.log2(
            beta * p.susceptible - gamma + 1)

        raw_df = sim_sir_df(
            p.susceptible,
            infected,
            recovered,
            beta,
            gamma,
            p.n_days,
        )
        dispositions_df = build_dispositions_df(raw_df, rates, p.market_share)
        admits_df = build_admits_df(dispositions_df)
        census_df = build_census_df(admits_df, lengths_of_stay)

        self.susceptible = susceptible
        self.infected = infected
        self.recovered = recovered

        self.detection_probability = detection_probability
        self.recovered = recovered
        self.intrinsic_growth_rate = intrinsic_growth_rate
        self.gamma = gamma
        self.beta = beta
        self.r_t = r_t
        self.r_naught = r_naught
        self.doubling_time_t = doubling_time_t
        self.raw_df = raw_df
        self.dispositions_df = dispositions_df
        self.admits_df = admits_df
        self.census_df = census_df


def sir(
        s: float, i: float, r: float, beta: float, gamma: float, n: float
) -> Tuple[float, float, float]:
    """The SIR model, one time step."""
    s_n = (-beta * s * i) + s
    i_n = (beta * s * i - gamma * i) + i
    r_n = gamma * i + r
    if s_n < 0.0:
        s_n = 0.0
    if i_n < 0.0:
        i_n = 0.0
    if r_n < 0.0:
        r_n = 0.0

    scale = n / (s_n + i_n + r_n)
    return s_n * scale, i_n * scale, r_n * scale


def gen_sir(
        s: float, i: float, r: float, beta: float, gamma: float, n_days: int
) -> Generator[Tuple[float, float, float], None, None]:
    """Simulate SIR model forward in time yielding tuples."""
    s, i, r = (float(v) for v in (s, i, r))
    n = s + i + r
    for d in range(n_days + 1):
        yield d, s, i, r
        s, i, r = sir(s, i, r, beta, gamma, n)


def sim_sir_df(
        s: float, i: float, r: float, beta: float, gamma: float, n_days: int
) -> pd.DataFrame:
    """Simulate the SIR model forward in time."""
    return pd.DataFrame(
        data=gen_sir(s, i, r, beta, gamma, n_days),
        columns=("day", "susceptible", "infected", "recovered"),
    )


def build_dispositions_df(
        sim_sir_df: pd.DataFrame,
        rates: Dict[str, float],
        market_share: float,
) -> pd.DataFrame:
    """Get dispositions of patients adjusted by rate and market_share."""
    patients = sim_sir_df.infected + sim_sir_df.recovered
    return pd.DataFrame({
        "day": sim_sir_df.day,
        **{
            key: patients * rate * market_share
            for key, rate in rates.items()
        }
    })


def build_admits_df(dispositions_df: pd.DataFrame) -> pd.DataFrame:
    """Build admits dataframe from dispositions."""
    admits_df = dispositions_df.iloc[:-1, :] - dispositions_df.shift(1)
    admits_df.day = dispositions_df.day
    return admits_df


def build_census_df(
        admits_df: pd.DataFrame,
        lengths_of_stay: Dict[str, int],
) -> pd.DataFrame:
    """ALOS for each disposition of COVID-19 case (total guesses)"""
    return pd.DataFrame({
        'day': admits_df.day,
        **{
            key: (
                    admits_df[key].cumsum().iloc[:-los]
                    - admits_df[key].cumsum().shift(los).fillna(0)
            ).apply(np.ceil)
            for key, los in lengths_of_stay.items()
        }
    })


class Seiar:
    def __init__(self, p: Parameters):

        self.N = p.N
        self.S_0 = p.S_0
        self.E_0 = p.E_0
        self.I_0 = p.I_0
        self.A_0 = p.A_0
        self.R_0 = p.R_0
        self.alpha = p.alpha
        self.beta_ill = p.beta_ill
        self.beta_asy = p.beta_asy
        self.gamma_ill = p.gamma_ill
        self.gamma_asy = p.gamma_asy
        self.rho = p.rho
        self.theta = p.theta
        self.start_date_simulation = p.start_date_simulation
        self.number_of_days = p.number_of_days
        self.projection = p.model_checkpoints
        self.run_simulation()
        self.results = []

    def model(self, t):
        S, E, I, A, R = [self.S_0 / self.N], [self.E_0 / self.N], [self.I_0 / self.N], [self.A_0 / self.N], [
            self.R_0 / self.N]

        dt = t[1] - t[0]
        time_asy, time_ill, beta_asy, beta_ill = self.projection['time_asy'], self.projection['time_ill'], \
                                                 self.projection['beta_asy'], self.projection['beta_ill']
        for tm in t[1:]:
            if tm in time_asy:
                print(tm, beta_asy)
                self.beta_asy = beta_asy[time_asy.index(tm)]
                print(tm, self.beta_asy)
                time_asy.pop(0)
                beta_asy.pop(0)
            if tm in time_ill:
                self.beta_ill = beta_ill[time_ill.index(tm)]
                print(tm, self.beta_ill)
                beta_ill.pop(0)
                time_ill.pop(0)
            next_S = S[-1] - (self.rho * self.beta_ill * S[-1] * I[-1] + self.rho * self.beta_asy * S[-1] * A[-1]) * dt
            next_E = E[-1] + (self.rho * self.beta_ill * S[-1] * I[-1] + self.rho * self.beta_asy * S[-1] * A[
                -1] - self.alpha * E[-1]) * dt
            next_I = I[-1] + (self.theta * self.alpha * E[-1] - self.gamma_ill * I[-1]) * dt
            next_A = A[-1] + ((1 - self.theta) * self.alpha * E[-1] - self.gamma_asy * A[-1]) * dt
            next_R = R[-1] + (self.gamma_ill * I[-1] + self.gamma_asy * A[-1]) * dt

            S.append(next_S)
            E.append(next_E)
            I.append(next_I)
            A.append(next_A)
            R.append(next_R)

        return np.stack([S, E, I, A, R]).T

    def run_simulation(self):
        t_max = 600
        dt = .01
        t = np.linspace(0, t_max, int(t_max / dt) + 1)

        results = self.model(t)

        df = pd.DataFrame(results)
        df = df.rename(columns={df.columns[0]: 'S', df.columns[1]: 'E', df.columns[2]: 'I', df.columns[3]: 'A',
                                df.columns[4]: 'R'})
        dates = pd.date_range(start=self.start_date_simulation, end='05/01/2030')
        df_I_E = df[::100].reset_index(drop=True)
        df_I_E.index = dates[:len(df_I_E)]

        df_I_E = df_I_E.rename(
            columns={'S': 'Susceptible', 'E': 'Exposed', 'I': 'Infected', 'A': 'Asymptomatic', 'R': 'Recovered'})
        infected_df = df_I_E[['Infected']] * self.N
        asymptomatic_df = df_I_E[['Asymptomatic']] * self.N
        recovered_df = df_I_E[['Recovered']] * self.N
        susceptible_df = df_I_E[['Susceptible']] * self.N
        exposed_df = df_I_E[['Exposed']] * self.N

        results = [
            infected_df.loc[:self.number_of_days],
            asymptomatic_df.loc[:self.number_of_days],
            recovered_df.loc[:self.number_of_days],
            susceptible_df.loc[:self.number_of_days],
            exposed_df.loc[:self.number_of_days]
        ]

        self.results = pd.concat(results, axis=1)
        return 0


class OLG:
    """
    calc_asymptomatic start from first case
    exposed are the asymptomatic_infected with lag not only infected
    asymptomatic_infected eq 10 does not always grow but uses two diferent R0

    fi  # proportion of infectives are never diagnosed
    theta = theta  # diagnosis daily rate

    """

    def __init__(self, df, p: Parameters, jh_hubei , have_serious_data=True):
        self.detected = []
        self.r_adj = np.array([])
        self.r_values = np.array([])
        self.r0d = np.array([])
        self.asymptomatic_infected = []
        self.df = pd.DataFrame()
        self.tmp = None
        self.have_serious_data = have_serious_data
        self.iter_countries(df, p, jh_hubei)

    @staticmethod
    def next_gen(r0, tau, c0, ct):
        r0d = r0 / tau
        return r0d * (ct - c0) + ct

    @staticmethod
    def true_a(fi, theta, d, d_prev, d_delta_ma):
        delta_detected = (d - d_prev)
        prev_asymptomatic_infected = (1 / (1 - fi)) * ((d_delta_ma) / theta + d_prev)
        return prev_asymptomatic_infected


    @staticmethod
    def crystal_ball(r_prev, hubei_prev, hubei_prev_t2, s_prev_t7):
        crystal_ball_coef = {'intercept': 1.462, 'r_prev': 0.915, 'hubei_prev': 0.05, 'hubei_prev_t2': 0.058, 's_prev_t7': 0.0152 }

        ln_r = crystal_ball_coef.get('intercept') + crystal_ball_coef.get('r_prev') * np.log(1+r_prev)\
                                                   + crystal_ball_coef.get('hubei_prev') * np.log(1+hubei_prev)\
                                                   + crystal_ball_coef.get('hubei_prev_t2') * np.log(1+hubei_prev_t2)\
                                                   - crystal_ball_coef.get('s_prev_t7') * s_prev_t7
        return np.exp(ln_r)

    def iter_countries(self, df, p, jh_hubei):

        self.process(detected=jh_hubei, init_infected=p.init_infected)
        self.calc_r(tau=p.tau, init_infected=p.init_infected)
        r_hubei = self.r_values

        for country in p.countries:
            # print(country)
            df_tmp = df[df['country'] == country].copy()
            # print(df_tmp)
            self.process(detected=df_tmp['total_cases'].values, init_infected=p.init_infected)
            self.calc_r(tau=p.tau, init_infected=p.init_infected)
            self.predict(tau=p.tau, scenario=p.scenario)
            self.calc_asymptomatic(fi=p.fi, theta=p.theta, init_infected=p.init_infected)
            self.write(df_tmp, tau=p.tau, critical_condition_rate=p.critical_condition_rate,
                       recovery_rate=p.recovery_rate, critical_condition_time=p.critical_condition_time,
                       recovery_time=p.recovery_time, r_hubei=r_hubei)

    def process(self, detected, init_infected):
        day_0 = np.argmax(detected >= init_infected)
        detected = detected[day_0:]
        self.detected = [detected[0]]
        for t in range(1, len(detected)):
            self.detected.append(max(detected[t - 1] + 1, detected[t]))

    def calc_r(self, tau, init_infected):
        epsilon = 1e-06
        detected = self.detected
        r_values = np.array([(detected[0] / (init_infected + epsilon) - 1) * tau])

        for t in range(1, len(detected)):
            if t <= tau:
                r_value = (detected[t] - detected[t - 1]) / (detected[t - 1] - 1) * tau
            elif t > tau:
                r_value = (detected[t] - detected[t - 1]) / (detected[t - 1] - detected[t - tau]) * tau
            r_values = np.append(r_values, max(r_value, 0))

        self.r_values, self.r_adj = r_values, np.convolve(r_values, np.ones(int(tau / 2, )) / int(tau / 2), mode='full')[:len(detected)]

    def predict(self, tau, scenario):
        forcast_cnt = sum(scenario['t'].values()) - 1
        t = len(self.detected) - 1
        scenario_wgt, cnt = 0, 0

        holt_model = Holt(self.r_adj[-tau:], exponential=True).fit(smoothing_level=0.1, smoothing_slope=0.9)
        self.r0d = np.append(self.r_adj[-1], holt_model.forecast(forcast_cnt))
        # self.r0d = holt_model.forecast(forcast_cnt)

        for i in scenario['t'].keys():
            while cnt < scenario['t'].get(i):
                c0 = self.detected[t - tau] if t - tau >= 0 else 0
                if cnt == 0 & scenario['R0D'].get(i) != 0:
                    scenario_wgt += self.r0d[cnt] * scenario['R0D'].get(i)
                self.r0d[cnt] = self.r0d[cnt] + scenario_wgt
                next_gen = self.next_gen(r0=self.r0d[cnt], tau=tau, c0=c0, ct=self.detected[t])
                self.detected.append(next_gen)
                t += 1
                cnt += 1

        # final decsecnt
        end_forecast = holt_model.forecast(tau)
        end_forecast_normed = end_forecast / end_forecast.max(axis=0)
        end_r0d = end_forecast_normed * (scenario_wgt + self.r0d[-1])

        end_r0d = end_r0d[end_r0d > 0]
        self.r0d = np.append(self.r0d, end_r0d)

        # cnt = 0
        while cnt < len(self.r0d):
            c0 = self.detected[t - tau]
            next_gen = self.next_gen(r0=self.r0d[cnt], tau=tau,
                                     c0=c0, ct=self.detected[t])
            self.detected.append(next_gen)
            t += 1
            cnt += 1

        self.r0d = np.append(self.r_adj, self.r0d)

    def calc_asymptomatic(self, fi, theta, init_infected):

        detected_deltas = [self.detected[0]]
        for i in range(1, len(self.detected)):
            delta = self.detected[i] - self.detected[i-1]
            detected_deltas.append(delta)

        detected_deltas_ma = np.convolve(detected_deltas, np.ones(int(4, )) / int(4), mode='full')[:len(detected_deltas)]
        asymptomatic_infected = [self.true_a(fi=fi, theta=theta, d=self.detected[0], d_prev=init_infected, d_delta_ma= detected_deltas_ma[0])]

        for t in range(1, len(self.detected)):
            prev_asymptomatic_infected = self.true_a(fi=fi, theta=theta, d=self.detected[t],  d_prev=self.detected[t - 1], d_delta_ma=detected_deltas_ma[i])
            asymptomatic_infected.append(prev_asymptomatic_infected)
        self.asymptomatic_infected = asymptomatic_infected

    def calc_crystall_ball(self, df, r_hubei):
        size = min(len(df), len(r_hubei))
        df.loc[:size, 'hubei_detected'] = r_hubei[:size]

        crystall_ball_list = [self.r0d[0]]
        for t in range(1, len(df) - 1):
            projected_r = self.crystal_ball(self.r0d[t-1], r_hubei[t-1], r_hubei[max(0, t-2)], df['StringencyIndex'][max(0, t-7)])
            crystall_ball_list.append(projected_r)

        df.loc[:len(crystall_ball_list) - 1, 'crystall_ball'] = crystall_ball_list
        return df

    def write(self, df_o, tau, critical_condition_rate, recovery_rate, critical_condition_time, recovery_time, r_hubei):
        forcast_cnt = len(self.detected) - len(self.r_adj)
        if self.have_serious_data==False:
            df_o['serious_critical'] = (df_o['total_cases'].shift(critical_condition_time)
                                        - df_o['total_cases'].shift(recovery_time+critical_condition_time)) * critical_condition_rate
            df_o['new_cases'] = df_o['total_cases'] - df_o['total_cases'].shift(1)
            df_o['activecases'] = None
        df = df_o[-len(self.r_adj):][['date', 'country', 'StringencyIndex', 'serious_critical', 'new_cases', 'activecases']].reset_index(drop=True).copy()
        df['r_values'] = self.r_values

        # pad df for predictions
        predict_date = df['date'].max() + pd.to_timedelta(1, unit="D")
        prediction_dates = pd.date_range(start=predict_date.strftime('%Y-%m-%d'), periods=forcast_cnt)
        predicted = pd.DataFrame({'date': prediction_dates})

        df = df.append(predicted, ignore_index=True)

        df['total_cases'] = self.detected
        df['R'] = self.r0d

        df['infected'] = self.asymptomatic_infected
        df['exposed'] = df['infected'].shift(periods=-tau)
        df['country'].fillna(method='ffill', inplace=True)
        df['corona_days'] = pd.Series(range(1, len(df) + 1))
        df['prediction_ind'] = np.where(df['corona_days'] <= len(self.r_adj), 0, 1)
        if df['country'][0]=='israel':
            df = self.calc_crystall_ball(df, r_hubei)

        df['Currently Infected'] = np.where(df['corona_days'] <= (critical_condition_time + recovery_time),
                                            df['total_cases'],
                                            df['total_cases'] - df['total_cases'].shift(periods=(critical_condition_time + recovery_time)))

        df['Doubling Time'] = np.log(2) / np.log(1 + df['R'] / tau)

        df['dI'] = df['total_cases'] - df['total_cases'].shift(1)
        df['dA'] = df['infected'] - df['infected'].shift(1)
        df['dE'] = df['exposed'] - df['exposed'].shift(1)

        # critical condition calc
        df['Critical_condition'] = df['Currently Infected'] * critical_condition_rate
        df['Recovery_Critical'] = df['Critical_condition'] * recovery_rate
        df['Mortality_Critical'] = df['Critical_condition'] - df['Recovery_Critical']

        df['Critical_condition'] = df['Critical_condition'].shift(periods=-critical_condition_time).round(0)
        df[['Mortality_Critical', 'Recovery_Critical']] = df[['Mortality_Critical', 'Recovery_Critical']].shift(periods=critical_condition_time + recovery_time).round(0)

        # critical condition world_meter
        df['Critical_condition_test'] = df['total_cases'].shift(periods=+recovery_time) - df['total_cases'].shift(periods=+(critical_condition_time + recovery_time))
        df['Critical_condition_test'] = df['Critical_condition_test'] * critical_condition_rate

        tmp = df[['date', 'R', 'total_cases', 'Critical_condition_test']]

        # fill with obsereved values
        if self.have_serious_data:
            df['Critical_condition'] = np.where(~df['serious_critical'].isna(), df['serious_critical'], df['Critical_condition'])
            df['Critical_condition_test'] = np.where(~df['serious_critical'].isna(), df['serious_critical'], df['Critical_condition_test'])
            df['dI2'] = np.where(~df['new_cases'].isna(), df['new_cases'], df['dI'])
            df['Currently Infected2'] = np.where(~df['activecases'].isna(), df['activecases'], df['Currently Infected'])

        df = df.rename(columns={'total_cases': 'Total Detected', 'infected': 'Total Infected', 'exposed': 'Total Exposed',
                                'dI': 'New Detected', 'dA': 'New Infected', 'dE': 'New Exposed'})

        self.df = pd.concat([self.df, df])


class CountryData:
    def __init__(self, country_files):
        self.country_files = country_files
        self.country_df = self.get_country_data()
        self.stringency_df = self.get_country_stringency()
        self.df = self.get_data()
        self.sir_df = self.get_sir()
        self.jh_confirmed_df = self.get_jhopkins_confirmed()

    def get_country_data(self):
        country_df = pd.read_csv(self.country_files['country_file'])
        # country_df = country_df.set_index('Country')
        country_df = country_df.drop(columns="Unnamed: 0")
        # country_df['date'] = country_df['date'].apply(lambda x: x if x.month<4 else x - relativedelta(years=1))
        # country_df['date'] = pd.to_datetime(country_df['date'],format="%d/%m/%Y")
        country_df['date'] = pd.to_datetime(country_df['date'], format="%Y-%m-%d")
        country_df = country_df.rename(columns={'country': 'Country'})
        country_df['new_deaths'] = country_df['new_deaths'].str.replace('+', '')
        country_df['new_deaths'] = country_df['new_deaths'].str.replace(',', '')
        country_df['new_deaths'] = country_df['new_deaths'].apply(lambda x: float(x))
        return country_df

    def get_country_stringency(self):
        country_st_df = pd.read_excel(self.country_files['stringency_file'])
        country_st_df['date'] = pd.to_datetime(country_st_df['Date'], format="%Y%m%d")
        return country_st_df

    def get_data(self):
        df = self.country_df.merge(self.stringency_df, left_on=["Country", "date"], right_on=["CountryName", "date"])
        return df

    def get_sir(self):
        sir_df = pd.read_csv(self.country_files['sir_file'])
        # sir_df = sir_df.set_index('Country')
        sir_df = sir_df.drop(columns="Unnamed: 0")
        # sir_df['date'] = sir_df['date'].apply(lambda x: x if x.month<4 else x - relativedelta(years=1))
        # sir_df['date'] = pd.to_datetime(sir_df['date'],format="%d/%m/%Y")
        sir_df['date'] = pd.to_datetime(sir_df['date'], format="%Y-%m-%d")
        sir_df['country'] = sir_df['country'].str.capitalize()
        sir_df = sir_df.rename(columns={'country': 'Country'})
        return sir_df

    def get_jhopkins_confirmed(self):
        df = pd.read_csv(self.country_files['jhopkins_confirmed'])
        # df = df.drop(columns="Unnamed: 0")
        colnames = df.columns
        df = df.melt(id_vars=['Province/State', 'Country/Region'], value_vars=colnames[2:])
        df['variable'] = pd.to_datetime(df['variable'], format="%m/%d/%y", errors='coerce')
        df = df[df["variable"].dt.year > 1677].dropna(subset=['value'])
        df = df.rename(columns={'Country/Region': 'Country', 'Province/State': 'Province'})
        df['Province'] = df['Province'].fillna('All')
        # df = df.rename(columns={'יישוב':'Yishuv', 'variable':'date'})
        return df

class IsraelData:
    def __init__(self, israel_files):
        self.filepath = israel_files
        self.yishuv_df = self.get_yishuv_data()
        self.isolation_df = self.get_isolation_df()
        self.lab_results_df = self.get_lab_results_df()
        self.tested_df = self.get_tested_df()
        self.patients_df = self.get_patients_df()

    @st.cache
    def get_yishuv_data(self):
        df = pd.read_csv(self.filepath['yishuv_file'])
        df = df.drop(columns="Unnamed: 0")
        id_vars = ['יישוב', 'סוג מידע','אוכלוסייה נכון ל- 2018']
        colnames = [c for c in df.columns if c not in id_vars]
        df = df.melt(id_vars=id_vars, value_vars=colnames)
        df['variable'] = pd.to_datetime(df['variable'], format="%d/%m/%Y", errors='coerce')
        df = df[df["variable"].dt.year>1677].dropna()
        df = df.rename(columns={'יישוב':'Yishuv','אוכלוסייה נכון ל- 2018':'pop2018', 'variable':'date'})
        return df

    @st.cache
    def get_isolation_df(self):
        df = pd.read_csv(self.filepath['isolations_file'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index("date", drop=False)
        df = df.drop(columns="_id")
        return df

    @st.cache
    def get_lab_results_df(self):
        df = pd.read_csv(self.filepath['lab_results_file'])
        df['result_date'] = pd.to_datetime(df['result_date'])
        return df

    @st.cache
    def get_tested_df(self):
        df = pd.read_csv(self.filepath['tested_file'])
        df['None'] = df[df.columns[2:]].sum(axis=1)
        df['None'] = df['None'].apply(lambda x: 0 if x > 0 else 1)
        df['At Least One'] = df['None'].apply(lambda x: 0 if x > 0 else 1)
        df['test_date'] = pd.to_datetime(df['test_date'])
        df = df.drop(columns="_id")
        return df

    @st.cache
    def get_patients_df(self):
        df = pd.read_csv(self.filepath['patients_file'])
        df = df.dropna(subset=['New Patients Amount'])
        df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
       # df = df.drop(columns="_id")
        return df


def get_sir_country_file(sir_country_file):
    sir_country_df = pd.read_csv(sir_country_file, parse_dates=['date'])
    # sir_country_df['I'] = sir_country_df['total_cases']
    return sir_country_df


class StringencyIndex:
    def __init__(self):
        OXDF = "OxCGRT_Download_180420_223736_Full.csv"
        self.filepath = os.path.join(os.getcwd(), "Resources", "Datasets", "CountryData", OXDF)
        self.oxford_df = pd.read_csv(os.path.join(os.getcwd(), "Resources", "Datasets", "CountryData", OXDF))
        self.input_df = pd.DataFrame()
        self.output_df = pd.DataFrame()
        self.max_val = {'S1': 2., 'S2': 2., 'S3': 2., 'S4': 2., 'S5': 1., 'S6': 2., 'S7': 3.}
        self.project_til = None

    def get_latest(self):
        s1_7 = tuple("S" + str(i) + "_" for i in range(1, 8, 1))
        keep_cols = [c for c in self.oxford_df.columns if c.startswith(s1_7)]
        keep_cols = [c for c in keep_cols if c.find('Notes') == -1]
        oxford_df = self.oxford_df.dropna(subset=['StringencyIndex'])
        oxford_df = oxford_df.fillna('ffill')
        oxford_df = oxford_df[keep_cols]
        oxford_dict = oxford_df[-1:].to_dict('records')[0]
        return oxford_dict

    def display_st(self, st):
        oxford_dict = self.get_latest()
        st.sidebar.subheader("Oxford Index")
        output = {}
        oxford_start = oxford_dict.copy()
        self.project_til = st.sidebar.date_input("Project until:")
        max_val = self.max_val
        for k, v in oxford_dict.items():
            if k.find('IsGeneral') > -1:
                output[k] = st.sidebar.checkbox(k, oxford_dict[k] * True) * 1.
            else:
                output[k] = st.sidebar.number_input(k.split("_")[1], value=oxford_dict[k], min_value=0.,
                                                    max_value=max_val[k[:2]], step=1.)
                output[k + '_date'] = st.sidebar.date_input("Date " + k.split("_")[1])
                # add original date
                oxford_start[k + '_date'] = datetime.date.today()
        self.input_df = pd.DataFrame([oxford_start, output])

    def calculate_stringency(self):
        max_val = self.max_val
        temp = self.input_df.copy()
        cols = temp.columns
        date_cols = [c for c in cols if c.find('_date') > -1]
        temp[date_cols] = temp[date_cols].apply(lambda x: pd.to_datetime(x))
        # dts = temp[date_cols].apply(lambda x: max(x), axis=1).values
        # dts_range = pd.date_range(dts[0], dts[1])
        dts_range = pd.date_range(datetime.date.today(),  self.project_til)
        temp['times'] = None
        temp['times'] = [1, len(dts_range) - 1]

        temp = temp.loc[temp.index.repeat(temp.times)]
        temp.drop(columns='times', inplace=True)
        temp['date'] = dts_range
        cols = temp.columns
        cols = [c for c in cols if c.find('IsGeneral') == -1]
        cols = [c for c in cols if c.find('date') == -1]
        temp = temp.reset_index(drop=True)
        for k in cols:
            for i in temp.index:
                if temp.loc[i, k + "_date"] != temp.loc[i, 'date']:
                    temp.at[i, k] = temp.loc[i - 1, k]
                    try:
                        temp.at[i, k[:2] + "_IsGeneral"] = temp.loc[i - 1, k + "_IsGeneral"]
                    except:
                        pass

        for k in cols:
            if k[:2] != 'S7':
                temp[k[:2] + '_score'] = (temp[k] + temp[k[:2] + "_IsGeneral"]) / (max_val[k[:2]] + 1)
            else:
                temp[k[:2] + '_score'] = temp[k] / (max_val[k[:2]])

        cols = temp.columns
        score_cols = [c for c in cols if c.find("score") > -1]
        temp['StringencyIndex'] = temp[score_cols].apply(lambda x: np.average(x), axis=1)
        cols = list(temp.columns)
        cols.insert(0, cols.pop(cols.index('StringencyIndex')))
        cols.insert(0, cols.pop(cols.index('date')))
        temp = temp.loc[:, cols]
        self.output_df = temp
        return temp




