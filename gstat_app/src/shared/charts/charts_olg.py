from altair import Chart  # type: ignore
import pandas as pd  # type: ignore
import streamlit as st

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
