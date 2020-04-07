"""Defaults."""
from typing import Dict, Any, Union

from .utils import RateLos

class Regions:
    """Arbitrary number of counties."""

    def __init__(self, **kwargs):
        susceptible = 0
        for key, value in kwargs.items ():
            setattr (self, key, value)
            susceptible += value
        self._susceptible = susceptible

    @property
    def susceptible(self):
        return self._susceptible


class Constants:


    def __init__(
            self,
            *,
            current_hospitalized: int,
            doubling_time: int,
            known_infected: int,
            relative_contact_rate: int,

            region: Regions,

            hospitalized: RateLos,
            icu: RateLos,
            ventilated: RateLos,
            olg_params: Dict[str, int] = {'tau': 8, 'init_infected': 100, 'fi': 0.1, 'theta':0.0771},
            seirs_plus_params: Dict,
            seiar_params: Dict,
            model_chekpoints: Dict,
            as_date: bool = False,
            market_share: float = 1.0,
            max_y_axis: int = None,
            n_days: int = 60,
            recovery_days: int = 14,

            country_file: str,
            stringency_file: str,
            sir_file: str,
            israel_file: str,
            country_file2: str,
    ):
        self.region = region
        self.current_hospitalized = current_hospitalized
        self.known_infected = known_infected
        self.doubling_time = doubling_time
        self.relative_contact_rate = relative_contact_rate

        self.olg_params = olg_params

        self.hospitalized = hospitalized
        self.icu = icu
        self.ventilated = ventilated

        self.as_date = as_date
        self.market_share = market_share
        self.max_y_axis = max_y_axis
        self.n_days = n_days
        self.recovery_days = recovery_days

        self.seiar_params = seiar_params
        self.seirs_plus_params = seirs_plus_params
        self.model_chekpoints = model_chekpoints
        self.country_file = country_file
        self.stringency_file = stringency_file
        self.sir_file = sir_file
        self.israel_file = israel_file
        self.country_file2 = country_file2

    def __repr__(self) -> str:
        return f"Constants(susceptible_default: {self.region.susceptible}, known_infected: {self.known_infected})"
