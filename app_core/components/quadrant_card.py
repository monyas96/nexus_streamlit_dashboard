import streamlit as st
import altair as alt
import pandas as pd


def _mini_chart(data: pd.DataFrame, chart_type: str, color: str):
    if data is None or data.empty:
        data = pd.DataFrame({"Year": [2015, 2020, 2024], "Value": [0, 0, 0]})

    if "Year" not in data.columns or "Value" not in data.columns:
        # Try to coerce common schemas
        df = data.copy()
        if "year" in df.columns:
            df = df.rename(columns={"year": "Year"})
        if "value" in df.columns:
            df = df.rename(columns={"value": "Value"})
        data = df[[c for c in ["Year", "Value"] if c in df.columns]]
        if set(["Year", "Value"]).difference(data.columns):
            data = pd.DataFrame({"Year": [2015, 2020, 2024], "Value": [0, 0, 0]})

    data = data.copy()
    data["Year"] = data["Year"].astype(str)

    if chart_type == "bar":
        chart = alt.Chart(data).mark_bar(color=color).encode(x="Year:O", y="Value:Q")
    else:
        chart = alt.Chart(data).mark_line(color=color).encode(x="Year:O", y="Value:Q")

    return chart.properties(height=140)


def quadrant_card(
    pillar_name: str,
    color: str,
    indicator_data: pd.DataFrame,
    chart_type: str,
    concept_text: str,
    data_summary: str,
    link: str,
    key: str | None = None,
):
    with st.container():
        st.markdown(
            f"<div class='quadrant' style='border-top: 5px solid {color};'>",
            unsafe_allow_html=True,
        )

        chart = _mini_chart(indicator_data, chart_type, color)
        st.altair_chart(chart, use_container_width=True)

        st.markdown(
            f"""
            <div class="tooltip">
                <strong>{pillar_name}</strong><br/>
                {concept_text}<br/>
                <em>{data_summary}</em>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(f"Explore {pillar_name}", key=(key or pillar_name)):
            st.switch_page(link)

        st.markdown("</div>", unsafe_allow_html=True)
