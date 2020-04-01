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


class OLM:
    def __init__(self, p: Parameters):
        self.periods_count = len(p.daily_hospitalized)
        self.r_values = np.zeros(self.periods_count, dtype='float')
        self.procces(daily_hospitalized=p.daily_hospitalized, tau=p.tau, cases=p.cases)
        self.RMA = self.movingaverage(r_values=self.r_values, tau=p.tau)
        self.df = self.create_df()


    def procces(self, daily_hospitalized, tau, cases):

        b = np.zeros((self.periods_count,), dtype='int')
        b[0] = daily_hospitalized[0]

        for t in range(self.periods_count - 1):  # Increasing values only
            b[t + 1] = daily_hospitalized[t + 1] if daily_hospitalized[t + 1] > daily_hospitalized[t] else daily_hospitalized[t]

        first_case = np.argmax(b > cases)  # First case

        for t in range(first_case + 1, first_case + tau + 1):
            self.r_values[t] = (b[t] / b[t - 1] - 1) * tau

        for t in range(first_case + tau + 1, self.periods_count):
            self.r_values[t] = (b[t] / (b[t - 1] - b[t - tau] + b[t - tau - 1]) - 1) * tau


    def movingaverage(self, r_values, tau):
        weights = np.repeat(1.0, tau) / tau
        sma = np.convolve(r_values, weights, 'valid')
        RMA = np.append(np.zeros((tau - 1,), dtype='float'), sma)
        return RMA


    def create_df(self):
        return  pd.DataFrame({'RMA': self.RMA},
                              index=pd.date_range(end=pd.to_datetime('today'),
                                                  periods=self.periods_count)).reset_index()


    # for t=tau:T
    # RMA(t) = sum(R(t - tau + 1:t)) / tau;
    # end
