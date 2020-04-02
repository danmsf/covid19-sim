"""Models.

Changes affecting results or their presentation should also update
parameters.py `change_date`, so users can see when results have last
changed
"""

from __future__ import annotations

from typing import Dict, Generator, Tuple

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from .parameters import Parameters

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
        self.run_simulation()
        self.results=[]


    def model(self,t):
        S, E, I, A, R = [self.S_0/self.N], [self.E_0/self.N], [self.I_0/self.N], [self.A_0/self.N], [self.R_0/self.N]

        dt = t[1] - t[0]
        for _ in t[1:]:
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
    asymptomatic_infected does not always grow


    fi  # proportion of infectives are never diagnosed
    gamma = gamma  # diagnosis daily rate

    """
    def __init__(self, p: Parameters):
        self.periods_count = len(p.detected)
        self.first_case = np.argmax(p.detected > p.init_infected)  # First case

        self.detected = self.increasing_values(p.detected)
        self.asymptomatic_infected = self.calc_asymptomatic(fi=p.fi, gamma=p.gamma)

        self.RMA_D, self.R0_D = self.calc_r(self.detected, tau=p.tau)
        self.RMA_C, self.R0_C = self.calc_r(self.asymptomatic_infected, tau=p.tau)

        self.predict(tau=p.tau)
        self.df = self.create_df(p.tau)

    @staticmethod
    def movingaverage(r_values, tau):
        weights = np.repeat(1.0, tau) / tau
        sma = np.convolve(r_values, weights, 'valid')
        RMA = np.append(np.zeros((tau - 1,), dtype='float'), sma)
        return RMA, RMA[-1]

    @staticmethod
    def calc_next_gen(r0=4.9636, tau=14, C_t=70, C_o=0):
        return C_t * (1 + r0 / tau) ** tau - C_o * r0 / tau * (1 + r0 / tau) ** (tau - 1)

    def increasing_values(self, detected):
        tmp = [detected[0]]
        for t in range(1, self.periods_count):
            tmp.append(max(detected[t - 1], detected[t]))
        return tmp

    def calc_asymptomatic(self, fi, gamma):
        asymptomatic_infected = np.zeros(self.periods_count, dtype='float')

        for t in range(self.first_case + 1, self.periods_count):
            prev_detected, cur_detected = self.detected[t - 1], self.detected[t]
            asymptomatic_infected[t] = 1 / (1 - fi) * ((cur_detected - prev_detected) / gamma + prev_detected)
        return asymptomatic_infected


    def calc_r(self, values, tau):
        r_values = np.zeros(self.periods_count, dtype='float')

        for t in range(self.first_case + 1, self.first_case + tau + 1):
            r_values[t] = (values[t] / values[t - 1] - 1) * tau

        for t in range(self.first_case + tau + 1, self.periods_count):
            r_values[t] = (values[t] / (values[t - 1] - values[t - tau] + values[t - tau - 1]) - 1) * tau

        return self.movingaverage(r_values, tau)


    def predict(self, tau):
        for i in range(self.periods_count - tau, self.periods_count):
            self.detected = np.append(self.detected, self.calc_next_gen(r0=self.R0_D, tau=tau, C_t=self.detected[i], C_o=self.detected[i-tau]))
            self.asymptomatic_infected = np.append(self.asymptomatic_infected, self.calc_next_gen(r0=self.R0_C, tau=tau, C_t=self.asymptomatic_infected[i], C_o=self.asymptomatic_infected[i-tau]))


    def create_df(self, tau):
        periods  = self.periods_count + tau
        exposed = np.empty(periods)
        exposed[tau:] = self.asymptomatic_infected[:-tau]

        asymptomatic = self.asymptomatic_infected - self.detected
        return  pd.DataFrame({'Asymptomatic': asymptomatic, 'Infected': self.detected, 'Exposed': exposed},
                             index=pd.date_range(end=pd.to_datetime('today'),
                                                 periods=periods)).reset_index()


class CountryData:
    def __init__(self, country_file):
        self.filepath = country_file
        self.df = self.build_country_data()

    def build_country_data(self):
        country_df = pd.read_csv(self.filepath)
        # country_df = country_df.set_index('Country')
        country_df = country_df.drop(columns="Unnamed: 0")
        # country_df['date'] = country_df['date'].apply(lambda x: x if x.month<4 else x - relativedelta(years=1))
        country_df['date'] = pd.to_datetime(country_df['date'],format="%d/%m/%Y")
        return country_df
