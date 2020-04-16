import numpy as np
import pandas as pd
import altair as alt
from statsmodels.tsa.api import SimpleExpSmoothing, Holt
from SimCode.src.penn_chime.models import CountryData, OLG
from penn_chime.settings import DEFAULTS


class Parameters:
    def __init__(self, tau, init_infected, fi, theta, scenario, countries, critical_condition_rate, recovery_rate,
                 critical_condition_time, recovery_time):
        self.tau = tau
        self.init_infected = init_infected
        self.fi = fi  # proportion of infectives are never diagnosed
        self.theta = theta  # diagnosis daily rate

        self.scenario = scenario
        self.countries = countries
        self.critical_condition_rate = critical_condition_rate
        self.recovery_rate = recovery_rate
        self.critical_condition_time = critical_condition_time
        self.recovery_time = recovery_time


scenario = {'t': {0: 20},
            'R0D': {0: 0}}  ## TODO t: == 20+

p = Parameters(tau=14,
               init_infected=100,
               fi=0.25,
               theta=0.0771,
               countries=['israel'],
               scenario=scenario,
               critical_condition_rate=0.05,
               recovery_rate=0.4,
               critical_condition_time=10,
               recovery_time=6
               )

countrydata = CountryData(DEFAULTS.country_files)
countrydata.country_df.drop('I', axis=1, inplace=True)
countrydata.country_df.rename(columns={'Country': 'country'}, inplace=True)

olg_model = OLG(countrydata.country_df, p)

olg_model.df.to_excel('new.xlsx', index=False)
