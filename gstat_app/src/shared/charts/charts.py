from math import ceil
import datetime

from altair import Chart  # type: ignore
import pandas as pd  # type: ignore
import streamlit as st
from penn_chime.parameters import Parameters
from src.penn_chime.utils import add_date_column
from src.penn_chime.presentation import DATE_FORMAT


@st.cache(allow_output_mutation=True)
def yishuv_level_chart(alt, df: pd.DataFrame, by_pop=True):
    source = df
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

@st.cache(allow_output_mutation=True)
def isolations_chart(alt, df: pd.DataFrame, stacked='zero'):
    isolations = df.melt(id_vars='date', value_vars=df.columns[1:]).dropna()
    return alt.Chart(isolations).mark_area(tooltip=True, line=True).encode(alt.X('date', title='Isolation Date'),
                                                                           alt.Y('value', title='Count', stack=stacked),
                                                               color=alt.Color('variable',  legend=alt.Legend(orient="top", title=''))).properties(
        width=600, height=300, title="Isolation"
    ).interactive()
@st.cache(allow_output_mutation=True)
def test_symptoms_chart(alt, df: pd.DataFrame, drill_down=True, stacked='normalize'):

    symptoms = df
    symptoms = symptoms.drop(columns=['age_60_and_above', 'gender'])
    sym_cols = symptoms.columns
    sym_cols = [c for c in sym_cols if c not in ['test_date', 'corona_result', 'test_indication']]
    symptoms = symptoms.melt(id_vars=['test_date', 'test_indication','corona_result'], value_vars=sym_cols).dropna()
    agg_data = symptoms.groupby(['test_date', 'corona_result', 'test_indication','variable'], as_index=False).sum()
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
@st.cache(allow_output_mutation=True)
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
@st.cache(allow_output_mutation=True)
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

    return alt.layer(line,selectors, text, rules ).properties(
        width=600, height=300, title="Patients Condition"
    ).interactive()

@st.cache(allow_output_mutation=True)
def olg_projections_chart(alt, df: pd.DataFrame, title: str, by_corona_time=True, baseline=False):
    olg_cols = df.columns
    olg_cols = [c for c in olg_cols if c not in ['date', 'corona_days', 'country', 'prediction_ind']]
    olg_df = df.melt(id_vars=['date', 'corona_days', 'country', 'prediction_ind'], value_vars=olg_cols).dropna()
    if by_corona_time==False :
        olg_df['corona_days'] = olg_df['date']
    line1 = alt.Chart(olg_df.loc[olg_df['prediction_ind'] == 0, :]).transform_calculate(
        cat="datum.country + '-' + datum.variable"
    ).mark_line(interpolate='basis', point=False, tooltip=True).encode(
        x='corona_days',
        y=alt.Y('value', title=""),
        color=alt.Color('cat:N', title=None, legend=alt.Legend(orient="top", title='')),
    )

    line2 = alt.Chart(olg_df.loc[olg_df['prediction_ind'] == 1, :]).transform_calculate(
        cat="datum.country + '-' + datum.variable"
    ).mark_line(interpolate='basis', point=False, tooltip=True, strokeDash=[1, 1]).encode(
        x=alt.X('corona_days', title=""),
        y=alt.Y('value', title=""),
        color=alt.Color('cat:N', title=None, legend=alt.Legend(orient="top", title='')),
    )

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['corona_days'], empty='none')


    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(olg_df).mark_point().encode(
        x='corona_days',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    # Draw text labels near the points, and highlight based on selection
    text = line1.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'value', alt.value(' ')),
        y=alt.Y('value', axis=alt.Axis(labels=True, title='', tickOpacity=0)),
    )

    text2 = line2.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'value', alt.value(' ')),
        y=alt.Y('value', axis=alt.Axis(labels=True, title='', tickOpacity=0)),
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(olg_df).mark_rule(color='gray').encode(
        x='corona_days',
    ).transform_filter(
        nearest
    )

    if baseline:
        rule = alt.Chart(olg_df).transform_calculate("baseline", "500") .mark_rule().encode(
            y='baseline:Q',
            # color='symbol',
            size=alt.value(0.5)
        )
        return alt.layer(line1, line2, rule, selectors, text, text2, rules).properties(
                width=600, height=300, title=title
            ).interactive()
    else:
        return alt.layer(line1, line2, selectors, text, text2, rules).properties(
                width=600, height=300, title=title
            ).interactive()




