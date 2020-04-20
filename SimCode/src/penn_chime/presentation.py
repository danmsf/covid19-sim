"""effectful functions for streamlit io"""

from typing import Optional

import altair as alt  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import datetime
from .defaults import Constants, RateLos
from .utils import add_date_column, dataframe_to_base64
from .parameters import Parameters, OLGParameters


DATE_FORMAT = "%b, %d"  # see https://strftime.org


hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """


########
# Text #
########
def init_olg_params(st, d: Constants) -> OLGParameters:

    return OLGParameters(
        tau=d.olg_params['tau'],
        init_infected=d.olg_params['init_infected'],
        fi=d.olg_params['fi'],
        theta=d.olg_params['theta'],
        countries=d.olg_params['countries'],
        scenario=d.olg_params['scenario'],
        critical_condition_rate=d.olg_params['critical_condition_rate'],
        recovery_rate=d.olg_params['recovery_rate'],
        critical_condition_time=d.olg_params['critical_condition_time'],
        recovery_time=d.olg_params['recovery_time'],
    )

def display_header(st, m, p):

    detection_prob_str = (
        "{detection_prob:.0%}".format(detection_prob=m.detection_probability)
        if m.detection_probability
        else "unknown"
    )
    # Logo and Title:
    st.markdown(
        """
<link rel="stylesheet" href="https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css">

<div class="penn-medicine-header__content">
    <a href="https://www.penn.com" class="penn-medicine-header__logo"
        title="Go to Penn">Penn Medicine</a>
    <a id="title" class="penn-medicine-header__title" style="text-align:center">Penn Medicine - COVID-19 Hospital Impact Model for Epidemics</p>
