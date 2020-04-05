"""App."""

import altair as alt  # type: ignore
import streamlit as st  # type: ignore
import pandas as pd

from penn_chime.presentation import (
    build_download_link,
    display_header,
    display_sidebar,
    draw_census_table,
    draw_projected_admissions_table,
    draw_raw_sir_simulation_table,
    hide_menu_style,
    show_additional_projections,
    show_more_info_about_this_tool,
    write_definitions,
    write_footer,
)
from penn_chime.settings import DEFAULTS
from penn_chime.models import SimSirModel, OLG, Seiar, CountryData, SEIRSModel
from penn_chime.charts import (
    additional_projections_chart,
    admitted_patients_chart,
    new_admissions_chart,
    chart_descriptions,
    admission_rma_chart,
    country_level_chart
)

# This is somewhat dangerous:
# Hide the main menu with "Rerun", "run on Save", "clear cache", and "record a screencast"
# This should not be hidden in prod, but removed
# In dev, this should be shown
st.markdown(hide_menu_style, unsafe_allow_html=True)
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

st.sidebar.subheader("General parameters")

if st.sidebar.checkbox(label="Show country data"):

    countrydata = CountryData(DEFAULTS.country_file, DEFAULTS.stringency_file)
    countrydata.get_country_data()
    countrydata.get_country_stringency()
    # TODO: fix overlapping countries comparison option
    countryname = st.sidebar.multiselect(label="Select Countries", options=countrydata.df['Country'].unique())
    temp = countrydata.df.loc[countrydata.df.Country.isin(countryname), ['Country', 'date', 'New Cases', 'ActiveCases',
                                                                  'Serious_Critical', 'Total Cases', 'Total Recovered',
                                                                  'Total Deaths', 'StringencyIndex']]

    temp = temp.set_index("date", drop=False)

    if st.checkbox(label="Show Totals", value=False):
        temp = temp[['Total Cases', 'Total Recovered', 'Total Deaths', 'StringencyIndex', 'date']]
    else:
        temp = temp[['ActiveCases', 'New Cases', 'Serious_Critical', 'StringencyIndex', 'date']]
    if st.checkbox(label="Show table", value=False):
        temp
    else:
        st.altair_chart(
            country_level_chart(alt, temp),
            use_container_width=True,
        )
        # st.line_chart(temp)
        st.markdown("""*Source: Worldmeter*""")


models_option = st.sidebar.multiselect(
    'Which models to show?',
    ('Penn Dashboard', 'OLG Model', 'SEIAR Model', 'SEIRSPlus'), )

p = display_sidebar(st, DEFAULTS, models_option)


if "Penn Dashboard" in models_option:
    m = SimSirModel(p)
    display_header(st, m, p)
    if st.checkbox("Show more info about this tool"):
        notes = "The total size of the susceptible population will be the entire catchment area for Penn Medicine entities (HUP, PAH, PMC, CCH)"
        show_more_info_about_this_tool(st=st, model=m, parameters=p, defaults=DEFAULTS, notes=notes)

    st.subheader("New Admissions")
    st.markdown("Projected number of **daily** COVID-19 admissions at Penn hospitals")
    new_admit_chart = new_admissions_chart(alt, m.admits_df, parameters=p)
    st.altair_chart(
        new_admissions_chart(alt, m.admits_df, parameters=p),
        use_container_width=True,
    )

    st.markdown(chart_descriptions(new_admit_chart, p.labels))


    if st.checkbox("Show Projected Admissions in tabular form"):
        if st.checkbox("Show Daily Counts"):
            draw_projected_admissions_table(st, m.admits_df, p.labels, 1, as_date=p.as_date)
        else:
            admissions_day_range = st.slider(
                'Interval of Days for Projected Admissions',
                1, 10, 7
            )
            draw_projected_admissions_table(st, m.admits_df, p.labels, admissions_day_range, as_date=p.as_date)
        build_download_link(st,
            filename="projected_admissions.csv",
            df=m.admits_df,
            parameters=p
        )
    st.subheader("Admitted Patients (Census)")
    st.markdown(
        "Projected **census** of COVID-19 patients, accounting for arrivals and discharges at Penn hospitals"
    )
    census_chart = admitted_patients_chart(alt=alt, census=m.census_df, parameters=p)
    st.altair_chart(
        admitted_patients_chart(alt=alt, census=m.census_df, parameters=p),
        use_container_width=True,
    )
    st.markdown(chart_descriptions(census_chart, p.labels, suffix=" Census"))
    if st.checkbox("Show Projected Census in tabular form"):
        if st.checkbox("Show Daily Census Counts"):
            draw_census_table(st, m.census_df, p.labels, 1, as_date=p.as_date)
        else:
            census_day_range = st.slider(
                'Interval of Days for Projected Census',
                1, 10, 7
            )
            draw_census_table(st, m.census_df, p.labels, census_day_range, as_date=p.as_date)
        build_download_link(st,
            filename="projected_census.csv",
            df=m.census_df,
            parameters=p
        )

    st.markdown(
        """**Click the checkbox below to view additional data generated by this simulation**"""
    )
    if st.checkbox("Show Additional Projections"):
        show_additional_projections(
            st, alt, additional_projections_chart, model=m, parameters=p
        )
        if st.checkbox("Show Raw SIR Simulation Data"):
            draw_raw_sir_simulation_table(st, model=m, parameters=p)

if "OLG Model" in models_option:

    st.subheader("OLG Prediction")
    st.markdown("Projected number of **daily** COVID-19 admissions")
    olg = OLG (p)
    # new_admit_chart = new_admissions_chart(alt, m.admits_df, parameters=p)
    st.altair_chart(
        admission_rma_chart(alt, olg.df),
        use_container_width=True,
    )


# write_definitions(st)
# write_footer(st)

# SEIAR - Model
if "SEIAR Model" in models_option:
    st.subheader("SEIAR Model")

    mseiar = Seiar(p)
    mseiar.run_simulation()
    mseiar_results = mseiar.results.copy()

    if st.sidebar.checkbox(label="Plot as percentages", value=False):
        mseiar_results = mseiar_results/mseiar.N

    if st.sidebar.checkbox(label="Present result as dates instead of days ", value=False):
        mseiar_results = mseiar_results
    else:
        mseiar_results = mseiar_results.reset_index(drop=True)

    if st.checkbox(label="Present result as table", value=False):
        mseiar_results
    else:
        st.line_chart(mseiar_results)

if "SEIRSPlus" in models_option:
    st.subheader("SEIRSPlus")
    model = SEIRSModel(**p.seirs_plus_params)
    model.run(T=300)
    df = pd.DataFrame(
        {'S': model.numS, 'E': model.numE, 'I': model.numI, 'D_E': model.numD_E, 'D_I': model.numD_I, 'R': model.numR,
         'F': model.numF}, index=model.tseries)
    st.line_chart(df)
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
        # TODO: Fix images
        st.markdown(
            """
            <a href = https://github.com/ryansmcgee/seirsplus> Seirsplus </a>
            """, unsafe_allow_html=True
        )