def new_admissions_chart(
        alt, projection_admits: pd.DataFrame, parameters: Parameters
) -> Chart:
    """docstring"""
    plot_projection_days = parameters.n_days - 10
    max_y_axis = parameters.max_y_axis
    as_date = parameters.as_date

    y_scale = alt.Scale()

    if max_y_axis is not None:
        y_scale.domain = (0, max_y_axis)

    tooltip_dict = {False: "day", True: "date:T"}
    if as_date:
        projection_admits = add_date_column(projection_admits)
        x_kwargs = {"shorthand": "date:T", "title": "Date", "axis": alt.Axis(format=(DATE_FORMAT))}
    else:
        x_kwargs = {"shorthand": "day", "title": "Days from today"}

    # TODO fix the fold to allow any number of dispositions
    return (
        alt.Chart(projection_admits.head(plot_projection_days))
            .transform_fold(fold=["hospitalized", "icu", "ventilated"])
            .mark_line(point=True)
            .encode(
            x=alt.X(**x_kwargs),
                y=alt.Y("value:Q", title="Daily admissions", scale=y_scale),
            color="key:N",
            tooltip=[
                tooltip_dict[as_date],
                alt.Tooltip("value:Q", format=".0f", title="Admissions"),
                "key:N",
            ],
        )
            .interactive()
    )


def admitted_patients_chart(
        alt, census: pd.DataFrame, parameters: Parameters
) -> Chart:
    """docstring"""

    plot_projection_days = parameters.n_days - 10
    max_y_axis = parameters.max_y_axis
    as_date = parameters.as_date
    if as_date:
        census = add_date_column(census)
        x_kwargs = {"shorthand": "date:T", "title": "Date", "axis": alt.Axis(format=(DATE_FORMAT))}
        idx = "date:T"
    else:
        x_kwargs = {"shorthand": "day", "title": "Days from today"}
        idx = "day"

    y_scale = alt.Scale()

    if max_y_axis:
        y_scale.domain = (0, max_y_axis)

    # TODO fix the fold to allow any number of dispositions
    return (
        alt.Chart(census.head(plot_projection_days))
            .transform_fold(fold=["hospitalized", "icu", "ventilated"])
            .mark_line(point=True)
            .encode(
            x=alt.X(**x_kwargs),
            y=alt.Y("value:Q", title="Census", scale=y_scale),
            color="key:N",
            tooltip=[
                idx,
                alt.Tooltip("value:Q", format=".0f", title="Census"),
                "key:N",
            ],
        )
            .interactive()
    )


def additional_projections_chart(
        alt, model, parameters
) -> Chart:
    # TODO use subselect of df_raw instead of creating a new df
    raw_df = model.raw_df
    dat = pd.DataFrame({
        "infected": raw_df.infected,
        "recovered": raw_df.recovered
    })
    dat["day"] = dat.index

    as_date = parameters.as_date
    max_y_axis = parameters.max_y_axis

    if as_date:
        dat = add_date_column(dat)
        x_kwargs = {"shorthand": "date:T", "title": "Date", "axis": alt.Axis(format=(DATE_FORMAT))}
    else:
        x_kwargs = {"shorthand": "day", "title": "Days from today"}

    y_scale = alt.Scale()

    if max_y_axis is not None:
        y_scale.domain = (0, max_y_axis)

    return (
        alt.Chart(dat)
            .transform_fold(fold=["infected", "recovered"])
            .mark_line()
            .encode(
            x=alt.X(**x_kwargs),
            y=alt.Y("value:Q", title="Case Volume", scale=y_scale),
            tooltip=["key:N", "value:Q"],
            color="key:N",
        )
            .interactive()
    )


def chart_descriptions(chart: Chart, labels, suffix: str = ""):
    """

    :param chart: Chart: The alt chart to be used in finding max points
    :param suffix: str: The assumption is that the charts have similar column names.
                   The census chart adds " Census" to the column names.
                   Make sure to include a space or underscore as appropriate
    :return: str: Returns a multi-line string description of the results
    """
    messages = []

    cols = ["hospitalized", "icu", "ventilated"]
    asterisk = False
    day = "date" if "date" in chart.data.columns else "day"

    for col in cols:
        if chart.data[col].idxmax() + 1 == len(chart.data):
            asterisk = True

        on = chart.data[day][chart.data[col].idxmax()]
        if day == "date":
            on = datetime.datetime.strftime(on, "%b %d")  # todo: bring this to an optional arg / i18n
        else:
            on += 1  # 0 index issue

        messages.append(
            "{}{} peaks at {:,} on day {}{}".format(
                labels[col],
                suffix,
                ceil(chart.data[col].max()),
                on,
                "*" if asterisk else "",
            )
        )

    if asterisk:
        messages.append("_* The max is at the upper bound of the data, and therefore may not be the actual max_")
    return "\n\n".join(messages)

