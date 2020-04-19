"""App."""

import altair as alt  # type: ignore
import streamlit as st  # type: ignore
import pandas as pd
from penn_chime.utils import pivot_dataframe

from penn_chime.presentation import(
    build_download_link,
    display_header,
    display_sidebar,
    draw_census_table,
    draw_projected_admissions_table,
    draw_raw_sir_simulation_table,
    hide_menu_style,
    show_additional_projections,
    show_more_info_about_this_tool
)
from penn_chime.settings import DEFAULTS
from penn_chime.models import SimSirModel, OLG, Seiar, CountryData, SEIRSModel, IsraelData, StringencyIndex
from penn_chime.charts import (
    additional_projections_chart,
    admitted_patients_chart,
    new_admissions_chart,
    chart_descriptions,
    country_level_chart,
    yishuv_level_chart,
    test_results_chart,
    isolations_chart,
    test_symptoms_chart,
    test_indication_chart,
    patients_status_chart,
    jhopkins_level_chart,
    olg_projections_chart
)

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

st.markdown(
    """*This tool was developed to aid government in policy making. It enables rapid simulation of multiple models for 
    forecasting the effects of government policies on the spread of Covid-19 virus. Most models are framed in the SIR 
    Model framework.*"""
)

st.sidebar.subheader("General parameters")
# TODO: Michaels models by city/country
# TODO: Michaels model for S effect
# TODO: get rid of S
# TODO: add calendar days
# TODO: add משרד המודיעין and GSTAT logo
if st.sidebar.checkbox(label="Compare Countries Corona Data"):
    st.header('Country Data')
    countrydata = CountryData(DEFAULTS.country_files)
    countrydata.get_country_data()
    countrydata.get_country_stringency()
    countrydata.get_sir()
    # 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered', 'activecases', 'serious_critical'
    countryname = st.multiselect("Select Countries", list(countrydata.country_df['Country'].sort_values().unique()), ['israel'])
    # d = countrydata.country_df
    # d
    temp = countrydata.country_df.loc[countrydata.country_df.Country.isin(countryname), ['Country', 'date', 'total_cases', 'new_cases',
                                                                         'total_deaths', 'new_deaths',
                                                                         'total_recovered', 'activecases',
                                                                         'serious_critical', 'StringencyIndex']]
    # TODO: Add per million columns
    # min_infected = st.sidebar.number_input("Minimum Infected for graphs", value=10)
    # temp = temp.loc[temp['Total Cases'] >= min_infected, :]

    temp = temp.set_index("date", drop=False)
    total_cases_criteria = st.number_input(label='Minimum Infected for Start', value=10)
    temp = temp.loc[temp['total_cases'] >= total_cases_criteria, :]
    cols = temp.columns
    cols = [c for c in cols if c not in ['Country', 'date']]
    col_measure = st.selectbox("Chose comparison column", cols, 0)
    st.line_chart(pivot_dataframe(temp, col_measure, countryname, normalize_day=int(total_cases_criteria)))
    if st.checkbox(label="Show table", value=False):
        temp
    else:
        col_measures = st.multiselect("Chose columns", [c for c in cols if c not in ['StringencyIndex']],['total_cases'] , key=2)
        for c in countryname:
            st.altair_chart(
                country_level_chart(alt, temp.loc[temp.Country == c, ['Country', 'date', 'StringencyIndex'] + col_measures]),
                use_container_width=True,
            )
        st.markdown("""*Note: Oxford Stringency Index is a score from 0-100 rating the government restrictions due to Corona*""")

        st.markdown("""*Source: Worldmeter*""")
    # total_cases_criteria
    st.subheader("Johns Hopkins Data")
    jh_confirmed_df = countrydata.jh_confirmed_df.copy()
    # TODO: Add: Contagion rate (R) estimates by countries ; Doubling time by countries - graph instead of this... move to top
    jh_confirmed_df = jh_confirmed_df.loc[jh_confirmed_df['value'] >= total_cases_criteria, :]
    jh_confirmed_df['min_date'] = jh_confirmed_df.groupby(['Country', 'Province'])['variable'].transform('min')
    jh_confirmed_df['date'] = (jh_confirmed_df['variable'] - jh_confirmed_df['min_date']).dt.days
    jh_confirmed_df['country'] = jh_confirmed_df['Country'] + " - " + jh_confirmed_df['Province'].str.lower()
    province = st.multiselect("Select Country - Province", list(jh_confirmed_df.country.unique()), "Israel - all")

    jh_confirmed_df = jh_confirmed_df.loc[jh_confirmed_df['country'].isin(province), :]
    st.altair_chart(
        jhopkins_level_chart(alt, jh_confirmed_df), use_container_width=True,
            )

