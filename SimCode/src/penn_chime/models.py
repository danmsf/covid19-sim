"""Models.

Changes affecting results or their presentation should also update
parameters.py `change_date`, so users can see when results have last
changed
"""

from __future__ import annotations

from typing import Dict, Generator, Tuple

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from penn_chime.parameters import Parameters

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

    def __init__(self, df, p: Parameters2):
        self.detected = []
        self.rma = np.array([])
        self.r_values = np.array([])
        self.R0D = int
        self.asymptomatic_infected = []
        self.df = pd.DataFrame()
        self.r_contagion = []

        self.tmp = None

        self.iter_countries(df, tau=p.tau, init_infected=p.init_infected, theta=p.theta, fi=p.fi, scenario=p.scenario,
                            comparator_country=p.comparator_country, contagion_pi_country=p.contagion_pi_country,
                            countries=p.countries)

    @staticmethod
    def next_gen(r0, tau, c0, ct):
        r0d = r0 / tau
        return ct * (1 + r0d) ** tau - c0 * r0d * (1 + r0d) ** (tau - 1)

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

    def iter_countries(self, df, tau, init_infected, theta, fi, scenario,
                       comparator_country, contagion_pi_country, countries='Israel'):
        for country in countries:
            df_tmp = df[df['Country'] == country].copy()
            self.process(detected=df_tmp['I'].values, init_infected=init_infected)
            self.calc_r(tau=tau, init_infected=init_infected, scenario=scenario)
            self.predict(tau=tau, scenario=scenario)
            self.calc_asymptomatic(fi=fi, theta=theta, init_infected=init_infected)
            self.write(df_tmp, tau=tau)


        if comparator_country is not None:
            df = df[df['Country'] == comparator_country].copy()
            self.calc_r(tau=tau, init_infected=init_infected, scenario=scenario)
            self.write_comparator(df)
        #     self.policy_on_contagion(countries, contagion_pi_country)

    def process(self, detected, init_infected):
        day_0 = np.argmax(detected > init_infected)
        detected = detected[day_0 - 1:]
        self.detected = []
        for t in range(1, len(detected)):
            self.detected.append(max(detected[t - 1] + 1, detected[t]))

    def calc_r(self, tau, init_infected, scenario):
        detected = self.detected
        forcast_cnt = sum(scenario['t'].values())
        r_values = np.array([(detected[0] / (init_infected + 1e-05) - 1) * tau])

        for t in range(1, len(detected)):
            if t <= tau:
                r_value = (detected[t] / (detected[t - 1] + 1e-05) - 1) * tau
            else:
                r_value = (detected[t] / (detected[t - 1] - detected[t - tau] + detected[t - tau - 1]) - 1) * tau
            r_values = np.append(r_values, max(r_value, 0))

        # holt_model = Holt(r_values, exponential=True).fit(smoothing_level=0.8, smoothing_slope=0.2)
        # holt = holt_model.forecast(forcast_cnt)

        rma_model = np.convolve(r_values, np.ones((tau,)) / tau, mode='full')[:-tau + 1]

        exp_smot_model = SimpleExpSmoothing(r_values[-tau:]).fit()
        exp_smot = exp_smot_model.forecast(forcast_cnt)

        # print(len(holt_model), len(rma_model), len(exp_smot))


        self.r_values, self.R0D, self.rma  = r_values, exp_smot[-1], r_values

    def predict(self, tau, scenario):
        t = len(self.detected) - tau
        cnt = 0

        for i in scenario['t'].keys():
            while cnt <= scenario['t'].get(i):
                c0 = self.detected[t - tau] if t - tau >= 0 else 0
                next_gen = self.next_gen(r0=self.R0D * (scenario['R0D'].get(i) + 1), tau=tau, c0=c0,
                                         ct=self.detected[t])
                self.detected.append(next_gen)
                t += 1
                cnt += 1

    def calc_asymptomatic(self, fi, theta, init_infected):
        asymptomatic_infected = [self.true_a(fi=fi, theta=theta, d=self.detected[0], d_prev=init_infected)]

        for t in range(1, len(self.detected)):
            prev_asymptomatic_infected = self.true_a(fi=fi, theta=theta, d=self.detected[t],
                                                     d_prev=self.detected[t - 1])
            asymptomatic_infected.append(
                max(prev_asymptomatic_infected, asymptomatic_infected[-1]))  # not in Michel's paper!!!!!!!

        self.asymptomatic_infected = asymptomatic_infected

    def write(self, df, tau):
        forcast_cnt = len(self.detected) - len(self.rma)
        df = df[-len(self.rma):][['Country', 'StringencyIndex']].copy()

        df['r_values'] = self.r_values
        df['R'] = self.rma
        df['I'] = self.detected[:len(self.rma)]

        predicted = pd.DataFrame(
            {'I': self.detected[-forcast_cnt:],
             'R': self.R0D})
        df = df.append(predicted, ignore_index=True)

        df['A'] = self.asymptomatic_infected
        df['A'] = df['A'].shift(periods=-1)
        df['E'] = df['A'].shift(periods=-tau - 1)
        df['A'] = df['A'] - df['I']
        df['Country'].fillna(method='ffill', inplace=True)
        df['corona_days'] = pd.Series(range(1, len(df) + 1))
        df['prediction_ind'] = np.where(df['corona_days'] < len(self.rma), 0, 1)
        self.df = pd.concat([self.df, df])

    def write_comparator(self, df):

        comparator_df = pd.DataFrame({'comparator_R':self.rma})
        comparator_df['comparator_Stringency'] = df[-len(self.rma):][['StringencyIndex']].copy()
        comparator_df['corona_days'] = list(range(1, comparator_df.shape[0] + 1))

        self.df = self.df.merge(comparator_df, on='corona_days', how='left')
        self.df['comparator_R'].fillna(self.R0D, inplace=True)

    def policy_on_contagion(self, countries, contagion_pi_country):
        for country in countries:
            print(country)
            tmp_country_df = self.df.query('Country == @country').copy()
            print(len(tmp_country_df))
            tmp_country_df[['R_prev', 'comparator_R_prev', 'StringencyIndex_prev', 'comparator_Stringency_prev']] \
                = tmp_country_df[['R', 'comparator_R', 'StringencyIndex', 'comparator_Stringency']].shift(periods=1)
            tmp_country_df['R_contagion_score'] = tmp_country_df.apply(
                lambda row: self.project_contagion(contagion_pi_country,
                                                   row['R_prev'],
                                                   row['comparator_R_prev'],
                                                   row['comparator_R'],
                                                   row['StringencyIndex_prev'],
                                                   row['StringencyIndex'],
                                                   row['comparator_Stringency_prev'],
                                                   row['comparator_Stringency']
                                                   ),
                axis=1)

            tmp_country_df.drop(['R_prev', 'comparator_R_prev', 'StringencyIndex_prev', 'comparator_Stringency_prev'],
                                axis=1, inplace=True)
            self.df = self.df.query('Country != @country').append(tmp_country_df)

    def plot_data(self, countries, var_in_multi_line='I'):
        country_count = self.df['Country'].nunique()

        if country_count == len(countries):
            plot_df = self.df.query('prediction_ind==0').melt(id_vars=['corona_days'], value_vars=['A', 'I', 'E'])
            plot_df_predict = self.df.query('prediction_ind==1').melt(id_vars=['corona_days'], value_vars=['A', 'I'])

        else:
            plot_df = self.df.query('prediction_ind==0').pivot(index='corona_days', columns='Country',
                                                               values=var_in_multi_line).reset_index().melt(
                id_vars=['corona_days'],
                value_vars=countries)
            plot_df_predict = self.df.query('prediction_ind==1').pivot(index='corona_days', columns='Country',
                                                                       values=var_in_multi_line).reset_index().melt(
                id_vars=['corona_days'],
                value_vars=countries)

        plot_df.dropna(inplace=True)
        plot_df_predict.dropna(inplace=True)
        plot_df['value'] = plot_df['value'].astype('int64')
        plot_df_predict['value'] = plot_df_predict['value'].astype('int64')

        color_group = 'variable' if country_count == 1 else 'Country'

        # The basic line
        line = alt.Chart(plot_df).mark_line(interpolate='basis').encode(
            x='corona_days:Q',
            y='value',
            color=color_group
        )

        line2 = alt.Chart(plot_df_predict).mark_line(interpolate='basis', strokeDash=[1, 1]).encode(
            x='corona_days:Q',
            y='value',
            color=color_group
        )

        return alt.layer(
            line, line2
        ).properties(
            width=600, height=300
        )

    def plot_data_contagion_score(self):

        plot_df = self.df.query('prediction_ind==0')[['corona_days', 'StringencyIndex', 'r_values']]
        plot_df = plot_df.melt(id_vars=['corona_days'], value_vars=['StringencyIndex', 'r_values']).dropna()

        plot_df_contagion = self.df.query('prediction_ind==0')[['corona_days', 'R_contagion_score']]
        # plot_df_contagion['R_contagion_score'].clip(upper=10, inplace=True)
        plot_df_contagion = plot_df_contagion.melt(id_vars=['corona_days'], value_vars=['R_contagion_score'])

        line = alt.Chart(plot_df).mark_line(interpolate='basis').encode(
            x='corona_days:Q',
            y='value',
            color='variable'
        )

        line2 = alt.Chart(plot_df_contagion).mark_line(interpolate='basis', strokeDash=[1, 1]).encode(
            x='corona_days:Q',
            y='value',
            color='variable'
        )

        return alt.vconcat(line, line2).configure_view(stroke='transparent')


