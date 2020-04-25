from altair import Chart  # type: ignore
import pandas as pd  # type: ignore
import streamlit as st



# @st.cache(allow_output_mutation=True)
def isolations_chart(alt, df: pd.DataFrame, stacked='zero'):
    isolations = df.melt(id_vars='date', value_vars=df.columns[1:]).dropna()
    return alt.Chart(isolations).mark_area(tooltip=True, line=True).encode(alt.X('date', title='Isolation Date'),
                                                                           alt.Y('value', title='Count', stack=stacked),
                                                               color=alt.Color('variable',  legend=alt.Legend(orient="top", title=''))).properties(
        width=600, height=300, title="Isolation"
    ).interactive()

# @st.cache(allow_output_mutation=True)
def test_symptoms_chart(alt, df: pd.DataFrame, drill_down=True, stacked='normalize'):

    symptoms = df.copy()
    symptoms = symptoms.drop(columns=['age_60_and_above', 'gender'])
    sym_cols = symptoms.columns
    sym_cols = [c for c in sym_cols if c not in ['test_date', 'corona_result', 'test_indication']]
    symptoms = symptoms.melt(id_vars=['test_date', 'test_indication', 'corona_result'], value_vars=sym_cols).dropna()
    agg_data = symptoms.groupby(['test_date', 'corona_result', 'test_indication', 'variable'], as_index=False).sum()
    # agg_data = agg_data.loc[agg_data['corona_result'] != 'אחר', :]
    area = alt.Chart(agg_data).mark_area(tooltip=True, line=True).\
        encode(x=alt.X('test_date', title=None, axis=alt.Axis(labels=True)),
               y=alt.Y('value', title=None, stack=stacked),
               color=alt.Color('corona_result', title='', legend=alt.Legend(orient="top", title='')),
               column=alt.Column('test_indication', header=alt.Header(labelOrient='top'), title='Test Indication'),
               row=alt.Row('variable', title='Symptom')).\
        properties(
        width=200, height=150, title="Symptoms vs Test Indication by Date"
    ).interactive()
    agg_data = symptoms.groupby(['corona_result', 'test_indication', 'variable'], as_index=False)['value'].sum()
    bar = alt.Chart(agg_data).mark_bar(tooltip=True, line=True).\
        encode(x=alt.X('test_indication', title=None, axis=alt.Axis(labels=True, labelAngle=0, orient="top")),
               y=alt.Y('value', title=None, stack=stacked),
               color=alt.Color('corona_result', title='', legend=alt.Legend(orient="top", title='')),
               # column=alt.Column('test_indication', header=alt.Header(labelOrient='top'), title='Test Indication'),
               row=alt.Row('variable', title='Symptom')).\
        properties(
        width=600, height=150, title="Symptoms vs Test Indication"
    ).interactive()

    if drill_down:
        return area
    else:
        return bar

# @st.cache(allow_output_mutation=True)
def test_indication_chart(alt, df: pd.DataFrame,):

    agg_data = df.groupby(['test_date', 'corona_result', 'test_indication'], as_index=False).size().reset_index(name='counts')
    agg_data = agg_data.loc[agg_data['corona_result'] != 'אחר', :]
    line1 = alt.Chart(agg_data).mark_area(tooltip=True, line=True).\
        encode(x=alt.X('test_date', title='Test Date'),
               y=alt.Y('counts', title=None, stack="normalize"),
               color=alt.Color('corona_result', title='', legend=alt.Legend(orient="top", title='')),
               row=alt.Row('test_indication', title='Result')). \
        configure_view(
        stroke='transparent'
    ).properties(
        width=600, height=300, title="Test Indication"
    ).interactive()

    # bar1 = alt.Chart(agg_data).mark_bar(tooltip=True).\
    #     encode(x=alt.X('test_indication', title=None, axis=alt.Axis(labels=False), scale=alt.Scale(rangeStep=8)),
    #            y=alt.Y('value_pct', title=None),
    #            color=alt.Color('test_indication', title='', legend=alt.Legend(orient="top", title='')),
    #            column=alt.Column('test_date', header=alt.Header(labelOrient='bottom'), title=None),
    #            row=alt.Row('corona_result', title='Result')). \
    #     configure_view(
    #     stroke='transparent'
    # ).properties(
    #     width=50, height=300, title="Test Indication"
    # ).interactive()
    return line1

# @st.cache(allow_output_mutation=True)
def patients_status_chart(alt, df: pd.DataFrame,):
    patients = df.melt(id_vars='Date', value_vars=df.columns[1:]).dropna()
    line = alt.Chart(patients).mark_line(interpolate='basis', point=False, tooltip=True).encode(
        x='Date:T',
        y=alt.Y('value', title="Counts"),
        color=alt.Color('variable', title=None, legend=alt.Legend(orient="top", title='')),
    )
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['Date'], empty='none')
    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(patients).mark_point().encode(
        x='Date:T',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'value', alt.value(' ')),
        y=alt.Y('value', axis=alt.Axis(labels=True, title='', tickOpacity=0)),
    )
    # Draw a rule at the location of the selection
    rules = alt.Chart(patients).mark_rule(color='gray').encode(
        x='Date',
    ).transform_filter(
        nearest
    )

    return alt.layer(line, selectors, text, rules ).properties(
        width=600, height=300, title="Patients Condition"
    ).interactive()

# @st.cache(allow_output_mutation=True)
def test_results_chart(alt, df: pd.DataFrame, stacked='zero'):
    cond = (df['is_first_test'] == "Yes")
    lab_tests = df.loc[cond, ['result_date', 'corona_result']]
    agg_data = lab_tests.groupby(['result_date', 'corona_result']).size().reset_index(name='counts')
    return alt.Chart(agg_data).mark_area(tooltip=True, line=True).encode(
                                                            alt.X('result_date', title='Result Date'),
                                                            alt.Y('counts', title='Counts', stack=stacked),
                                                            color=alt.Color('corona_result',  legend=alt.Legend(orient="top", title=''))
                                                    ).properties(
        width=600, height=300, title="Lab Test Results"
    ).interactive()

# @st.cache(allow_output_mutation=True)
def yishuv_level_chart(alt, df: pd.DataFrame, by_pop=True):
    source = df.copy()
    if by_pop:
        source['value'] = source['value'].astype('int64')/(source['pop2018']/1000)
    else:
        source['value'] = source['value'].astype('int64')

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['date'], empty='none')

    line = alt.Chart(source).mark_line(interpolate='basis').encode(
        x=alt.X('date:T', title=""),
        y=alt.Y('value',title=""),
        color=alt.Color('Yishuv', title='Yishuv', legend=alt.Legend(orient="top", title=''))
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
        width=600, height=300, title="Cases by Yishuv"
    ).resolve_scale(y='independent').interactive()
            )

