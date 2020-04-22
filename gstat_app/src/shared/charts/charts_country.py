

@st.cache(allow_output_mutation=True)
def country_comparison_chart(alt, df: pd.DataFrame, caronadays=False):

    source = df.dropna()
    # source = source.reset_index()
    colnames = source.columns
    colnames = [c if c in ['date', 'Country'] else 'value' for c in colnames]
    source.columns = colnames
    if caronadays:
        source['date'] = pd.to_datetime(source['date'])
        source['min_date'] = source.groupby('Country')['date'].transform('min')
        source['date'] = source['date'] - source['min_date']
        source['date'] = source['date'].dt.days
        source.drop(columns='min_date', inplace=True)
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['date'], empty='none')

    line = alt.Chart(source).mark_line(interpolate='basis').encode(
        x='date',
        y='value',
        color=alt.Color('Country', legend=alt.Legend(orient="top", title='')),
    )
    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(source).mark_point().encode(
        x='date',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
        y = alt.Y('value', axis=alt.Axis(labels=False, title='', tickOpacity=0)),
    )
    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'value', alt.value(' ')),
        y=alt.Y('value', axis=alt.Axis(labels=True, title='', tickOpacity=0)),
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(source).mark_rule(color='gray').encode(
        x='date',
    ).transform_filter(
        nearest
    )

    # Put the five layers into a chart and bind the data

    return (alt.layer(
        line, selectors, rules, text
    ).properties(
        width=600, height=300, title="Country Comparison"
    ).interactive()
            )

@st.cache(allow_output_mutation=True)
def country_level_chart(alt, df: pd.DataFrame,):
    colnames = df.columns
    colnames = [c for c in colnames if c not in ['date', 'StringencyIndex', 'Country']]
    source = df.melt(id_vars=['date', 'Country'], value_vars=colnames).dropna()
    source = source.reset_index()
    source['value'] = source['value'].astype('int64')

    source['value'] = source['value'].astype('int64')

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['date'], empty='none')

    line = alt.Chart(source).mark_line(interpolate='basis').encode(
        x='date:T',
        y='value',
        color= alt.Color('variable', legend=alt.Legend(orient="top", title='')),
    )

    line2 = alt.Chart(df).mark_line(interpolate='basis', strokeDash=[1, 1]).encode(
        x='date:T',
        y='StringencyIndex'
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(source).mark_point().encode(
        x='date',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
        y = alt.Y('value', axis=alt.Axis(labels=False, title='', tickOpacity=0)),
    )
    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'value', alt.value(' ')),
        y=alt.Y('value', axis=alt.Axis(labels=False, title='', tickOpacity=0)),
    )

    text2 = line2.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'StringencyIndex', alt.value(' ')),
        y=alt.Y('StringencyIndex', axis=alt.Axis(labels=False, title='', tickOpacity=0)),
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(source).mark_rule(color='gray').encode(
        x='date',
    ).transform_filter(
        nearest
    )

    # Put the five layers into a chart and bind the data

    return (alt.layer(
        line, line2, selectors, rules, text, text2
    ).properties(
        width=600, height=300, title=df.Country[0]
    ).resolve_scale(y='independent').interactive()
            )

@st.cache(allow_output_mutation=True)
def jhopkins_level_chart(alt, df: pd.DataFrame,):
    # colnames = df.columns
    # colnames = [c for c in colnames if c not in ['date', 'StringencyIndex', 'Country']]
    # source = df.melt(id_vars=['date', 'Country'], value_vars=colnames).dropna()
    source = df
    source['value'] = source['value'].astype('int64')

    line = alt.Chart(source).transform_calculate(
        cat="datum.Country + '-' + datum.Province"
    ).mark_line(interpolate='basis', tooltip=True).encode(
            x=alt.X('date:Q', title='Corona Date'),
            y=alt.Y('value', title='Counts'),
            color=alt.Color('cat:N', title='Country-Region', legend=alt.Legend(orient="top", title=''))
        )

    return line.properties(
        width=600, height=300, title="Total Cases by Country-Region"
    ).resolve_scale(y='independent').interactive()

