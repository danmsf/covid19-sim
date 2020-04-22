import streamlit as st
import src.pages.models.olg_model
import gstat_app.src as gst

MODELS = {
    "GSTAT Model": src.pages.models.olg_model,
    "SEAIRs Plus Model": src.pages.models.seirsplus,
}


def write():
    selection = st.sidebar.radio("Go to model", list(MODELS.keys()))
    # models_option = st.sidebar.multiselect(
    #     'Which models to show?',
    #     ['GSTAT Model'], ['GSTAT Model'])
    # # ('Penn Dashboard', 'GSTAT Model', 'SEIAR Model', 'SEIRSPlus'), )

    page = MODELS[selection]

    with st.spinner(f"Loading {selection} ..."):
        gst.shared.components.components.write_page(page)
