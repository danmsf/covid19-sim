#!/usr/bin/env python

from .defaults import Constants, Regions, RateLos
import datetime
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.dirname(os.path.dirname(os.path.dirname(current_directory)))
israel_data_path = os.path.join(project_path, "Resources", "Datasets", "IsraelData")
country_data_path = os.path.join(project_path, "Resources", "Datasets", "CountryData")

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

    olg_params={'tau': 14, 'init_infected': 100, 'fi': 0.25, 'theta': 0.0771,
                'country': ['israel', 'canada'],
                'scenario': {'t': {0: 10, 1: 10}, 'R0D': {0: 0, 1: -0.4}}},

    seirs_plus_params={
        'beta': 0.155,
        'sigma': 1. / 4,
        'gamma': 1. / 14,
        'xi': 0.0,
        'mu_I': 0.0,
        'mu_0': 0.0,
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
    },
    seiar_params={
        'N_0': 8740000.00,
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
    },
    model_chekpoints={'t': [], 'beta': []},
    country_file=os.path.join(project_path, "Resources", "all_dates.csv"),
    stringency_file=os.path.join(project_path, "Resources", "OxCGRT_Download_latest_data.xlsx"),
    israel_file=os.path.join(project_path, "Resources", "Israel Corona Network Data Yishuv.xlsx"),
    sir_file=os.path.join(project_path, "Resources", "all_dates.csv"),
    sir_country_file=os.path.join(project_path, "Resources", "SIR_COUNTRY.csv"),
    country_file2=os.path.join(project_path, "Resources", "all_dates_n.csv"),
    lab_results=os.path.join(project_path, "Resources", "Datasets", "IsraelData", "lab_tests.csv"),
    isolations=os.path.join(project_path, "Resources", "Datasets", "IsraelData", "isolations.csv"),
    israel_files={
        'yishuv_file': os.path.join(israel_data_path, "Israel Corona Network Data Yishuv.xlsx"),
        'lab_results_file': os.path.join(israel_data_path, "lab_tests.csv"),
        'isolations_file': os.path.join(israel_data_path, "isolations.csv"),
        'tested_file': os.path.join(israel_data_path, "corona_tested_individuals_ver_001.csv"),
    }
)
