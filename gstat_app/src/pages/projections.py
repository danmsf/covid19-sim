import streamlit as st
import src.pages.models.olg_model

MODELS = {
    "GSTAT Model": src.pages.models.olg_model,
    "SEAIRs Plus Model": src.pages.models.seirsplus,
}

def write():
    selection = st.sidebar.radio("Go to model", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)