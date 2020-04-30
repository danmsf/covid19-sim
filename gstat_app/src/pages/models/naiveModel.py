import streamlit as st
from src.shared.models.model_olg import OLGParameters, naiveModel
from src.pages.models.olg_model import display_sidebar as display_olg_params
from src.shared.charts.charts_olg import *
import altair as alt
from src.shared.utils import get_table_download_link
import pandas as pd
from src.shared.settings import DEFAULTS, load_stringency, user_session_id
import numpy as np
# from src.shared.models.data import CountryData
# from src.shared.settings import DEFAULTS, load_data, user_session_id

def display_filtes(filters_dict):
    filters_dict['days_range'] = st.sidebar.slider("Choose Corona Days Forward Range for Policy Value", 1, 20, (5, 10))
    filters_dict['stringency_range'] = st.sidebar.slider("Choose Stringency Range", 20., 100., (45., 90.))
    return filters_dict


def write():
    # pathfile = "C:\\Users\\User\\Downloads\\OxCGRT_Download_280420_162625_Full.csv"
    # data = pd.read_csv(pathfile, parse_dates=['Date'])
    data = load_stringency(DEFAULTS, user_session_id)
    olg_params = DEFAULTS['MODELS']['olg_params']
    if st.sidebar.checkbox("Change Model Parameters", False):
        olg_params = display_olg_params(olg_params)
    # -------------------Main Logic -----------------------------
    st.subheader("GSTAT Covid-19 Predictions for Israel")

    st.info("Models are based on *Natural and Unnatural Histories of Covid-19 Contagion * "
            "by Professor Michael Beenstock and Dai Xieer "
            "[download paper](https://github.com/gstat-gcloud/covid19-sim/raw/master/Resources/Natural_and_Unnatural_Histories_of_Covid19.pdf)")

    # naive_params = display_sidebar(naive_params)
    p = OLGParameters(**olg_params)
    model = naiveModel(data, p)
    filters_dict = {'days_range': (1, 10), 'stringency_range': (45., 90.)}
    filters_dict = display_filtes(filters_dict)
    df_r = model.df.copy()
    cond = ((df_r['corona_days'] - model.israel_day).between(*filters_dict['days_range'])) & \
           (df_r['StringencyIndexForDisplay'].between(*filters_dict['stringency_range']))

    allCountries = list(df_r.loc[df_r['corona_days'] > model.israel_day]['CountryName'].unique())
    countryList = list(df_r.loc[cond]['CountryName'].unique())
    countryList = st.multiselect("Select Countries for prediction", allCountries, countryList)
    if st.checkbox("Plot Countries R", False):
        # st.write(df_r[df_r.CountryName.isin(countryList)])
        st.altair_chart(
            countries_rchart(alt, df_r[df_r.CountryName.isin(countryList)],
                                  "Rate of Infection"),
            use_container_width=True,
        )

    pred = model.predict(countryList)
    dd = model.write(pred, olg_params['critical_condition_rate'], olg_params['recovery_rate'],  olg_params['critical_condition_time'], olg_params['recovery_time'])
    # critical_condition_rate, recovery_rate, critical_condition_time, recovery_time
    dd = dd.rename(columns={'Date': 'date', 'CountryName': 'country'})
    olg_cols = dd.columns
    olg_cols = [c for c in olg_cols if c not in ['date', 'corona_days', 'country', 'r_adjn', 'prediction_ind']]
    olg_cols_select = st.multiselect('Select Prediction Columns', olg_cols, ['Daily Critical Predicted'])

    st.altair_chart(
        olg_projections_chart(alt,
                              dd.loc[:, ['date', 'corona_days', 'country', 'prediction_ind'] + olg_cols_select],
                              "GSTAT Model Projections", False),
        use_container_width=True,
    )
    if st.checkbox("Show Projection Data", False):
        st.write(dd)
        st.markdown(get_table_download_link(dd, "gstat_prediciton"), unsafe_allow_html=True)

    st.altair_chart(
        olg_projections_chart(alt, dd[['date', 'corona_days', 'country', 'prediction_ind', 'R']],
                              "Rate of Infection"),
        use_container_width=True,
    )

    st.altair_chart(
        olg_projections_chart(alt, dd.loc[
            dd['corona_days'] > 2, ['date', 'corona_days', 'country', 'prediction_ind', 'Doubling Time']],
                              "Doubling Time"),
        use_container_width=True,
    )
    st.sidebar.markdown(get_table_download_link(data, "OxfordStringency"), unsafe_allow_html=True)

# if __name__ == "__main__":
#     write()
