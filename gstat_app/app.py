"""Main module for the streamlit app"""
import streamlit as st

import awesome_streamlit as ast
import src.pages.israel_data
import src.pages.country_data
import src.pages.projections
"""App."""
# streamlit run ./SimCode/src/app.py

import altair as alt  # type: ignore
import streamlit as st  # type: ignore
import pandas as pd
from penn_chime.utils import pivot_dataframe, get_table_download_link, get_repo_download_link

from penn_chime.presentation import(
    build_download_link,
    display_header,
    display_sidebar,
    draw_census_table,
    draw_projected_admissions_table,
    draw_raw_sir_simulation_table,
    hide_menu_style,
    show_additional_projections,
    show_more_info_about_this_tool,
    init_olg_params
)
from penn_chime.settings import DEFAULTS
from penn_chime.models import SimSirModel, OLG, Seiar, CountryData, SEIRSModel, IsraelData, StringencyIndex
from penn_chime.charts import (
    additional_projections_chart,
    admitted_patients_chart,
    new_admissions_chart,
    chart_descriptions,
    country_level_chart,
    yishuv_level_chart,
    test_results_chart,
    isolations_chart,
    test_symptoms_chart,
    test_indication_chart,
    patients_status_chart,
    jhopkins_level_chart,
    olg_projections_chart,
    country_comparison_chart
)

# This is somewhat dangerous:
# Hide the download_dfs menu with "Rerun", "run on Save", "clear cache", and "record a screencast"
# This should not be hidden in prod, but removed
# In dev, this should be shown
st.markdown(hide_menu_style, unsafe_allow_html=True)
st.markdown(
    """
    <div class="penn-medicine-header__content">
    <h1 id="title" class="penn-medicine-header__title" style="text-align:center">GSTAT Impact Model for Epidemics</h1>
    </div>
    """, unsafe_allow_html=True)

# st.write(
#     "# GSTAT Impact Tool for Epidemics  "
#     "[![GSTAT](https://github.com/gstat-gcloud/covid19-sim/raw/master/SimCode/src/gstat_logo.png)]"
#     "(https://g-stat.com)"
# )
# h="36px"
# w="36px"
st.sidebar.markdown(
    "[![GSTAT](https://github.com/gstat-gcloud/covid19-sim/raw/master/SimCode/src/gstat_logo.png)]"
    "(https://g-stat.com)"
)
st.markdown(
    """*This tool was developed to aid government in policy making. It enables rapid simulation of multiple models for 
    forecasting the effects of government policies on the spread of Covid-19 virus. Most models are framed in the SIR 
    Model framework.*"""
)

# Load all tables:
stringency_dummy = pd.DataFrame(data={'date': [pd.datetime.today()], 'StringencyIndex': [100]})

# TODO: update gov response source
st.sidebar.subheader("General parameters")
# TODO: add משרד המודיעין and GSTAT logo
# TODO: move table loading up here

ast.core.services.other.set_logging_format()

PAGES = {
    "Compare Countries Data": src.pages.country_data,
    "Show Israel Data": src.pages.israel_data,
    "Show Israel Projections": src.pages.projections,
}


def main():
    """Main function of the App"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)
    st.sidebar.title("Contribute")
    st.sidebar.info(
        "This an open source project and you are very welcome to **contribute** your awesome "
        "comments, questions, resources and apps as "
        "[issues](https://github.com/MarcSkovMadsen/awesome-streamlit/issues) of or "
        "[pull requests](https://github.com/MarcSkovMadsen/awesome-streamlit/pulls) "
        "to the [source code](https://github.com/MarcSkovMadsen/awesome-streamlit). "
    )
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This app is maintained by Marc Skov Madsen. You can learn more about me at
        [datamodelsanalytics.com](https://datamodelsanalytics.com).
"""
    )

    if st.sidebar.checkbox("About", False):
    st.sidebar.markdown("This app was developed in pure python utilizing the awesome [streamlit](https:\\streamlit.io) library.  "
                        "For other inspiring ideas see [Penn University Covid](https://penn-chime.phl.io) "
                        "or for more general applications [Awesome Streamlit](https://awesome-streamlit.org/)")
    st.sidebar.info("Thanks to everyone who volounteered to help develop and mantain this app, including (but not limited to):  "
            "Elisar Chodorov, "
            "Oz Mizrahi, "
            "Roy Assis, "
            "Dan Feldman, "
            "Ephraim Goldin, "
            "Annia Sorokin, "
            "Laura Lerner, and anyone else I missed :) ")


if __name__ == "__main__":
    main()
