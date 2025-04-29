import altair as alt
import pandas as pd
import streamlit as st

def plot_indicator(
    df: pd.DataFrame,
    indicator_label: str,
    countries: list = None,
    chart_type: str = "bar",
    y_title: str = "Value",
    show_chart: bool = True
):
    """
    Create a reusable Altair chart for a given indicator.

    Args:
        df: Long-format DataFrame with OBT structure
        indicator_label: The indicator to plot (from df['indicator_label'])
        countries: Optional list of ISO3 codes to filter
        chart_type: "bar" or "line"
        y_title: Label for Y-axis
        show_chart: Whether to display with st.altair_chart

    Returns:
        Altair Chart object
    """
    filtered = df[df["indicator_label"] == indicator_label].copy()

    if countries:
        filtered = filtered[filtered["iso3"].isin(countries)]

    if chart_type == "bar":
        mark = alt.Chart(filtered).mark_bar()
    elif chart_type == "line":
        mark = alt.Chart(filtered).mark_line()
    else:
        raise ValueError("Unsupported chart_type. Use 'bar' or 'line'.")

    chart = mark.encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("value:Q", title=y_title),
        color=alt.Color("country_or_area:N", title="Country"),
        tooltip=["country_or_area", "year", "value"]
    ).properties(
        title=indicator_label,
        width=700,
        height=400
    )

    if show_chart:
        st.altair_chart(chart, use_container_width=True)

    return chart
