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
        self.results=[]


    def model(self,t):
        S, E, I, A, R = [self.S_0/self.N], [self.E_0/self.N], [self.I_0/self.N], [self.A_0/self.N], [self.R_0/self.N]

        dt = t[1] - t[0]
        time_asy, time_ill, beta_asy, beta_ill = self.projection['time_asy'], self.projection['time_ill'], self.projection['beta_asy'], self.projection['beta_ill']
        for tm in t[1:]:
            if tm in time_asy:
                print(tm, beta_asy)
                self.beta_asy = beta_asy[time_asy.index(tm)]
                print(tm, self.beta_asy)
                time_asy.pop(0)
                beta_asy.pop(0)
            if tm in time_ill:
                self.beta_ill = beta_ill[time_ill.index (tm)]
                print(tm, self.beta_ill)
                beta_ill.pop(0)
                time_ill.pop(0)
            next_S = S[-1] - (self.rho * self.beta_ill * S[-1] * I[-1] + self.rho * self.beta_asy * S[-1] * A[-1]) * dt
            next_E = E[-1] + (self.rho * self.beta_ill * S[-1] * I[-1] + self.rho * self.beta_asy * S[-1] * A[-1] - self.alpha * E[-1]) * dt
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
        df = df.rename(columns={df.columns[0]: 'S', df.columns[1]: 'E', df.columns[2]: 'I', df.columns[3]: 'A', df.columns[4]: 'R'})
        dates = pd.date_range(start=self.start_date_simulation, end='05/01/2030')
        df_I_E = df[::100].reset_index(drop=True)
        df_I_E.index = dates[:len(df_I_E)]

        df_I_E = df_I_E.rename(columns={'S': 'Susceptible', 'E': 'Exposed', 'I': 'Infected', 'A': 'Asymptomatic', 'R': 'Recovered'})
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

        self.results = pd.concat(results, axis = 1)
        return 0


