"""Main module for the streamlit app"""

# import awesome_streamlit as ast
import src as gst
import src.pages.israel_data
import src.pages.country_data
import src.pages.projections
"""App."""
# streamlit run ./SimCode/src/app.py

import streamlit as st  # type: ignore

from penn_chime.presentation import hide_menu_style

from penn_chime.settings import DEFAULTS


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

# ast.core.services.other.set_logging_format()

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
        gst.shared.components.components.write_page(page)

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
