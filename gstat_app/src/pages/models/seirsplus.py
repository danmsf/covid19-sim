import streamlit as st
from seirsplus.models import SEIRSModel
import pandas as pd
from src.shared.settings import DEFAULTS


class SEIRSParamaters():
    def __init__(self, *,
                 seirs_plus_params,
                 model_checkpoints,
                 time_steps: int):
        self.seirs_plus_params = seirs_plus_params
        self.model_checkpoints = model_checkpoints
        self.time_steps = time_steps

def display_sidebar(st, d):
    seirs_plus_params = d['seirs_plus_params']
    print(seirs_plus_params)
    for k, v in seirs_plus_params.items():
        if k.find('init') > -1:
            seirs_plus_params[k] = st.sidebar.number_input(
                k,
                min_value=0.0,
                max_value=100000000.0,
                value=v,
                step=10.0,
                format="%f")
        else:
            seirs_plus_params[k] = st.sidebar.number_input(
                k,
                min_value=0.0,
                max_value=100.0,
                value=v,
                step=0.01,
                format="%f")

    time_steps = st.sidebar.number_input("Days to project?", value=150, format="%i")
    if st.sidebar.checkbox("Make a projection", value=False, key=15):

        s_times = st.sidebar.text_input('Insert array of times', value='20, 50', key=16)
        s_betas = st.sidebar.text_input('Insert percentage change in betas', value='0.2, 0.7', key=17)
        s_times = s_times.split(",")
        s_betas = s_betas.split(",")
        s_times = [int(s) for s in s_times]
        s_betas = [float(s) for s in s_betas]
        beta_t = seirs_plus_params['beta']
        s_betas_p = []
        for s in s_betas:
            beta_t = beta_t * (1 + s)
            s_betas_p.append(beta_t)
        projection_path = {'t': [], 'beta': []}
        projection_path['t'] = s_times
        projection_path['beta'] = s_betas_p
    else:
        projection_path = None
    return SEIRSParamaters(seirs_plus_params=seirs_plus_params, model_checkpoints=projection_path, time_steps=time_steps)


def write(datasets):
    # -------------------Sidebar logic-------------------------
    seirs_plus = DEFAULTS['MODELS']['seirs_plus']
    p = SEIRSParamaters(**seirs_plus)
    if st.sidebar.checkbox("Change Model Parameters", False):
        p = display_sidebar(st, seirs_plus)

    st.subheader("SEIRs Plus")


    model = SEIRSModel(**p.seirs_plus_params)
    # st.write(p.model_checkpoints)
    # st.write(p.time_steps)
    if p.model_checkpoints:
        model.run(T=p.time_steps, checkpoints=p.model_checkpoints)
    else:
        model.run(T=p.time_steps)

    df = pd.DataFrame(
        {'S': model.numS, 'E': model.numE, 'I': model.numI, 'D_E': model.numD_E, 'D_I': model.numD_I, 'R': model.numR,
         'F': model.numF}, index=model.tseries)

    cols = st.multiselect("Choose columns:", list(df.columns), list(df.columns))
    if st.checkbox("Percent", True):
        print(model.N)
        df = df/model.N[0]
    st.line_chart(df[cols])

    st.markdown(
    "*Model generated from [SEIRs Plus](https://github.com/ryansmcgee/seirsplus) package*"
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
    st.markdown(
    """
    <img src="https://github.com/ryansmcgee/seirsplus/raw/master/images/SEIRStesting_diagram.png" alt="drawing" width="550" />
    """
    , unsafe_allow_html=True)