"""Defaults."""
from typing import Dict, Any, Union

from .utils import RateLos
import datetime


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
            olg_params: Dict[str, int],

            as_date: bool = False,
            market_share: float = 1.0,
            max_y_axis: int = None,
            n_days: int = 60,
            recovery_days: int = 14,

            country_file: str,
            stringency_file: str,
            sir_file: str,
            sir_country_file: str,
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

        self.seiar_params = {'N_0': 8740000.00,
                             'S_0': 8739990.00,
                             'E_0': 0.0,
                             'A_0': 0.00,
                             'I_0': 10.00,
                             'R_0': 0.00,
                             'seiar_alpha': 0.2,
                             'seiar_beta_ill': 1.05,
                             'seiar_beta_asy': 1.05,
                             'seiar_gamma_ill': 0.08,
                             'seiar_gamma_asy': 0.15,
                             'seiar_rho': 1.0,
                             'seiar_theta': 0.8,
                             'seiar_start_date_simulation': datetime.date(2020, 3, 1),
                             'seiar_number_of_days': 30.00
                             }
        self.seirs_plus_params = {
            'beta': 0.155,
            'sigma': 1./4,
            'gamma': 1./14,
            'xi':0.0,
            'mu_I': 0.0,
            'mu_0':0.0,
            'nu': 0.0,
            'beta_D': 0.0,
            'sigma_D': 0.0,
            'gamma_D': 0.0,
            'mu_D': 0.0,
            'theta_E': 0.0,
            'theta_I': 0.0,
            'psi_E': 0.0,
            'psi_I': 0.0,
            'initN': 8740000.0,
            'initI': 10.0,
            'initE': 0.0,
            'initD_E': 0.0,
            'initD_I': 0.0,
            'initR': 0.0,
            'initF': 0.0,
        }
        self.model_chekpoints = {'t': [], 'beta': []}
        self.country_file = country_file
        self.stringency_file = stringency_file
        self.sir_file = sir_file
        self.sir_country_file = sir_country_file
        self.israel_file = israel_file
        self.country_file2 = country_file2

    def __repr__(self) -> str:
        return f"Constants(susceptible_default: {self.region.susceptible}, known_infected: {self.known_infected})"
