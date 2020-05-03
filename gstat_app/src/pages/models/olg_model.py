import streamlit as st
from src.shared.models.model_olg import *
from src.shared.models.data import CountryData
from src.shared.charts.charts_olg import *
from src.shared.utils import get_table_download_link
import altair as alt
from src.shared.settings import DEFAULTS, load_data, user_session_id

def display_sidebar(olg_params):
        st.sidebar.subheader("GSTAT Model parameters")
        olg_params['tau'] = st.sidebar.number_input(
            "Tau rate (number of days infectious)",
            min_value=2,
            value=olg_params['tau'],
            step=1,
            format="%i",
        )

        olg_params['init_infected'] = st.sidebar.number_input(
            "Minimum cases for calculation",
            min_value=0,
            value=olg_params['init_infected'],
            step=10,
            format="%i",
        )

        olg_params['fi'] = st.sidebar.number_input(
            "Proportion of asymptomatic",
            min_value=0.01,
            value=olg_params['fi'],
            step=0.025,
            format="%f",
        )

        olg_params['theta'] = st.sidebar.number_input(
            "Daily diagnosis rate",
            min_value=0.0001,
            value=olg_params['theta'],
            step=0.01,
            format="%f",
        )

        olg_params['critical_condition_rate'] = st.sidebar.number_input(
            "Critical Condition Rate",
            min_value=0.0001,
            value=olg_params['critical_condition_rate'],
            step=0.0005,
            format="%f",
        )

        olg_params['recovery_rate'] = st.sidebar.number_input(
            "Recovery Rate",
            min_value=0.01,
            value=olg_params['recovery_rate'],
            step=0.025,
            format="%f",
        )

        olg_params['critical_condition_time'] = st.sidebar.number_input(
            "Critical Condition Time",
            min_value=1,
            value=olg_params['critical_condition_time'],
            step=1,
            format="%i",
        )

        olg_params['recovery_time'] = st.sidebar.number_input(
            "Recovery Time",
            min_value=1,
            value=olg_params['recovery_time'],
            step=1,
            format="%i",
        )

        return olg_params

def write():
    #-------------------Init Data and Params------------------
    olg_params = DEFAULTS['MODELS']['olg_params']
    sgidx = StringencyIndex("Israel")
    country_df, _, _, _, _, _, _ = load_data(DEFAULTS, user_session_id)
    # -------------------Sidebar logic-------------------------
    if st.sidebar.checkbox("Change Model Parameters", False):
        olg_params = display_sidebar(olg_params)

    p = OLGParameters(**olg_params)

    # Display Oxford Index
    st.sidebar.info(
        "We are currently updating the projection models, so changing the Oxford Index won't have any effect")
    sgidx.display_st(st)

    # -------------------Main Logic -----------------------------
    st.subheader("GSTAT Covid-19 Predictions for Israel")

    st.info("Models are based on *Natural and Unnatural Histories of Covid-19 Contagion * "
            "by Professor Michael Beenstock and Dai Xieer "
            "[download paper](https://cepr.org/sites/default/files/news/CovidEconomics10.pdf)")

    # Calculate Stringency
    sgidx.calculate_stringency()
    # sgidx_data = sgidx.output_df.copy()

    stringency = sgidx.output_df[['date', 'StringencyIndex']]

    p.countries = ['israel']
    olg = OLG(country_df, p, have_serious_data=True)
    dd = olg.df.copy()
    # ddd

    st.altair_chart(
        olg_projections_chart(alt, dd.loc[:, ['date', 'corona_days', 'country', 'prediction_ind',
                                              'StringencyIndex']].ffill(), "Stringency Index"),
        use_container_width=True,
    )
    # if st.checkbox("Download Stringency Calculation Data"):
    st.markdown(get_table_download_link(sgidx.output_df, "stringency"), unsafe_allow_html=True)

    olg_cols = dd.columns
    olg_cols = [c for c in olg_cols if c not in ['date', 'corona_days', 'country', 'r_values', 'prediction_ind']]
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

# temp = pread_csv('C:\\Users\\User\\PycharmProjects\\covad19-sim\\michaels_data.csv', parse_dates=['date'])
# temp['total_cases'] = temp['total_cases'].fillna(0).astype(int)
# temp['StringencyIndex'] = temp['StringencyIndex'].fillna(0).astype(float)
#
# p.countries = ['israel']
# olg = OLG(temp, p, temp[temp['country']=='hubei']['total_cases'].values, stringency, False)
# dd = olg.df.copy()
# st.altair_chart(
# olg_projections_chart(alt, dd[['date', 'corona_days', 'country', 'prediction_ind', 'R', 'r_predicted']],
#                           "Rate of Infection"),
#     use_container_width=True,
# )