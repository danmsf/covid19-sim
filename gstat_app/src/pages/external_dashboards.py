from src.shared.settings import DEFAULTS, load_data, user_session_id
import streamlit as st

def write():
    st.markdown("-----------------------------------------------------------------------------------------------")
    st.subheader("Johns Hopkins Dashboard")
    st.markdown(
        """
        <iframe src="https://coronavirus.jhu.edu/map.html" style="width: 120%; height: 600px; border: 0px none;"></iframe>
        """,
        unsafe_allow_html=True
    )

    st.markdown("--------------------------------------------------------------------")
    st.subheader('Our World in Data Graphs')
    st.subheader('Total Deaths')
    # https://ourworldindata.org/grapher/total-covid-deaths-per-million?year=2020-04-28&country=ISR
    st.markdown(
        """
        <iframe src="https://ourworldindata.org/grapher/total-covid-deaths-per-million" style="width: 100%; height: 600px; border: 0px none;"></iframe>
        """
        , unsafe_allow_html=True
    )
    st.subheader('Deaths Trajectory')
    st.markdown(
        """
    <iframe src="https://ourworldindata.org/grapher/covid-confirmed-daily-deaths-epidemiological-trajectory?country=ISR" style="width: 100%; height: 600px; border: 0px none;"></iframe>
        """, unsafe_allow_html=True
    )
    st.subheader('Test Amounts vs Confirmed Cases')
    # "https://ourworldindata.org/grapher/covid-19-tests-cases-scatter-with-comparisons?zoomToSelection=true&time=2020-01-22..2020-04-27&country=ISR"
    st.markdown(
        """
        <iframe src="https://ourworldindata.org/grapher/covid-19-tests-cases-scatter-with-comparisons?zoomToSelection=true&country=ISR" style="width: 100%; height: 600px; border: 0px none;"></iframe>
        """, unsafe_allow_html=True
    )
