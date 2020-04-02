#!/usr/bin/env python

from .defaults import Constants, Regions, RateLos
import os

current_directory = os.path.abspath(os.getcwd())
project_path = os.path.dirname(current_directory)

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

    olg_params={'tau': 8, 'init_infected': 100, 'fi': 0.1, 'gamma':0.0771},
    country_file=os.path.join(project_path,"Resources/all_dates_n.csv")
    # country_file=os.path.abspath(r"/../../Resources/all_dates_n.csv" + "/../../")
)
