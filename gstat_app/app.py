"""Main module for the streamlit app"""
# streamlit run ./gstat_app/src/app.py

import src.pages.israel_data
import src.pages.external_dashboards
import src.pages.country_data
import src.pages.projections
import src.pages.explain

import streamlit as st  # type: ignore
from src.shared.components import components
from src.shared.settings import hide_menu_style
from src.shared.utils import display_about
from src.shared.settings import DEFAULTS, load_data

# country_df, lab_tests, israel_yishuv_df, israel_patients, isolation_df = load_data(DEFAULTS)
# datasets_o = load_data(DEFAULTS)
# datasets = (i.copy() for i in datasets_o)
# This is somewhat dangerous:
# Hide the download_dfs menu with "Rerun", "run on Save", "clear cache", and "record a screencast"
# This should not be hidden in prod, but removed
# In dev, this should be shown
st.markdown(hide_menu_style, unsafe_allow_html=True)


st.sidebar.markdown(
    "[![GSTAT](https://github.com/gstat-gcloud/covid19-sim/raw/master/SimCode/src/gstat_logo.png)]"
    "(https://g-stat.com)"
)


# ast.core.services.other.set_logging_format()

PAGES = {
    "Home": src.pages.explain,
    "Compare Countries Data": src.pages.country_data,
    "World Dashboards": src.pages.external_dashboards,
    "Show Israel Data": src.pages.israel_data,
    "Show Israel Projections": src.pages.projections,
}


def main():
    """Main function of the App"""
    # st.sidebar.title("Navigation")
    st.sidebar.markdown("<h1 style='text-indent:0;margin-bottom:-0.5in;color:#2F5496;'>Navigation<h1>", unsafe_allow_html=True)
    selection = st.sidebar.radio("", list(PAGES.keys()), 0)
    if selection!='Home':
        st.markdown(
            """
            <div class="penn-medicine-header__content">
            <h1 id="title" class="penn-medicine-header__title" style="text-align:center">GSTAT Impact Model for Epidemics</h1>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(
            """*This tool was developed to aid government in policy making. It enables rapid simulation of multiple models for 
            forecasting the effects of government policies on the spread of Covid-19 virus. Most models are framed in the SIR 
            Model framework.*"""
        )
    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        components.write_page(page)

    st.sidebar.markdown("----------------")
    st.sidebar.markdown("<h2 style='text-indent:0in;color:#2F5496;'>About</h2>", unsafe_allow_html=True)
    display_about(st)


if __name__ == "__main__":
    main()