class OLG:
    """
    calc_asymptomatic start from first case
    exposed are the asymptomatic_infected with lag not only infected
    asymptomatic_infected eq 10 does not always grow but uses two diferent R0

    fi  # proportion of infectives are never diagnosed
    theta = theta  # diagnosis daily rate

    """

    def __init__(self, df, p: Parameters):
        self.detected = []
        self.r_adj = np.array([])
        self.r_values = np.array([])
        self.r0d = int
        self.asymptomatic_infected = []
        self.df = pd.DataFrame()
        self.tmp = None

        self.iter_countries(df, tau=p.tau, init_infected=p.init_infected, theta=p.theta, fi=p.fi, scenario=p.scenario, countries=p.country)

    @staticmethod
    def next_gen(r0, tau, c0, ct):
        r0d = r0 / tau
        # return ct * (1 + r0d) ** tau - c0 * r0d * (1 + r0d) ** (tau - 1) # Eq 2
        return c0 * (r0d) + ct

    @staticmethod
    def true_a(fi, theta, d, d_prev):
        delta_detected = (d - d_prev)
        prev_asymptomatic_infected = 1 / (1 - fi) * (delta_detected / theta + d_prev)
        return prev_asymptomatic_infected

    @staticmethod
    def project_contagion(pi, r_prev, comparator_r_prev, comparator_r, s_prev, s, s_comparator_prev, s_comparator):
        r_comparator_delta_ln = np.log(comparator_r) / np.log(comparator_r_prev) - 1
        s_delta = s / s_prev - 1
        s_comparator_delta = s_comparator / s_comparator_prev - 1
        ln_r = np.log(r_prev) + r_comparator_delta_ln + pi * (s_delta - s_comparator_delta)
        return np.exp(ln_r)

    def iter_countries(self, df, tau, init_infected, theta, fi, scenario, countries='israel'):
        for country in countries:
            df_tmp = df[df['country'] == country].copy()
            self.process(detected=df_tmp['I'].values, init_infected=init_infected)
            self.calc_r(tau=tau, init_infected=init_infected, scenario=scenario)
            self.predict(tau=tau, scenario=scenario)
            self.calc_asymptomatic(fi=fi, theta=theta, init_infected=init_infected)
            self.write(df_tmp, tau=tau)

    def process(self, detected, init_infected):
        day_0 = np.argmax(detected > init_infected)
        detected = detected[day_0 - 1:]
        self.detected = []
        for t in range(1, len(detected)):
            self.detected.append(max(detected[t - 1] + 1, detected[t]))

    def calc_r(self, tau, init_infected, scenario):
        detected = self.detected
        r_values = np.array([(detected[0] / (init_infected + 1e-05) - 1) * tau])

        for t in range(1, len(detected)):
            if t <= tau:
                r_value = (detected[t] / (detected[t - 1] + 1e-05) - 1) * tau
            elif t > tau:
                r_value = (detected[t] / (detected[t - 1] - detected[t - tau] + detected[t - tau - 1]) - 1) * tau
            r_values = np.append(r_values, max(r_value, 0))
        # print(len(holt_model), len(r_adj_model), len(exp_smot))
        self.r_values = r_values

    def predict(self, tau, scenario):
        forcast_cnt = sum(scenario['t'].values())
        t = len(self.detected) - 1
        cnt, predicted_cnt = 0, 0

        holt_model = Holt(self.r_values[-tau:], exponential=True).fit(smoothing_level=0.6, smoothing_slope=0.1)
        self.r0d = holt_model.forecast(forcast_cnt)

        r_adj_model = np.convolve(self.r_values, np.ones((tau,)) / tau, mode='full')[:-tau + 1]

        exp_smot_model = SimpleExpSmoothing(self.r_values[-tau:]).fit()
        exp_smot = exp_smot_model.forecast(forcast_cnt)

        self.r_adj = self.r_values

        for i in scenario['t'].keys():
            predicted_cnt += cnt
            cnt = 0
            while cnt < scenario['t'].get(i):
                c0 = self.detected[t - tau] if t - tau >= 0 else 0
                next_gen = self.next_gen(r0=self.r0d[cnt + predicted_cnt] * (scenario['R0D'].get(i) + 1), tau=tau,
                                         c0=c0, ct=self.detected[t])
                # print(self.r0d[cnt + predicted_cnt] * (scenario['r0d'].get(i) + 1), c0, self.detected[t], next_gen, )
                self.detected.append(next_gen)
                t += 1
                cnt += 1

    def calc_asymptomatic(self, fi, theta, init_infected):
        asymptomatic_infected = [self.true_a(fi=fi, theta=theta, d=self.detected[0], d_prev=init_infected)]

        for t in range(1, len(self.detected)):
            prev_asymptomatic_infected = self.true_a(fi=fi, theta=theta, d=self.detected[t],
                                                     d_prev=self.detected[t - 1])
            # asymptomatic_infected.append(
            #     max(prev_asymptomatic_infected, asymptomatic_infected[-1]))  # not in Michel's paper!!!!!!!

            asymptomatic_infected.append(prev_asymptomatic_infected)
        self.asymptomatic_infected = asymptomatic_infected

    def write(self, df, tau):
        forcast_cnt = len(self.detected) - len(self.r_adj)
        df = df[-len(self.r_adj):][['date', 'country', 'StringencyIndex', ]].copy()

        df['r_values'] = self.r_values
        df['R'] = self.r_adj
        df['I'] = self.detected[:len(self.r_adj)]

        predict_date = df['date'].max() + pd.to_timedelta(1, unit="D")
        prediction_dates = pd.date_range(start=predict_date.strftime('%Y-%m-%d'), periods=forcast_cnt)

        predicted = pd.DataFrame(
            {'date': prediction_dates,
             'I': self.detected[-forcast_cnt:],
             'R': self.r0d,
             })
        df = df.append(predicted, ignore_index=True)

        df['A'] = self.asymptomatic_infected
        df['A'] = df['A'].shift(periods=-1)
        df['E'] = df['A'].shift(periods=-tau -1)
        df['A'] = df['A'] - df['I']
        df['country'].fillna(method='ffill', inplace=True)
        df['corona_days'] = pd.Series(range(1, len(df) + 1))
        df['prediction_ind'] = np.where(df['corona_days'] < len(self.r_adj), 0, 1)
        df['dI'] = df['I'] - df["I"].shift(1)
        df['dA'] = df['A'] - df["A"].shift(1)
        df['dE'] = df['E'] - df["E"].shift(1)
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
        country_df = country_df.rename(columns={'country' : 'Country'})
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
        sir_df = sir_df.rename(columns={'country':'Country'})
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
        colnames = df.columns
        df = df.melt(id_vars=['יישוב'], value_vars=colnames[1:])
        df['variable'] = pd.to_datetime(df['variable'], format="%d/%m/%Y", errors='coerce')
        df = df[df["variable"].dt.year>1677].dropna()
        df = df.rename(columns={'יישוב':'Yishuv', 'variable':'date'})
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
       # df = df.drop(columns="_id")
        return df

    @st.cache
    def get_patients_df(self):
        df = pd.read_csv(self.filepath['patients_file'])
        df = df.dropna(subset=['New Patients Amount'])
        df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
       # df = df.drop(columns="_id")
        return df


def get_sir_country_file(sir_country_file):
    sir_country_df = pd.read_csv(sir_country_file, usecols=['I', 'date', 'country', 'StringencyIndex'], parse_dates=['date'])
    return sir_country_df