if st.sidebar.checkbox(label="Show Israel data"):
    # TODO: Move yishuvim to top
    # TODO: remove stingency index from yishuvim
    # TODO: Add ISRAEL R and yishuvim R
    # TODO: Add doubling rate by yishuvim
    st.header('Israeli Data')
    israel_data = IsraelData(DEFAULTS.israel_files)

    # Load data
    countrydata = CountryData(DEFAULTS.country_files)
    country_df = countrydata.get_country_data()
    lab_tests = israel_data.lab_results_df.copy()
    israel_data.get_yishuv_data()
    israel_yishuv_df = israel_data.yishuv_df.copy()
    israel_patients = israel_data.patients_df.copy()
    isolation_df = israel_data.isolation_df.copy()

    # Patients graph
    patient_cols = ['New Patients Amount', 'Total Patients',
                    'Current Serious Condition Patients',
                    'Total Serious Condition Patients', 'New Dead Patients Amount',
                    'Total Dead Patients', 'Total Serious + Dead Patients',
                    'Lab Test Amount']
    patient_cols_selected = st.multiselect("Select Patients Columns:", patient_cols, ['Current Serious Condition Patients'])
    israel_patients = israel_patients.loc[:, ['Date'] + patient_cols_selected]
    st.altair_chart(patients_status_chart(alt, israel_patients), use_container_width=True)
    st.markdown("""*Source: Self collection*""")
    # Isolation chart
    st.altair_chart(isolations_chart(alt, isolation_df), use_container_width=True)
    st.markdown("""*Source: Israel Ministry of Health*""")

    # Test charts
    if st.checkbox("Show as percentage", False, key=1):
        st.altair_chart(test_results_chart(alt, lab_tests,'normalize'), use_container_width=True)
    else:
        st.altair_chart(test_results_chart(alt, lab_tests), use_container_width=True)
    st.markdown("""*Source: Israel Ministry of Health*""")

    # st.altair_chart(test_indication_chart(alt, israel_data.tested_df), use_container_width=False)
    if st.checkbox("Show as percentage", True, key=2):
        st.altair_chart(test_symptoms_chart(alt, israel_data.tested_df, drill_down=False), use_container_width=False)
    else:
        st.altair_chart(test_symptoms_chart(alt, israel_data.tested_df, drill_down=False, stacked='zero'), use_container_width=False)
    if st.checkbox("Drill down symptoms by date", value=False):
        st.altair_chart(test_symptoms_chart(alt, israel_data.tested_df, drill_down=True), use_container_width=False)
    st.markdown("""*Source: Israel Ministry of Health*""")
    # Yishuvim charts
    st.subheader("Cases by Yishuv")
    israel_yishuv_df = israel_yishuv_df.merge(
        country_df.loc[country_df['Country'] == 'israel', ['date', 'StringencyIndex']], how='left')

    yishuvim = st.multiselect("Select Yishuv:", list(israel_yishuv_df['Yishuv'].unique()), 'בני ברק')
    colvars = list(israel_yishuv_df['סוג מידע'].unique())
    sel_vars = st.selectbox("Select Variable: ", colvars, 0)
    israel_yishuv_df = israel_yishuv_df.loc[(israel_yishuv_df['Yishuv'].isin(yishuvim) &
                                             israel_yishuv_df['סוג מידע'].isin([sel_vars])), :]
    if st.checkbox("Show per 1,000 inhabitants", True):
        st.altair_chart(yishuv_level_chart(alt, israel_yishuv_df), use_container_width=True)
    else:
        st.altair_chart(yishuv_level_chart(alt, israel_yishuv_df, by_pop=False), use_container_width=True)
    st.markdown("""*Source: Self collection*""")