class CountryData:
    def __init__(self, country_file, stringency_file, sir_file):
        self.country_file = country_file
        self.sir_file = sir_file
        self.stringency_file = stringency_file
        self.country_df = self.get_country_data()
        self.stringency_df = self.get_country_stringency()
        self.df = self.get_data()
        self.sir_df = self.get_sir()

    def get_country_data(self):
        country_df = pd.read_csv(self.country_file)
        # country_df = country_df.set_index('Country')
        country_df = country_df.drop(columns="Unnamed: 0")
        # country_df['date'] = country_df['date'].apply(lambda x: x if x.month<4 else x - relativedelta(years=1))
        # country_df['date'] = pd.to_datetime(country_df['date'],format="%d/%m/%Y")
        country_df['date'] = pd.to_datetime(country_df['date'], format="%Y-%m-%d")
        country_df = country_df.rename(columns={'country' : 'Country'})

        return country_df

    def get_country_stringency(self):
        country_st_df = pd.read_excel(self.stringency_file)
        country_st_df['date'] = pd.to_datetime(country_st_df['Date'], format="%Y%m%d")
        return country_st_df

    def get_data(self):
        df = self.country_df.merge(self.stringency_df, left_on=["Country", "date"], right_on=["CountryName", "date"])
        return df

    def get_sir(self):
        sir_df = pd.read_csv(self.sir_file)
        # sir_df = sir_df.set_index('Country')
        sir_df = sir_df.drop(columns="Unnamed: 0")
        # sir_df['date'] = sir_df['date'].apply(lambda x: x if x.month<4 else x - relativedelta(years=1))
        # sir_df['date'] = pd.to_datetime(sir_df['date'],format="%d/%m/%Y")
        sir_df['date'] = pd.to_datetime(sir_df['date'], format="%Y-%m-%d")
        sir_df['country'] = sir_df['country'].str.capitalize()
        sir_df = sir_df.rename(columns={'country':'Country'})
        return sir_df


