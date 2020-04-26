import streamlit as st
from src.shared.charts.charts_il import *
from src.shared.charts.charts_olg import olg_projections_chart
from src.shared.models.model_olg import *
from src.shared.models.data import IsraelData, CountryData
from src.shared.settings import DEFAULTS, load_data
import altair as alt


def write():
    country_df, _, lab_tests, israel_yishuv_df, israel_patients, isolation_df, tested_df = load_data(DEFAULTS)
    st.subheader('Israeli Data')

    # Patients graph
    patient_cols = ['New Patients Amount', 'Total Patients',
                    'Current Serious Condition Patients',
                    'Total Serious Condition Patients', 'New Dead Patients Amount',
                    'Total Dead Patients', 'Total Serious + Dead Patients',
                    'Lab Test Amount']
    patient_cols_selected = st.multiselect("Select Patients Columns:", patient_cols, ['Current Serious Condition Patients'])
    israel_patients = israel_patients.loc[:, ['Date'] + patient_cols_selected]
    st.altair_chart(patients_status_chart(alt, israel_patients), use_container_width=True)

    pil = init_olg_params(DEFAULTS['MODELS']['olg_params'])
    pil.countries = ['israel']
    pil.init_infected = 100
    olgil = OLG(country_df, pil, have_serious_data=False)
    ddil = olgil.df.copy()

    # coronadays = st.checkbox("Show axis as number of days since outbreak", True)
    st.altair_chart(
        olg_projections_chart(alt, ddil.loc[
            ddil['prediction_ind'] == 0, ['date', 'corona_days', 'country', 'prediction_ind', 'R']],
                              "Rate of Infection", False),
        use_container_width=True,
    )

    st.altair_chart(
        olg_projections_chart(alt, ddil.loc[
            (ddil['corona_days'] > 2) & (ddil['prediction_ind'] == 0),
            ['date', 'corona_days', 'country', 'prediction_ind', 'Doubling Time']], "Doubling Time", False),
        use_container_width=True,
    )

    st.markdown("""*Source: Self collection*""")
    st.markdown("-----------------------------")
    # Yishuvim charts
    st.subheader("Cases by Yishuv")
    israel_yishuv_df = israel_yishuv_df.merge(
        country_df.loc[country_df['country'] == 'israel', ['date', 'StringencyIndex']], how='left')

    yishuvim = st.multiselect("Select Yishuv:", list(israel_yishuv_df['Yishuv'].unique()), 'בני ברק')
    colvars = list(israel_yishuv_df['סוג מידע'].unique())
    sel_vars = st.selectbox("Select Variable: ", colvars, 0)
    israel_yishuv_olg_df = israel_yishuv_df.loc[israel_yishuv_df['סוג מידע'] == 'מספר חולים מאומתים', :].copy()
    israel_yishuv_df_plot = israel_yishuv_df.loc[(israel_yishuv_df['Yishuv'].isin(yishuvim) &
                                             israel_yishuv_df['סוג מידע'].isin([sel_vars])), :].copy()
    if st.checkbox("Show per 1,000 inhabitants", True):
        st.altair_chart(yishuv_level_chart(alt, israel_yishuv_df_plot), use_container_width=True)
    else:
        st.altair_chart(yishuv_level_chart(alt, israel_yishuv_df_plot, by_pop=False), use_container_width=True)

    israel_yishuv_olg_df = israel_yishuv_olg_df.rename(columns={'value': 'total_cases', 'Yishuv': 'country'})

    pil = init_olg_params(DEFAULTS['MODELS']['olg_params'])
    pil.countries = yishuvim
    if len(pil.countries) > 0:
        # pil.init_infected = st.number_input("Select min corona cases for Yishuv", min_value=10, value=25)
        pil.init_infected = 25
        olgil = OLG(israel_yishuv_olg_df, pil, have_serious_data=False)
        ddil = olgil.df.copy()
        # coronadays = st.checkbox("Show axis as number of days since outbreak", True)
        st.altair_chart(
            olg_projections_chart(alt, ddil.loc[
                ddil['prediction_ind'] == 0, ['date', 'corona_days', 'country', 'prediction_ind', 'R']],
                                  "Rate of Infection", False),
            use_container_width=True,
        )

        st.altair_chart(
            olg_projections_chart(alt, ddil.loc[
                (ddil['corona_days'] > 2) & (ddil['prediction_ind'] == 0),
                ['date', 'corona_days', 'country', 'prediction_ind', 'Doubling Time']], "Doubling Time", False),
            use_container_width=True,
        )
        # st.markdown("*Note: Minimum 25 Cases for start out of outbreak*")
    st.markdown("""*Source: Self collection*""")
    st.markdown("-----------------------------")
    st.subheader('Ministry of Health Data')
    # Isolation chart
    st.altair_chart(isolations_chart(alt, isolation_df), use_container_width=True)
    st.markdown("""*Source: Israel Ministry of Health*""")
    st.markdown("-----------------------------")
    # Test charts
    if st.checkbox("Show as percentage", False, key=1):
        st.altair_chart(test_results_chart(alt, lab_tests, 'normalize'), use_container_width=True)
    else:
        st.altair_chart(test_results_chart(alt, lab_tests), use_container_width=True)
    st.markdown("""*Source: Israel Ministry of Health*""")
    st.markdown("-----------------------------")
    # st.altair_chart(test_indication_chart(alt, israel_data.tested_df), use_container_width=False)
    if st.checkbox("Show as percentage", True, key=2):
        st.altair_chart(test_symptoms_chart(alt, tested_df, drill_down=False), use_container_width=False)
    else:
        st.altair_chart(test_symptoms_chart(alt, tested_df, drill_down=False, stacked='zero'), use_container_width=False)
    if st.checkbox("Drill down symptoms by date", value=False):
        st.altair_chart(test_symptoms_chart(alt, tested_df, drill_down=True), use_container_width=False)
    st.markdown("""*Source: Israel Ministry of Health*""")

