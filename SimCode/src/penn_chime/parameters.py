"""Parameters.

Changes affecting results or their presentation should also update
`change_date`, so users can see when results have last changed
"""

from .utils import RateLos, daily_hospitalized

class Parameters:
    """Parameters."""

    def __init__(
        self,
        *,
        current_hospitalized: int,
        doubling_time: float,
        known_infected: int,
        relative_contact_rate: float,
        susceptible: int,
        daily_hospitalized=daily_hospitalized,
        hospitalized: RateLos,
        icu: RateLos,
        ventilated: RateLos,

        tau: int = 8,
        cases: int = 100,
        as_date: bool = False,
        market_share: float = 1.0,
        max_y_axis: int = None,
        n_days: int = 60,
        recovery_days: int = 14,

        N_0: int = 7000000,
        S_0: float = 0,
        E_0: float = 0,
        I_0: float = 0,
        A_0: float = 0,
        R_0: float = 0,
        seiar_alpha: float = 0.0,
        seiar_beta_ill: float = 0.0,
        seiar_beta_asy: float = 0.0,
        seiar_gamma_ill: float = 0.0,
        seiar_gamma_asy: float = 0.0,
        seiar_rho: float = 0.0,
        seiar_theta: float = 0.0,
        seiar_start_date_simulation,
        seiar_number_of_days: int,

        seirs_plus_params,
        country_file: str
    ):
        self.current_hospitalized = current_hospitalized
        self.doubling_time = doubling_time
        self.known_infected = known_infected
        self.relative_contact_rate = relative_contact_rate
        self.susceptible = susceptible
        self.tau = tau
        self.cases = cases

        self.hospitalized = hospitalized
        self.icu = icu
        self.ventilated = ventilated
        self.daily_hospitalized = daily_hospitalized ##TODO change to np array\dict + added to declares

        self.as_date = as_date
        self.market_share = market_share
        self.max_y_axis = max_y_axis
        self.n_days = n_days
        self.recovery_days = recovery_days

        # Seiar
        self.N = N_0
        self.S_0 = S_0
        self.E_0 = E_0
        self.I_0 = I_0
        self.A_0 = A_0
        self.R_0 = R_0
        self.alpha = seiar_alpha
        self.beta_ill = seiar_beta_ill
        self.beta_asy = seiar_beta_asy
        self.gamma_ill = seiar_gamma_ill
        self.gamma_asy = seiar_gamma_asy
        self.rho = seiar_rho
        self.theta = seiar_theta
        self.start_date_simulation = seiar_start_date_simulation
        self.number_of_days = seiar_number_of_days

        self.seirs_plus_params = seirs_plus_params
        self.country_file = country_file
        self.labels = {
            "hospitalized": "Hospitalized",
            "icu": "ICU",
            "ventilated": "Ventilated",
            "day": "Day",
            "date": "Date",
            "susceptible": "Susceptible",
            "infected": "Infected",
            "recovered": "Recovered",
        }

        self.dispositions = {
            "hospitalized": hospitalized,
            "icu": icu,
            "ventilated": ventilated,
        }

    def change_date(self):
        """
        This reflects a date from which previously-run reports will no
        longer match current results, indicating when users should
        re-run their reports
        """
        return "March 23 2020"
