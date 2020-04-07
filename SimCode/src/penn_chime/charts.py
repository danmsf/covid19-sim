from math import ceil
import datetime

from altair import Chart  # type: ignore
import pandas as pd  # type: ignore

from .parameters import Parameters
from .utils import add_date_column
from .presentation import DATE_FORMAT


def admission_rma_chart(alt, df: pd.DataFrame, df_predict: pd.DataFrame):
    print(df.head(5))
    country_count = len(set(df['country'].values)) # df['country'].nunique()
    print(df['country'].nunique())

    if country_count == 1:
        df = df.melt(id_vars=['date'], value_vars=['A', 'I', 'E'])  #
        df_predict = df_predict.melt(id_vars=['date'], value_vars=['A', 'I'])

    else:
        pp = set(df['country'])
        df = df.pivot(index='date', columns='country', values='A').reset_index().melt(id_vars=['date'],
                                                                                      value_vars=pp)
        df_predict = df_predict.pivot(index='date', columns='country', values='A').reset_index().melt(id_vars=['date'],
                                                                                                      value_vars=pp)
    df['value'] = df['value'].astype('int64')
    df_predict['value'] = df_predict['value'].astype('int64')

    color = 'variable' if country_count == 1 else 'country'

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['date'], empty='none')

    # The basic line
    line = alt.Chart(df).mark_line(interpolate='basis').encode(
        x='date:T',
        y='value',
        color='country'
    )

    line2 = alt.Chart(df_predict).mark_line(interpolate='basis', strokeDash=[1, 1]).encode(
        x='date:T',
        y='value',
        color='country'
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(df_predict).mark_point().encode(
        x='date',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )
    # Draw points on the line, and highlight based on selection
    points = line2.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line2.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'value', alt.value(' '))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(df_predict).mark_rule(color='gray').encode(
        x='date:T',
    ).transform_filter(
        nearest
    )

    # Put the five layers into a chart and bind the data

    return (alt.layer(
        line, line2, selectors, points, rules, text
    ).properties(
        width=600, height=300
    ).interactive()
    )

def yishuv_level_chart(alt, df: pd.DataFrame,):
    # colnames = df.columns
    # colnames = [c for c in colnames if c not in ['date', 'StringencyIndex', 'Country']]
    # source = df.melt(id_vars=['date', 'Country'], value_vars=colnames).dropna()
    source = df
    source['value'] = source['value'].astype('int64')

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['date'], empty='none')

    line = alt.Chart(source).mark_line(interpolate='basis').encode(
        x='date:T',
        y='value',
        color='Yishuv'
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
        width=600, height=300, title="Israel - Total Cases"
    ).resolve_scale(y='independent').interactive()
            )

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
        color='variable'
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

