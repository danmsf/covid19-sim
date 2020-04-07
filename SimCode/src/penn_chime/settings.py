#!/usr/bin/env python

from .defaults import Constants, Regions, RateLos
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.dirname(os.path.dirname(os.path.dirname(current_directory)))

delaware = 564696
chester = 519293
montgomery = 826075
bucks = 628341
philly = 1581000

DEFAULTS = Constants(
    # EDIT YOUR DEFAULTS HERE
    region=Regions(
        delaware=delaware,
        chester=chester,
        montgomery=montgomery,
        bucks=bucks,
        philly=philly,
    ),
    current_hospitalized=14,
    doubling_time=4,
    known_infected=510,
    n_days=60,
    market_share=0.15,
    relative_contact_rate=0.3,

    hospitalized=RateLos(0.025, 7),
    icu=RateLos(0.0075, 9),
    ventilated=RateLos(0.005, 10),

    olg_params={'tau': 14, 'init_infected': 100, 'fi': 0.25, 'theta': 0.0771, 'country': ['israel', 'canada'],
                'scenario': {'t': {0: 20},  'R0D': {0: 100}}},
    country_file=os.path.join(project_path, "Resources", "all_dates_n.csv"),
    stringency_file=os.path.join(project_path, "Resources", "OxCGRT_Download_latest_data.xlsx"),
    israel_file=os.path.join(project_path, "Resources", "Israel Corona Network Data Yishuv.xlsx"),
    sir_file=os.path.join(project_path, "Resources", "all_dates.csv"),
    sir_country_file=os.path.join(project_path, "Resources","SIR_COUNTRY.csv")
    # country_file=os.path.abspath(r"/../../Resources/all_dates_n.csv" + "/../../")
)
