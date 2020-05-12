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
    df_r = model.df.copy()
    # sgidx = StringencyIndexNaive("Israel")

    filters_dict = {'days_range': (1, 90),'stringency_range': (45., 90.)}
    # filters_dict['days_range'] = st.sidebar.slider("Choose Corona Days Forward for Policy Value", 1, 50, (1, 10))
    indices_dict = {'C1_School closing':None, 'C2_Workplace closing':None, 'C3_Cancel public events':None, 'C4_Restrictions on gatherings':None,
            'C5_Close public transport':None, 'C6_Stay at home requirements':None, 'C7_Restrictions on internal movement':None,
            'C8_International travel controls':None}
    indices_max = {'C1_School closing':3., 'C2_Workplace closing':3., 'C3_Cancel public events':2., 'C4_Restrictions on gatherings':4.,
            'C5_Close public transport':2., 'C6_Stay at home requirements':3., 'C7_Restrictions on internal movement':2.,
            'C8_International travel controls':4.}

    chose_options = ["Gstat Scenarios", "Choose by SringencyIndex Range", "Choose by SringencyIndex Values"]
    st.sidebar.subheader("Choose Comparison Method")
    chosen = st.sidebar.radio("", chose_options, 0)
    if chosen=="Choose by SringencyIndex Range":
        filters_dict = display_filtes(filters_dict)
        cond = ((df_r['corona_days'] - model.israel_day).between(*filters_dict['days_range'])) & \
               (df_r['StringencyIndexForDisplay'].between(*filters_dict['stringency_range']))
        countryList = list(df_r.loc[cond]['CountryName'].unique())
    elif chosen=="Choose by SringencyIndex Values":
        all_masks = []
        condition = (df_r['corona_days'] - model.israel_day).between(*filters_dict['days_range'])
        all_masks.append(condition)
        indices = st.sidebar.multiselect("Choose Index", list(indices_dict.keys()), ['C1_School closing'])
        for ix in indices:
            indices_dict[ix] = st.sidebar.number_input(ix, value=2.0, min_value=0.0, max_value=indices_max[ix], step=1.0)
            condition = (df_r[ix] == indices_dict[ix])
            all_masks.append(condition)
        mask = np.array(all_masks).all(axis=0)
        countryList = list(df_r.loc[mask]['CountryName'].unique())
    elif chosen=="Gstat Scenarios":
        st.subheader("Choose scenario")
        scenario = st.selectbox("", ["Pessimistic (Countries with second wave)", "Average", "Optimistic (Countries without second wave)"], 0)
        if scenario == "Pessimistic (Countries with second wave)":
            st.markdown("**Note:** Development of rate of infection in Israel will continue like in countries that "
                        "experienced a second wave (Hong Kong and Singapore).")
        if scenario == "Optimistic (Countries without second wave)":
            st.markdown("**Note:** Development of rate of infection in Israel will continue like in countries that did not "
                        "experienced a second wave (China, South Korea and Switzerland).")
        if scenario == "Average":
            st.markdown("**Note:** Development of rate of infection in Israel will continue as an average of multiple countries.")
        scenario_dict = {"Pessimistic (Countries with second wave)": ["Hong Kong", "Singapore"],
                         "Average": ["Hong Kong", "Singapore", "China", "South Korea", "Switzerland"],
                         "Optimistic (Countries without second wave)": ["China", "South Korea", "Switzerland"]}

        countryList = scenario_dict[scenario]


    pred = model.predict(countryList)
    dd = model.write(pred, olg_params['critical_condition_rate'], olg_params['recovery_rate'],  olg_params['critical_condition_time'], olg_params['recovery_time'])
    # critical_condition_rate, recovery_rate, critical_condition_time, recovery_time
    dd = dd.rename(columns={'Date': 'date', 'CountryName': 'country'})
    olg_cols = dd.columns
    print(olg_cols)
    olg_cols = [c for c in olg_cols if c not in ['date', 'corona_days', 'country', 'r_adjn', 'prediction_ind']]
    olg_cols = ['ConfirmedCases',  'ConfirmedCasesPred', 'ConfirmedDeaths', 'Total Deaths Predicted', 'StringencyIndex',
       'Total Detected', 'Currently Active Detected Predicted', 'New Detected Predicted', 'Daily Critical Predicted',
       'Total Recovery Predicted']
    olg_cols_select = st.multiselect('Select Prediction Columns', olg_cols, ['Daily Critical Predicted', 'New Detected Predicted'])

    st.altair_chart(
        olg_projections_chart(alt,
                              dd.loc[:, ['date', 'corona_days', 'country', 'prediction_ind'] + olg_cols_select],
                              "GSTAT Model Projections", False),
        use_container_width=True,
    )

    allCountries = list(df_r.loc[df_r['corona_days'] >= model.israel_day]['CountryName'].unique())
    countryList = st.multiselect("Select Countries for prediction", allCountries, countryList)

    # if st.checkbox("Plot Countries R", False):
        # st.write(df_r[df_r.CountryName.isin(countryList)])
    st.altair_chart(
        countries_rchart(alt, df_r[df_r.CountryName.isin(countryList)],
                              "Rate of Infection"),
        use_container_width=True,
    )
    if st.checkbox("Show Countries Data", False):
        st.write((df_r[df_r.CountryName.isin(countryList)]))


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
    last_updated = data['Date'].dt.date.max()
    st.markdown("*Source: Oxford University - Stringency Index Dataset*")
    st.markdown(f"*Last updated: {last_updated}*")
# if __name__ == "__main__":
#     write()
