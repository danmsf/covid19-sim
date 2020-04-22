import streamlit as st

def write():
    st.subheader('Country Comparison Graphs')
    countrydata = CountryData(DEFAULTS.country_files)
    countrydata.get_country_data()
    countrydata.get_country_stringency()
    countrydata.get_sir()
    # 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered', 'activecases', 'serious_critical'
    countryname = st.multiselect("Select Countries", list(countrydata.country_df['Country'].sort_values().unique()), ['israel'])

    keepcols = ['Country', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
     'total_recovered', 'activecases', 'serious_critical',
     'tot_cases/1m_pop', 'deaths/1m_pop', 'date',
     'totaltests', 'tests/_1m_pop', 'tot_deaths/1m_pop',
     'population',  'StringencyIndexForDisplay', 'StringencyIndex']
    temp = countrydata.country_df.loc[countrydata.country_df.Country.isin(countryname), keepcols]
    temp = temp.set_index("date", drop=False)
    total_cases_criteria = st.number_input(label='Minimum Infected for Start', value=10)
    temp = temp.loc[temp['total_cases'] >= total_cases_criteria, :]
    cols = temp.columns
    cols = [c for c in cols if c not in ['Country', 'date']]
    col_measure = st.selectbox("Chose comparison column", cols, 0)
    caronadays = st.checkbox("Normalize x axis to start of Epidemic time", True)

    st.altair_chart(
        country_comparison_chart(alt, temp[['date', 'Country'] + [col_measure]],caronadays),
        use_container_width=True,
    )
    if st.checkbox(label="Show table", value=False):
        temp
        st.markdown(get_table_download_link(temp, "countrydata"), unsafe_allow_html=True)

    jh_hubei = countrydata.jh_confirmed_df.query('Province=="Hubei"')['value'].values
    pjh = init_olg_params(st, DEFAULTS)
    pjh.countries = countryname
    if len(pjh.countries) > 0:
        pjh.init_infected = total_cases_criteria
        olgjh = OLG(temp.rename(columns={"Country":"country"}), pjh, jh_hubei, stringency_dummy, False)
        ddjh = olgjh.df.copy()
        st.altair_chart(
            olg_projections_chart(alt, ddjh.loc[ddjh['prediction_ind'] == 0,
                                                ['date', 'corona_days', 'country', 'prediction_ind', 'R']],
                                  "Rate of Infection", caronadays),
            use_container_width=True,
        )

        st.altair_chart(
            olg_projections_chart(alt, ddjh.loc[
                (ddjh['corona_days'] > 2) & (ddjh['prediction_ind'] == 0),
                ['date', 'corona_days', 'country', 'prediction_ind', 'Doubling Time']], "Doubling Time", caronadays),
            use_container_width=True,
        )
    st.markdown("-------------------------------------------------")
    st.subheader('Country Oxford Stringency Level vs Corona Data')
    col_measures = st.multiselect("Chose columns", [c for c in cols if c not in ['StringencyIndex']],['total_cases'] , key=2)
    for c in countryname:
        st.altair_chart(
            country_level_chart(alt, temp.loc[temp.Country == c, ['Country', 'date', 'StringencyIndex'] + col_measures]),
            use_container_width=True,
        )
    st.markdown("""*Note: Oxford Stringency Index is a score from 0-100 rating the government restrictions due to Corona*""")

    st.markdown("""*Source: Worldmeter, Oxford University*""")
    # total_cases_criteria
    st.subheader("Johns Hopkins Data")
    jh_confirmed_df = countrydata.jh_confirmed_df.copy()
    jh_confirmed_df = jh_confirmed_df.loc[jh_confirmed_df['value'] >= total_cases_criteria, :]
    jh_confirmed_df['min_date'] = jh_confirmed_df.groupby(['Country', 'Province'])['variable'].transform('min')
    jh_confirmed_df['date'] = (jh_confirmed_df['variable'] - jh_confirmed_df['min_date']).dt.days
    jh_confirmed_df['country'] = jh_confirmed_df['Country'] + " - " + jh_confirmed_df['Province'].str.lower()
    province = st.multiselect("Select Country - Province", list(jh_confirmed_df.country.unique()), "Israel - all")
    #
    jh_confirmed_df = jh_confirmed_df.loc[jh_confirmed_df['country'].isin(province), :]
    st.altair_chart(
        jhopkins_level_chart(alt, jh_confirmed_df), use_container_width=True,
            )
    pjh.init_infected = 100
    jh_confirmed_df = countrydata.jh_confirmed_df.copy()
    jh_confirmed_df['date'] = jh_confirmed_df['variable']
    jh_confirmed_df = jh_confirmed_df.merge(
        countrydata.country_df.loc[:,['Country','date','StringencyIndex']],how='left',
    )
    jh_confirmed_df['country'] = jh_confirmed_df['Country'] + " - " + jh_confirmed_df['Province'].str.lower()
    temp = jh_confirmed_df.loc[jh_confirmed_df['country'].isin(province), :]
    temp = temp.rename(columns={'value' : 'total_cases'})
    # temp['Country'] = 'israel'
    #
    # temp['country'] = 'israel'
    # temp
    # temp['StringencyIndex'] = 100
    # olgjh = OLG(temp, pjh, jh_hubei, stringency_dummy, False)
    # ddjh = olgjh.df.copy()
    # st.altair_chart(
    #    olg_projections_chart(alt, ddjh.loc[ddjh['prediction_ind'] == 0, ['date', 'corona_days', 'country', 'prediction_ind', 'R']],
    #                          "Rate of Infection", caronadays),
    #     use_container_width=True,
    #  )