class IsraelData:
    def __init__(self, israel_files):
        self.filepath = israel_files
        self.yishuv_df = self.get_yishuv_data()
        self.isolation_df = self.get_isolation_df()
        self.lab_results_df = self.get_lab_results_df()
        self.tested_df = self.get_tested_df()
        self.patients_df = self.get_patients_df()

    def get_yishuv_data(self):
        df = pd.read_excel(self.filepath['yishuv_file'])
        colnames = df.columns
        df = df.melt(id_vars=['יישוב'], value_vars=colnames[1:])
        df['variable'] = pd.to_datetime(df['variable'],format="%d/%m/%Y", errors='coerce')
        df = df[df["variable"].dt.year>1677].dropna()
        df = df.rename(columns={'יישוב':'Yishuv', 'variable':'date'})
        return df

    def get_isolation_df(self):
        df = pd.read_csv(self.filepath['isolations_file'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index("date", drop=False)
        df = df.drop(columns="_id")
        return df

    def get_lab_results_df(self):
        df = pd.read_csv(self.filepath['lab_results_file'])
        df['result_date'] = pd.to_datetime(df['result_date'])
        return df

    def get_tested_df(self):
        df = pd.read_csv(self.filepath['tested_file'])
        df['None'] = df[df.columns[2:]].sum(axis=1)
        df['None'] = df['None'].apply(lambda x: 0 if x > 0 else 1)
        df['At Least One'] = df['None'].apply(lambda x: 0 if x > 0 else 1)
        df['test_date'] = pd.to_datetime(df['test_date'])
       # df = df.drop(columns="_id")
        return df

    def get_patients_df(self):
        df = pd.read_csv(self.filepath['patients_file'])
        df = df.dropna(subset=['New Patients Amount'])
        df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
       # df = df.drop(columns="_id")
        return df


def get_sir_country_file(sir_country_file):
    sir_country_df = pd.read_csv(sir_country_file, usecols=['I', 'date', 'country'], parse_dates=['date'])
    return sir_country_df




