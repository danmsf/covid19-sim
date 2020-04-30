import yaml
import os
from src.shared.models.data import *
import streamlit as st
from .utils import get_session_id, fancy_cache
import datetime

current_directory = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.dirname(os.path.dirname(os.path.dirname(current_directory)))
project_path = os.getcwd()
defaults_file = os.path.join(project_path, "gstat_app/src/shared/defaults.yaml")

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """

with open(defaults_file) as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    DEFAULTS = yaml.load(file, Loader=yaml.FullLoader)

user_session_id = get_session_id()
print(user_session_id)

@st.cache(ttl=20, show_spinner=False , persist=True, max_entries=3)
def load_data(DEFAULTS,user_session_id):
    print(user_session_id, datetime.datetime.now())
    with open('./logs/session_ids.csv', 'a') as fd:
        fd.write(str(user_session_id) + ",")
        fd.write(str(datetime.datetime.now())+"\n")
    israel_data = IsraelData(DEFAULTS['FILES']['israel_files'])

    # Load data
    countrydata = CountryData(DEFAULTS['FILES']['country_files'])
    countrydata.get_country_data()
    country_df = countrydata.country_df.copy()
    lab_tests = israel_data.lab_results_df.copy()
    israel_data.get_yishuv_data()
    israel_yishuv_df = israel_data.yishuv_df.copy()
    israel_patients = israel_data.patients_df.copy()
    isolation_df = israel_data.isolation_df.copy()
    tested_df = israel_data.tested_df.copy()
    jh_confirmed_df = countrydata.jh_confirmed_df
    return country_df, jh_confirmed_df, lab_tests, israel_yishuv_df, israel_patients, isolation_df, tested_df

@st.cache(ttl=20, show_spinner=False , persist=True, max_entries=3)
def load_stringency(DEFAULTS,user_session_id):
    countrydata = CountryData(DEFAULTS['FILES']['country_files'])
    stringency_df = countrydata.get_stringency()
    return stringency_df

# datasets = load_data(DEFAULTS)
