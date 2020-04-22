import streamlit as st
from seirsplus.models import SEIRSModel
import pandas as pd

def write():
    st.subheader("SEIRSPlus")
    seirs_params = p.seirs_plus_params
    model = SEIRSModel(**p.seirs_plus_params)
    p.model_checkpoints
    p.time_steps
    if p.model_checkpoints:
        model.run(T=p.time_steps, checkpoints=p.model_checkpoints)
    else:
        model.run(T=p.time_steps)

    # df = pd.DataFrame(
    #     {'S': model.numS, 'E': model.numE, 'I': model.numI, 'D_E': model.numD_E, 'D_I': model.numD_I, 'R': model.numR,
    #      'F': model.numF}, index=model.tseries)
    df = pd.DataFrame(
        {'E': model.numE, 'I': model.numI}, index=model.tseries)
    st.line_chart(df)

    model.figure_basic()
    st.markdown(
        """*Graph generated from `SEIRSPlus` package*"""
    )
    if st.checkbox(label="Model Parameters", value=False):
        st.markdown(
            """### Model Parameters"""
        )
        st.markdown(
            """

            Constructor Argument | Parameter Description | Data Type | Default Value
            -----|-----|-----|-----
            ```beta   ``` | rate of transmission | float | REQUIRED
            ```sigma  ``` | rate of progression | float | REQUIRED
            ```gamma  ``` | rate of recovery | float | REQUIRED
            ```xi     ``` | rate of re-susceptibility | float | 0
            ```mu_I   ``` | rate of infection-related mortality | float | 0
            ```mu_0   ``` | rate of baseline mortality | float | 0
            ```nu     ``` | rate of baseline birth | float | 0
            ```beta_D ``` | rate of transmission for detected cases | float | None (set equal to ```beta```)
            ```sigma_D``` | rate of progression for detected cases | float | None (set equal to ```sigma```)
            ```gamma_D``` | rate of recovery for detected cases | float | None (set equal to ```gamma```)
            ```mu_D   ``` | rate of infection-related mortality for detected cases | float | None (set equal to ```mu_I```)
            ```theta_E``` | rate of testing for exposed individuals | float | 0
            ```theta_I``` | rate of testing for infectious individuals | float | 0
            ```psi_E  ``` | probability of positive tests for exposed individuals | float | 0
            ```psi_I  ``` | probability of positive tests for infectious individuals | float | 0
            ```initN  ``` | initial total number of individuals | int | 10
            ```initI  ``` | initial number of infectious individuals | int | 10
            ```initE  ``` | initial number of exposed individuals | int | 0
            ```initD_E``` | initial number of detected exposed individuals | int | 0
            ```initD_I``` | initial number of detected infectious individuals | int | 0
            ```initR  ``` | initial number of recovered individuals | int | 0
            ```initF  ``` | initial number of deceased individuals | int | 0

            """
        )
    if st.checkbox(label="Detailed information on model", value=False):
        st.markdown(
            """
            <a href = https://github.com/ryansmcgee/seirsplus> Seirsplus </a>
            """, unsafe_allow_html=True
        )