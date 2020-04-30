import streamlit as st
import src.pages.models.olg_model
import src.pages.models.seirsplus
import src.pages.models.naiveModel

MODELS = {
    # "GSTAT Model (Beta Version)": src.pages.models.olg_model,
    "GSTAT Naive Model (Beta Version)": src.pages.models.naiveModel,
    "SEIRs Plus Model": src.pages.models.seirsplus,
    # "SEIAR Model" : src.pages.models.seair_model
}


def write():
    selection = st.sidebar.selectbox("Go to model", list(MODELS.keys()), 0)

    page = MODELS[selection]

    with st.spinner(f"Loading {selection} ..."):
        src.shared.components.components.write_page(page)
