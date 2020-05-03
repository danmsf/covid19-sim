"""Main module for the streamlit app"""
# streamlit run ./gstat_app/src/app.py

import src.pages.israel_data
import src.pages.external_dashboards
import src.pages.country_data
import src.pages.projections
import src.pages.explain
import src.pages.users_guide
import src.pages.second_wave

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
    "Israel Predictive Models": src.pages.projections,
    "Israel Data Analytics": src.pages.israel_data,
    "Comparative Analytics by Countries": src.pages.country_data,
 }

# < button type = "button" class ="sidebar-collapse-control btn btn-outline-secondary" > < span class ="open-iconic" data-glyph="chevron-right" title="chevron-right" aria-hidden="true" > < / span > < / button >
def main():
    st.markdown(
    """
    <style> button[type="button"].sidebar-collapse-control.btn.btn-outline-secondary{color: white; background-color: green;}
    button[type="button"].sidebar-collapse-control.btn.btn-outline-secondary{
      visibility: hidden;
    }
    button[type="button"].sidebar-collapse-control.btn.btn-outline-secondary:after {
      content:'לחצו כאן'; 
      visibility: visible;
      display: block;
      position: absolute;
      background-color: green;
      padding: 5px;
      top: 2px;
      width: 90px
    }
    </style>
    """, unsafe_allow_html=True
    )
    # """Main function of the App"""
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


    st.sidebar.markdown("----------------")
    if selection != "Israel Predictive Models":
        st.sidebar.markdown("<h2 style='text-indent:0in;color:#2F5496;'>Blog</h2>", unsafe_allow_html=True)
        blog1 = st.sidebar.button("הוראות שימוש במערכת וחיזוי הגל שני בישראל - אפרים גולדין  מאי 2020", False)
        # blog2 = st.sidebar.button("בעיית חיזוי הגל שני בישראל - אפרים גולדין   מאי 2020", False)
        if blog1:
            components.write_page(src.pages.second_wave)
        # elif blog2:
        #    components.write_page(src.pages.second_wave)
        else:
            with st.spinner(f"Loading {selection} ..."):
                components.write_page(page)
    else:
        with st.spinner(f"Loading {selection} ..."):
            components.write_page(page)
    st.sidebar.markdown("<h2 style='text-indent:0in;color:#2F5496;'>About</h2>", unsafe_allow_html=True)
    display_about(st)


if __name__ == "__main__":
    main()
