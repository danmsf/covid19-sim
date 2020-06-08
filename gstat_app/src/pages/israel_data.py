import streamlit as st
from src.shared.charts.charts_il import *
from src.shared.charts.charts_olg import olg_projections_chart
from src.shared.models.model_olg import *
from src.shared.models.data import IsraelData, CountryData
from src.shared.settings import DEFAULTS, load_data, user_session_id
import altair as alt


def write():
    country_df, _, lab_tests, israel_yishuv_df, israel_patients, isolation_df, tested_df = load_data(DEFAULTS, user_session_id)
    st.subheader('Israeli Data')

    st.subheader('Health Ministry Dashboard')
    st.markdown(
        """
        <iframe src="https://datadashboard.health.gov.il/COVID-19/" style="width: 100%; height: 1200px; border: 0px none;"></iframe>
        """, unsafe_allow_html=True
    )

    # Patients graph
    # patient_cols = ['New Patients Amount', 'Total Patients',
    #                 'Current Serious Condition Patients',
    #                 'Total Serious Condition Patients', 'New Dead Patients Amount',
    #                 'Total Dead Patients', 'Total Serious + Dead Patients',
    #                 'Lab Test Amount']
    # Not updated anymore
    # patient_cols = [c for c in list(israel_patients.columns) if c not in ['Date', 'תאריך']]
    # patient_cols_selected = st.multiselect("Select Patients Columns:", patient_cols,['מספר חולים במצב קשה'])
    # st.altair_chart(patients_status_chart(alt, israel_patients.loc[:, ['Date'] + patient_cols_selected]),
    #                 use_container_width=True)
    # last_updated = israel_patients['Date'].dt.date.max()
    # st.markdown(
    #     f"""
    #     <p style='text-align:right;'><i>הערה: הנתונים מעודכנים שבוע אחורה בהתאם למדיניות הפרסום של משרד הבריאות</i></p>
    #     <p style='text-align:right;'><i>תאריך נתונים אחרון: {last_updated}</i></p>
    #     """, unsafe_allow_html=True
    # )

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
    last_updated = country_df['date'].dt.date.max()
    st.markdown(f"*Last updated : {last_updated}*")
    st.markdown("-----------------------------")
    # Yishuvim charts
    st.subheader("Cases by City")
    # israel_yishuv_df = israel_yishuv_df.merge(
    #     country_df.loc[country_df['country'] == 'israel', ['date', 'StringencyIndex']], how='left')

    st.altair_chart(
        yishuv_bar_chart(alt, israel_yishuv_df.loc[(israel_yishuv_df['סוג מידע'] == 'last3days') &
                                                   (israel_yishuv_df['date'] == israel_yishuv_df['last_updated']) &
                                                    (israel_yishuv_df['value']>0),
                                                   ['Yishuv', 'value']].dropna())
        , use_container_width=True)
    st.markdown(f"*Last updated : {israel_yishuv_df['last_updated'].dt.date.values[-1]}*")
    st.markdown("-----------------------------")
    yishuvim = st.multiselect("Select City:", list(israel_yishuv_df['Yishuv'].unique()), 'בני ברק')
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
    df = pd.read_excel
    st.markdown("""*Source: Self collection & Ministry of Health*""")
    st.markdown(f"*Last updated : {israel_yishuv_df['last_updated'].dt.date.values[-1]}*")
    # st.markdown("**מפת יישובים**")
    # st.markdown(
    #     """
    #     <iframe src="https://www.govmap.gov.il/sites/coronamap.html" style="width: 100%; height: 600px; border: 0px none;"></iframe>
    #     """,
    #     unsafe_allow_html=True
    # )
        # st.markdown("*Note: Minimum 25 Cases for start out of outbreak*")
    st.markdown("-----------------------------")
    if st.checkbox("Show Additional Data", False):
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