</div>
    """,
        unsafe_allow_html=True,
    )
    # Notice:
    # st.markdown(
    #     """**IMPORTANT NOTICE**: Admissions and Census calculations were previously **undercounting**. Please update your reports generated before """ + p.change_date() + """. See more about changes [here](https://github.com/CodeForPhilly/chime/labels/models)."""
    # )
    # Penn links:
    # st.markdown(
    #     """*This tool was developed by the [Predictive Healthcare team](http://predictivehealthcare.pennmedicine.org/) at
    # Penn Medicine. For questions on how to use this tool see the [User docs](https://code-for-philly.gitbook.io/chime/). Code can be found on [Github](https://github.com/CodeForPhilly/chime).
    # Join our [Slack channel](https://codeforphilly.org/chat?channel=covid19-chime-penn) if you would like to get involved!*"""
    # )

    st.markdown(
        """The estimated number of currently infected individuals is **{total_infections:.0f}**. The **{initial_infections}**
    confirmed cases in the region imply a **{detection_prob_str}** rate of detection. This is based on current inputs for
    Hospitalizations (**{current_hosp}**), Hospitalization rate (**{hosp_rate:.0%}**), Region size (**{S}**),
    and Hospital market share (**{market_share:.0%}**).

An initial doubling time of **{doubling_time}** days and a recovery time of **{recovery_days}** days imply an $R_0$ of
**{r_naught:.2f}**.

**Mitigation**: A **{relative_contact_rate:.0%}** reduction in social contact after the onset of the
outbreak **{impact_statement:s} {doubling_time_t:.1f}** days, implying an effective $R_t$ of **${r_t:.2f}$**.
""".format(
            total_infections=m.infected,
            initial_infections=p.known_infected,
            detection_prob_str=detection_prob_str,
            current_hosp=p.current_hospitalized,
            hosp_rate=p.hospitalized.rate,
            S=p.susceptible,
            market_share=p.market_share,
            recovery_days=p.recovery_days,
            r_naught=m.r_naught,
            doubling_time=p.doubling_time,
            relative_contact_rate=p.relative_contact_rate,
            r_t=m.r_t,
            doubling_time_t=abs(m.doubling_time_t),
            impact_statement=("halves the infections every" if m.r_t < 1 else "reduces the doubling time to")
        )
    )

    return None


def display_sidebar(st, d: Constants, models_option=None) -> Parameters:
    # Initialize variables
    # these functions create input elements and bind the values they are set to
    # to the variables they are set equal to
    # it's kindof like ember or angular if you are familiar with those

    n_days, current_hospitalized, doubling_time, relative_contact_rate, hospitalized_rate, icu_rate, ventilated_rate,\
    hospitalized_los, icu_los, ventilated_los, market_share, susceptible, known_infected, as_date, max_y_axis = \
        [d.n_days, d.current_hospitalized, d.doubling_time, d.relative_contact_rate, d.hospitalized.rate, d.icu.rate, d.ventilated.rate,
         d.hospitalized.length_of_stay, d.icu.length_of_stay, d.ventilated.length_of_stay, d.market_share, d.region.susceptible, d.known_infected, True, None]
    projection_path, time_steps = None, None

    if d.known_infected < 1:
            raise ValueError("Known cases must be larger than one to enable predictions.")
    if "Penn Dashboard" in models_option:
        init_beta, projection_path, time_steps = None, None, None
        n_days = st.sidebar.number_input(
            "Number of days to project",
            min_value=30,
            value=d.n_days,
            step=10,
            format="%i",
        )
        time_steps = n_days
        current_hospitalized = st.sidebar.number_input(
            "Currently Hospitalized COVID-19 Patients",
            min_value=0,
            value=d.current_hospitalized,
            step=1,
            format="%i",
        )

        doubling_time = st.sidebar.number_input(
            "Doubling time before social distancing (days)",
            min_value=0,
            value=d.doubling_time,
            step=1,
            format="%i",
        )

        relative_contact_rate = (
            st.sidebar.number_input(
                "Social distancing (% reduction in social contact)",
                min_value=0,
                max_value=100,
                value=int(d.relative_contact_rate * 100),
                step=5,
                format="%i",
            )
            / 100.0
        )

        hospitalized_rate = (
            st.sidebar.number_input(
                "Hospitalization %(total infections)",
                min_value=0.001,
                max_value=100.0,
                value=d.hospitalized.rate * 100,
                step=1.0,
                format="%f",
            )
            / 100.0
        )
        icu_rate = (
            st.sidebar.number_input(
                "ICU %(total infections)",
                min_value=0.0,
                max_value=100.0,
                value=d.icu.rate * 100,
                step=1.0,
                format="%f",
            )
            / 100.0
        )
        ventilated_rate = (
            st.sidebar.number_input(
                "Ventilated %(total infections)",
                min_value=0.0,
                max_value=100.0,
                value=d.ventilated.rate * 100,
                step=1.0,
                format="%f",
            )
            / 100.0
        )

        hospitalized_los = st.sidebar.number_input(
            "Hospital Length of Stay",
            min_value=0,
            value=d.hospitalized.length_of_stay,
            step=1,
            format="%i",
        )
        icu_los = st.sidebar.number_input(
            "ICU Length of Stay",
            min_value=0,
            value=d.icu.length_of_stay,
            step=1,
            format="%i",
        )
        ventilated_los = st.sidebar.number_input(
            "Vent Length of Stay",
            min_value=0,
            value=d.ventilated.length_of_stay,
            step=1,
            format="%i",
        )

        market_share = (
            st.sidebar.number_input(
                "Hospital Market Share (%)",
                min_value=0.001,
                max_value=100.0,
                value=d.market_share * 100,
                step=1.0,
                format="%f",
            )
            / 100.0
        )
        susceptible = st.sidebar.number_input(
            "Regional Population",
            min_value=1,
            value=d.region.susceptible,
            step=100000,
            format="%i",
        )

        known_infected = st.sidebar.number_input(
            "Currently Known Regional Infections (only used to compute detection rate - does not change projections)",
            min_value=0,
            value=d.known_infected,
            step=10,
            format="%i",
        )

        as_date = st.sidebar.checkbox(label="Present result as dates instead of days", value=False)

        max_y_axis_set = st.sidebar.checkbox("Set the Y-axis on graphs to a static value")
        max_y_axis = None
        if max_y_axis_set:
            max_y_axis = st.sidebar.number_input(
                "Y-axis static value", value=500, format="%i", step=25,
            )
    if "GSTAT Model" in models_option:
        st.sidebar.subheader("GSTAT Model parameters")
        d.olg_params['tau'] = st.sidebar.number_input(
            "Tau rate (number of days infectious)",
            min_value=2,
            value=d.olg_params['tau'],
            step=1,
            format="%i",
        )

        d.olg_params['init_infected'] = st.sidebar.number_input(
            "Minimum cases for calculation",
            min_value=0,
            value=d.olg_params['init_infected'],
            step=10,
            format="%i",
        )

        d.olg_params['fi'] = st.sidebar.number_input(
            "Proportion of asymptomatic",
            min_value=0.01,
            value=d.olg_params['fi'],
            step=0.025,
            format="%f",
        )

        d.olg_params['theta'] = st.sidebar.number_input(
            "Daily diagnosis rate",
            min_value=0.0001,
            value=d.olg_params['theta'],
            step=0.01,
            format="%f",
        )

        d.olg_params['critical_condition_rate'] = st.sidebar.number_input(
            "Critical Condition Rate",
            min_value=0.0001,
            value=d.olg_params['critical_condition_rate'],
            step=0.0005,
            format="%f",
        )

        d.olg_params['recovery_rate'] = st.sidebar.number_input(
            "Recovery Rate",
            min_value=0.01,
            value=d.olg_params['recovery_rate'],
            step=0.025,
            format="%f",
        )

        d.olg_params['critical_condition_time'] = st.sidebar.number_input(
            "Critical Condition Time",
            min_value=1,
            value=d.olg_params['critical_condition_time'],
            step=1,
            format="%i",
        )

        d.olg_params['recovery_time'] = st.sidebar.number_input(
            "Recovery Time",
            min_value=1,
            value=d.olg_params['recovery_time'],
            step=1,
            format="%i",
        )

        # if st.sidebar.checkbox ("Make a projection", value=False, key=10):
        #     s_times = st.sidebar.text_input('Insert array of times', value='10, 20', key=11)
        #     s_betas = st.sidebar.text_input('Insert percentage change in betas', value='0, 0', key=12)
        #     s_times = s_times.split(",")
        #     s_betas = s_betas.split(",")
        #     s_times = [int(s) for s in s_times]
        #     s_betas = [float(s) for s in s_betas]
        #
        #     d.olg_params['scenario'] = {'t': {k: v for k, v in enumerate(s_times)},
        #                                 'R0D': {k: v for k, v in enumerate(s_betas)}}


    if "SEIAR Model" in models_option:
        st.sidebar.subheader("SEAIR Model parameters")
        d.seiar_params['N_0'] = st.sidebar.number_input(
            "Population",
            min_value=1.,
            max_value=1000000000.0,
            value=d.seiar_params['N_0'],
            step=10.0,
            format="%f",
        )

        d.seiar_params['S_0'] = st.sidebar.number_input(
            "Susceptible",
            min_value=0.,
            max_value=d.seiar_params['N_0'],
            value=d.seiar_params['S_0'],
            step=10.,
            format="%f",
        )

        d.seiar_params['E_0'] = st.sidebar.number_input(
            "Exposed",
            min_value=0.,
            max_value=d.seiar_params['N_0'],
            value=d.seiar_params['E_0'],
            step=10.,
            format="%f",
        )

        d.seiar_params['A_0'] = st.sidebar.number_input(
            "Unknown Infected",
            min_value=0.,
            max_value=d.seiar_params['N_0'],
            value=d.seiar_params['A_0'],
            step=10.,
            format="%f",
        )

        d.seiar_params['I_0'] = st.sidebar.number_input(
            "Currently Known Ill ",
            min_value=0.,
            max_value=d.seiar_params['N_0'],
            value=d.seiar_params['I_0'],
            step=10.,
            format="%f",
        )

        d.seiar_params['R_0'] = st.sidebar.number_input(
            "Recovered",
            min_value=0.,
            max_value=d.seiar_params['N_0'],
            value=0.0,
            step=10.,
            format="%f",
        )

        d.seiar_params['seiar_alpha'] = st.sidebar.number_input(
            "seiar_alpha",
            min_value=0.0,
            max_value=100.0,
            value=d.seiar_params['seiar_alpha'],
            step=0.01,
            format="%f",
        )

        d.seiar_params['seiar_beta_ill'] = st.sidebar.number_input(
            "seiar_beta_ill",
            min_value=0.0,
            max_value=100.0,
            value=d.seiar_params['seiar_beta_ill'],
            step=0.01,
            format="%f",
        )

        d.seiar_params['seiar_beta_asy'] = st.sidebar.number_input(
            "seiar_beta_asy",
            min_value=0.0,
            max_value=100.0,
            value=d.seiar_params['seiar_beta_ill'],
            step=0.01,
            format="%f",
        )

        d.seiar_params['seiar_gamma_ill'] = st.sidebar.number_input(
            "seiar_gamma_ill",
            min_value=0.0,
            max_value=100.0,
            value=d.seiar_params['seiar_gamma_ill'],
            step=0.01,
            format="%f",
        )

        d.seiar_params['seiar_gamma_asy'] = st.sidebar.number_input(
            "seiar_gamma_asy",
            min_value=0.0,
            max_value=100.0,
            value=d.seiar_params['seiar_gamma_asy'],
            step=0.01,
            format="%f",
        )

        d.seiar_params['seiar_rho'] = st.sidebar.number_input(
            "seiar_rho",
            min_value=0.0,
            max_value=100.0,
            value=d.seiar_params['seiar_rho'],
            step=0.01,
            format="%f",
        )

        d.seiar_params['seiar_theta'] = st.sidebar.number_input(
            "seiar_theta",
            min_value=0.0,
            max_value=100.0,
            value=d.seiar_params['seiar_theta'],
            step=0.01,
            format="%f",
        )

        d.seiar_params['seiar_start_date_simulation'] = st.sidebar.date_input(
            "seiar_start_date_simulation",
            value=d.seiar_params['seiar_start_date_simulation']
        )

        d.seiar_params['seiar_number_of_days'] = st.sidebar.number_input(
            "seiar_number_of_days",
            min_value=0.0,
            max_value=1000.0,
            value=d.seiar_params['seiar_number_of_days'],
            step=1.0,
            format="%s",
        )
        if st.sidebar.checkbox ("Make a projection", value=False, key=14):
            time_steps = d.seiar_params['seiar_number_of_days']
            s_times1 = st.sidebar.text_input('Insert array of times for beta_ill', value='20, 50')
            s_betas1 = st.sidebar.text_input('Insert percentage change in beta_ill', value='0.2, 0.7')
            s_times2 = st.sidebar.text_input('Insert array of times for beta_asy', value='20, 50')
            s_betas2 = st.sidebar.text_input('Insert percentage change in beta_asy', value='0.2, 0.7')
            s_times1 = s_times1.split(",")
            s_betas1 = s_betas1.split(",")
            s_times1 = [int(s) for s in s_times1]
            s_betas1 = [float(s) for s in s_betas1]
            s_times2 = s_times2.split(",")
            s_betas2 = s_betas2.split(",")
            s_times2 = [int(s) for s in s_times2]
            s_betas2 = [float(s) for s in s_betas2]
            beta_t1 = d.seiar_params['seiar_beta_ill']
            beta_t2 = d.seiar_params['seiar_beta_asy']
            s_betas_p1 = []
            s_betas_p2 = []
            for s in s_betas1:
                beta_t1 = beta_t1 * (1 + s)
                s_betas_p1.append(beta_t1)
            for s in s_betas2:
                beta_t2 = beta_t2 * (1 + s)
                s_betas_p2.append(beta_t2)
            projection_path = {'time_ill': [], 'beta_ill': [], 'time_asy': [], 'beta_asy': []}
            projection_path['time_ill'] = s_times1
            projection_path['beta_ill'] = s_betas_p1
            projection_path['time_asy'] = s_times2
            projection_path['beta_asy'] = s_betas_p2
        else:
            projection_path, time_steps = {'time_ill': [], 'beta_ill': [], 'time_asy': [], 'beta_asy': []}, None

    if "SEIRSPlus" in models_option:
        for k, v in d.seirs_plus_params.items():
            if k.find('init')>-1:
                d.seirs_plus_params[k] = st.sidebar.number_input(
                k,
                min_value=0.0,
                max_value=100000000.0,
                value=v,
                step=10.0,
                format="%f")
            else:
                d.seirs_plus_params[k] = st.sidebar.number_input(
                k,
                min_value=0.0,
                max_value=100.0,
                value=v,
                step=0.01,
                format="%f")
        time_steps = st.sidebar.number_input("Days to project?", value=150, format="%i")
        if st.sidebar.checkbox ("Make a projection", value=False, key=15):

            s_times = st.sidebar.text_input('Insert array of times', value='20, 50', key=16)
            s_betas = st.sidebar.text_input('Insert percentage change in betas', value='0.2, 0.7', key=17)
            s_times = s_times.split(",")
            s_betas = s_betas.split(",")
            s_times = [int(s) for s in s_times]
            s_betas = [float(s) for s in s_betas]
            beta_t = d.seirs_plus_params['beta']
            s_betas_p = []
            for s in s_betas:
                beta_t = beta_t * (1 + s)
                s_betas_p.append(beta_t)
            projection_path = {'t': [], 'beta': []}
            projection_path['t'] = s_times
            projection_path['beta'] = s_betas_p
        else:
            projection_path = None


    return Parameters(
        as_date=as_date,
        current_hospitalized=current_hospitalized,
        doubling_time=doubling_time,
        known_infected=known_infected,
        market_share=market_share,
        max_y_axis=max_y_axis,
        n_days=n_days,
        relative_contact_rate=relative_contact_rate,
        susceptible=susceptible,
        tau=d.olg_params['tau'],
        init_infected=d.olg_params['init_infected'],
        fi=d.olg_params['fi'],
        theta=d.olg_params['theta'],
        countries=d.olg_params['countries'],
        scenario=d.olg_params['scenario'],
        critical_condition_rate=d.olg_params['critical_condition_rate'],
        recovery_rate=d.olg_params['recovery_rate'],
        critical_condition_time=d.olg_params['critical_condition_time'],
        recovery_time=d.olg_params['recovery_time'],

        hospitalized=RateLos(hospitalized_rate, hospitalized_los),
        icu=RateLos(icu_rate, icu_los),
        ventilated=RateLos(ventilated_rate, ventilated_los),

        # Seiar
        N_0 = d.seiar_params['N_0'],
        S_0 = d.seiar_params['S_0'],
        E_0 = d.seiar_params['E_0'],
        I_0 = d.seiar_params['I_0'],
        A_0 = d.seiar_params['A_0'],
        R_0 = d.seiar_params['R_0'],
        seiar_alpha = d.seiar_params['seiar_alpha'],
        seiar_beta_ill = d.seiar_params['seiar_beta_ill'],
        seiar_beta_asy = d.seiar_params['seiar_beta_asy'],
        seiar_gamma_ill = d.seiar_params['seiar_gamma_ill'],
        seiar_gamma_asy = d.seiar_params['seiar_gamma_asy'],
        seiar_rho = d.seiar_params['seiar_rho'],
        seiar_theta = d.seiar_params['seiar_theta'],
        seiar_start_date_simulation=d.seiar_params['seiar_start_date_simulation'],
        seiar_number_of_days = d.seiar_params['seiar_start_date_simulation'] + datetime.timedelta(d.seiar_params['seiar_number_of_days']),
        country_file=d.country_file,


        seirs_plus_params=d.seirs_plus_params,
        model_checkpoints=projection_path,
        time_steps=time_steps
        )


def show_more_info_about_this_tool(st, model, parameters, defaults, notes: str = ""):
    """a lot of streamlit writing to screen."""
    st.subheader(
        "[Discrete-time SIR modeling](https://mathworld.wolfram.com/SIRModel.html) of infections/recovery"
    )
    st.markdown(
        """The model consists of individuals who are either _Susceptible_ ($S$), _Infected_ ($I$), or _Recovered_ ($R$).

The epidemic proceeds via a growth and decline process. This is the core model of infectious disease spread and has been in use in epidemiology for many years."""
    )
    st.markdown("""The dynamics are given by the following 3 equations.""")

    st.latex("S_{t+1} = (-\\beta S_t I_t) + S_t")
    st.latex("I_{t+1} = (\\beta S_t I_t - \\gamma I_t) + I_t")
    st.latex("R_{t+1} = (\\gamma I_t) + R_t")

    st.markdown(
        """To project the expected impact to Penn Medicine, we estimate the terms of the model.

To do this, we use a combination of estimates from other locations, informed estimates based on logical reasoning, and best guesses from the American Hospital Association.


### Parameters

The model's parameters, $\\beta$ and $\\gamma$, determine the virulence of the epidemic.

$$\\beta$$ can be interpreted as the _effective contact rate_:
"""
    )
    st.latex("\\beta = \\tau \\times c")

    st.markdown(
        """which is the transmissibility ($\\tau$) multiplied by the average number of people exposed ($$c$$).  The transmissibility is the basic virulence of the pathogen.  The number of people exposed $c$ is the parameter that can be changed through social distancing.


$\\gamma$ is the inverse of the mean recovery time, in days.  I.e.: if $\\gamma = 1/{recovery_days}$, then the average infection will clear in {recovery_days} days.

An important descriptive parameter is the _basic reproduction number_, or $R_0$.  This represents the average number of people who will be infected by any given infected person.  When $R_0$ is greater than 1, it means that a disease will grow.  Higher $R_0$'s imply more rapid growth.  It is defined as """.format(
            recovery_days=int(parameters.recovery_days)
        )
    )
    st.latex("R_0 = \\beta /\\gamma")

    st.markdown(
        """

$R_0$ gets bigger when

- there are more contacts between people
- when the pathogen is more virulent
- when people have the pathogen for longer periods of time

A doubling time of {doubling_time} days and a recovery time of {recovery_days} days imply an $R_0$ of {r_naught:.2f}.

#### Effect of social distancing

After the beginning of the outbreak, actions to reduce social contact will lower the parameter $c$.  If this happens at
time $t$, then the number of people infected by any given infected person is $R_t$, which will be lower than $R_0$.

A {relative_contact_rate:.0%} reduction in social contact would increase the time it takes for the outbreak to double,
to {doubling_time_t:.2f} days from {doubling_time:.2f} days, with a $R_t$ of {r_t:.2f}.

#### Using the model

We need to express the two parameters $\\beta$ and $\\gamma$ in terms of quantities we can estimate.

- $\\gamma$:  the CDC is recommending 14 days of self-quarantine, we'll use $\\gamma = 1/{recovery_days}$.
- To estimate $$\\beta$$ directly, we'd need to know transmissibility and social contact rates.  since we don't know these things, we can extract it from known _doubling times_.  The AHA says to expect a doubling time $T_d$ of 7-10 days. That means an early-phase rate of growth can be computed by using the doubling time formula:
""".format(
            doubling_time=parameters.doubling_time,
            recovery_days=parameters.recovery_days,
            r_naught=model.r_naught,
            relative_contact_rate=parameters.relative_contact_rate,
            doubling_time_t=model.doubling_time_t,
            r_t=model.r_t,
        )
    )
    st.latex("g = 2^{1/T_d} - 1")

    st.markdown(
        """
- Since the rate of new infections in the SIR model is $g = \\beta S - \\gamma$, and we've already computed $\\gamma$, $\\beta$ becomes a function of the initial population size of susceptible individuals.
$$\\beta = (g + \\gamma)$$.


### Initial Conditions

- {notes} \n
""".format(
            notes=notes
        )
        + "- "
        + "| \n".join(
            f"{key} = {value} "
            for key, value in defaults.region.__dict__.items()
            if key != "_s"
        )
    )
    return None


def write_definitions(st):
    st.subheader("Guidance on Selecting Inputs")
    st.markdown(
        """**This information has been moved to the 
[User Documentation](https://code-for-philly.gitbook.io/chime/what-is-chime/parameters#guidance-on-selecting-inputs)**"""
    )


def write_footer(st):
    st.subheader("References & Acknowledgements")
    st.markdown(
        """* AHA Webinar, Feb 26, James Lawler, MD, an associate professor University of Nebraska Medical Center, What Healthcare Leaders Need To Know: Preparing for the COVID-19
* We would like to recognize the valuable assistance in consultation and review of model assumptions by Michael Z. Levy, PhD, Associate Professor of Epidemiology, Department of Biostatistics, Epidemiology and Informatics at the Perelman School of Medicine
    """
    )
    st.markdown("© 2020, The Trustees of the University of Pennsylvania")


def show_additional_projections(
    st, alt, charting_func, model, parameters
):
    st.subheader(
        "The number of infected and recovered individuals in the hospital catchment region at any given moment"
    )

    st.altair_chart(
        charting_func(
            alt,
            model=model,
            parameters=parameters
        ),
        use_container_width=True,
    )


##########
# Tables #
##########


def draw_projected_admissions_table(
    st, projection_admits: pd.DataFrame, labels, day_range, as_date: bool = False
):
    admits_table = projection_admits[np.mod(projection_admits.index, day_range) == 0].copy()
    admits_table["day"] = admits_table.index
    admits_table.index = range(admits_table.shape[0])
    admits_table = admits_table.fillna(0).astype(int)

    if as_date:
        admits_table = add_date_column(
            admits_table, drop_day_column=True, date_format=DATE_FORMAT
        )
    admits_table.rename(labels)
    st.table(admits_table)
    return None


def draw_census_table(st, census_df: pd.DataFrame, labels, day_range, as_date: bool = False):
    census_table = census_df[np.mod(census_df.index, day_range) == 0].copy()
    census_table.index = range(census_table.shape[0])
    census_table.loc[0, :] = 0
    census_table = census_table.dropna().astype(int)

    if as_date:
        census_table = add_date_column(
            census_table, drop_day_column=True, date_format=DATE_FORMAT
        )

    census_table.rename(labels)
    st.table(census_table)
    return None


def draw_raw_sir_simulation_table(st, model, parameters):
    as_date = parameters.as_date
    projection_area = model.raw_df
    infect_table = (projection_area.iloc[::7, :]).apply(np.floor)
    infect_table.index = range(infect_table.shape[0])
    infect_table["day"] = infect_table.day.astype(int)

    if as_date:
        infect_table = add_date_column(
            infect_table, drop_day_column=True, date_format=DATE_FORMAT
        )

    st.table(infect_table)
    build_download_link(st,
        filename="raw_sir_simulation_data.csv",
        df=projection_area,
        parameters=parameters
    )

def build_download_link(st, filename: str, df: pd.DataFrame, parameters: Parameters):
    if parameters.as_date:
        df = add_date_column(df, drop_day_column=True, date_format="%Y-%m-%d")

    csv = dataframe_to_base64(df)
    st.markdown("""
        <a download="{filename}" href="data:file/csv;base64,{csv}">Download full table as CSV</a>
""".format(csv=csv,filename=filename), unsafe_allow_html=True)