if st.sidebar.checkbox("Show Israel Projections", False):
    models_option = st.sidebar.multiselect(
        'Which models to show?',
        ['OLG Model'])
        # ('Penn Dashboard', 'OLG Model', 'SEIAR Model', 'SEIRSPlus'), )

    countrydata = CountryData(DEFAULTS.country_files)
    countrydata.country_df.drop('I', axis=1, inplace=True)
    countrydata.country_df.rename(columns={'Country': 'country'}, inplace=True)

    country_dict = {'countries_list': set(countrydata.country_df['country'].values)}
    DEFAULTS.olg_params.update(country_dict)

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
        # TODO: Change OLG Model to GSTAT Model
        st.subheader("GSTAT Covid-19 Predictions for Israel")
        # Load model

        jh_hubei = countrydata.jh_confirmed_df.query('Province=="Hubei"')['value'].values
        country_df = countrydata.country_df.copy()
        # p.countries = st.multiselect('Select countries',  list(country_df['country'].unique()), 'israel')
        # if len(p.countries) == 0:
        p.countries = ['israel']
        olg = OLG(country_df, p, jh_hubei)
        dd = olg.df.copy()
        # dd
        olg_cols = dd.columns
        olg_cols = [c for c in olg_cols if c not in ['date', 'corona_days', 'country', 'r_values', 'R', 'Doubling Time', 'prediction_ind']]
        olg_cols_select = st.multiselect('Select OLG Columns', olg_cols, ['Critical_condition'])

        st.altair_chart(
            olg_projections_chart(alt, dd.loc[:, ['date', 'corona_days', 'country', 'prediction_ind'] + olg_cols_select], "OLG Projections", False),
            use_container_width=True,
        )
        if st.checkbox("Show Projection Data", False):
            dd

        st.altair_chart(
            olg_projections_chart(alt, dd[['date', 'corona_days', 'country', 'prediction_ind', 'R']], "Rate of Infection"),
            use_container_width=True,
        )
        # st.altair_chart(
        #     olg_projections_chart(alt, dd[['date', 'corona_days', 'country', 'prediction_ind', 'crystal_ball']], "crystal_ball"),
        #     use_container_width=True,
        # )
        st.altair_chart(
            olg_projections_chart(alt, dd.loc[dd['corona_days'] > 2, ['date', 'corona_days', 'country', 'prediction_ind', 'Doubling Time']], "Doubling Time"),
            use_container_width=True,
        )
        # st.line_chart(dd.loc[])
        st.altair_chart(
            olg_projections_chart(alt, dd.loc[:, ['date', 'corona_days', 'country', 'prediction_ind',
                                                                  'StringencyIndex']].ffill(), "Stringency Index"),
            use_container_width=True,
        )

        st.subheader("Projection for Israeli Yishuvim")
        israel_data = IsraelData(DEFAULTS.israel_files)
        israel_yishuv_df = israel_data.yishuv_df.copy()
        israel_yishuv_df = israel_yishuv_df.merge(
            dd.loc[dd['country'] == 'israel', ['date', 'StringencyIndex']], how='left')
        israel_yishuv_df = israel_yishuv_df.loc[israel_yishuv_df['סוג מידע']=='מספר חולים מאומתים',:]
        israel_yishuv_df = israel_yishuv_df.rename(columns={'value':'total_cases', 'Yishuv':'country'})
        pil = p
        pil.countries = st.multiselect("Select Yishuv", list(israel_yishuv_df.country.unique()))
        if len(pil.countries) > 0:
            pil.init_infected = st.number_input("Select min corona cases for Yishuv", min_value=10, value=25)
            olgil = OLG(israel_yishuv_df, pil, jh_hubei, False)
            ddil = olgil.df.copy()
            # ddil
            st.altair_chart(
                olg_projections_chart(alt, ddil.loc[ddil['prediction_ind']==0,['date', 'corona_days', 'country', 'prediction_ind', 'R']], "Rate of Infection"),
                use_container_width=True,
            )
            st.markdown("*Note: In this model treatment does not vary by Yishuv*")

        st.subheader("Projection using Johns Hopkins Data")
        countrydata = CountryData(DEFAULTS.country_files)
        jh_confirmed_df = countrydata.jh_confirmed_df.copy()
        jh_confirmed_df = jh_confirmed_df.rename(columns={'Country': 'country', 'variable': 'date', 'value': 'total_cases'})
        jh_confirmed_df['country'] = jh_confirmed_df['country'].str.lower()
        country_df = countrydata.country_df.copy()
        country_df = country_df.rename(columns={'Country': 'country'})
        jh_confirmed_df = jh_confirmed_df.merge(
            country_df.loc[:, ['country', 'date', 'StringencyIndex']], how='left')
        jh_confirmed_df['country'] = jh_confirmed_df['country'] + " - " + jh_confirmed_df['Province'].str.lower()
        pjh = p
        pjh.countries = st.multiselect("Select Country - Province", list(jh_confirmed_df.country.unique()))
        # jh_confirmed_df.loc[jh_confirmed_df['country'].isin(pjh.countries), :]
        if len(pjh.countries) > 0:
            pjh.init_infected = st.number_input("Select min corona cases for Province", min_value=10, value=100)
            olgjh = OLG(jh_confirmed_df, pjh, jh_hubei, False)
            ddjh = olgjh.df.copy()
            st.altair_chart(
                olg_projections_chart(alt, ddjh.loc[ddjh['prediction_ind']==0 ,
                                        ['date', 'corona_days', 'country', 'prediction_ind', 'R']], "Rate of Infection"),
                use_container_width=True,
            )
            if st.checkbox("Show Countries Data", False):
                ddjh.loc[ddjh['prediction_ind'] == 0, :]

        st.subheader("Calculate Oxford StringencyIndex")
        sgidx = StringencyIndex("Israel")
        sgidx.display_st(st)
        sgidx.calculate_stringency()
        sgidx_data = sgidx.output_df.copy()
        sgidx_data
        sgidx_data.to_csv("stringencyExample.csv")


    if "SEIAR Model" in models_option:
        st.subheader("SEIAR Model")

        mseiar = Seiar(p)
        mseiar.run_simulation()
        mseiar_results = mseiar.results.copy()
        p.model_checkpoints
        if st.sidebar.checkbox(label="Plot as percentages", value=False):
            mseiar_results = mseiar_results/mseiar.N

        if st.sidebar.checkbox(label="Present result as dates instead of days ", value=False):
            mseiar_results = mseiar_results
        else:
            mseiar_results = mseiar_results.reset_index(drop=True)

        if st.checkbox(label="Present result as table", value=False):
            mseiar_results
        else:
            st.line_chart(mseiar_results[['Asymptomatic', 'Infected']])

    if "SEIRSPlus" in models_option:
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
            # TODO: Fix images
            st.markdown(
                """
                <a href = https://github.com/ryansmcgee/seirsplus> Seirsplus </a>
                """, unsafe_allow_html=True
            )

