import streamlit as st
from pathlib import Path
import pandas as pd
import pydeck as pdk
from utils import render_logo_header

render_logo_header()
# === Title and Home Button ===
col1, col2 = st.columns([0.8, 0.1])
with col1:
    st.title("📊 Topic 4.1: Public Expenditures")
with col2:
    st.page_link("pages/0_home.py", label="🏠 Back to Home")

# === Overview ===
st.markdown("""
Public expenditures focus on how governments allocate resources to essential services such as education, health, and infrastructure.  
Effective public expenditure management ensures that resources are not wasted and are directed toward development priorities.
""")

# === Load and Select Country ===
BASE_DIR = Path(__file__).resolve().parent.parent  
data_path = BASE_DIR / "data" / "iso3_country_reference.csv"
ref = pd.read_csv(data_path).rename(columns={"Country or Area": "country_name"})
country_list = sorted(ref["country_name"].dropna().unique())
selected_country = st.selectbox("🔎 Select a country to explore:", country_list)

# === Regional Map ===
st.markdown("### 🌍 Explore by Region")
map_data = ref.copy()
map_data["selected"] = map_data["country_name"] == selected_country

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v10",
    initial_view_state=pdk.ViewState(latitude=0, longitude=20, zoom=2),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=map_data,
            get_position="[lon, lat]",
            get_radius=40000,
            get_fill_color="[255, 100, 10, 180]",
            pickable=True,
        )
    ],
    tooltip={"text": "{country_name}"}
))

# === Tabs for 4.1.1 and 4.1.2 ===
st.markdown("## 🧭 Indicator Insights")
tab1, tab2 = st.tabs([
    "📌 4.1.1: Public Expenditure Efficiency",
    "📌 4.1.2: Expenditure Quality"
])

# === Tab 1: 4.1.1 ===
with tab1:
    with st.container():
        st.markdown("### 📌 Indicator 4.1.1: Aggregate Expenditure Outturn")
        st.caption("Proxy for Public Expenditure Efficiency Index")
        st.image("logos/Aggregate Expenditure Outturn.png", caption="Aggregate Expenditure Outturn", use_container_width=True)

        with st.expander("🔍 Learn more about Indicator 4.1.1"):
            t1, t2, t3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
            with t1:
                st.markdown("This indicator measures how closely actual government expenditures align with the approved budget. It reflects the efficiency of fiscal planning and budget execution.")
            with t2:
                st.markdown("""
- **Efficiency:** Assesses whether public spending adheres to planned allocations, minimizing budget deviations and cost overruns.  
- **Effectiveness:** Ensures that government expenditure remains within set limits, promoting fiscal discipline and stable public financial management.
                """)
            with t3:
                st.markdown("""
The Public Expenditure Efficiency Index (Ratio of actual project costs to budgeted costs) is used to evaluate how well spending follows planned budgets.  
PEFA-WB’s Aggregate Expenditure Outturn is used as a proxy since it directly measures the extent to which government spending aligns with the approved budget.
                """)

# === Tab 2: 4.1.2 ===
with tab2:
    with st.container():
        st.markdown("### 📌 Indicator 4.1.2: Expenditure Composition Outturn")
        st.caption("Proxy for Public Expenditure Quality Index")
        st.image("logos/ Expenditure Composition Outturn.png", caption="Expenditure Composition Outturn", use_container_width=True)

        with st.expander("🔍 Learn more about Indicator 4.1.2"):
            t1, t2, t3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
            with t1:
                st.markdown("This indicator measures whether government expenditures align with policy priorities, ensuring that funds are directed toward critical sectors such as education, health, and infrastructure.")
            with t2:
                st.markdown("""
- **Efficiency:** Evaluates if public spending is allocated as planned, reducing inefficiencies and ensuring fiscal responsibility.  
- **Effectiveness:** Demonstrates whether financial resources are used to support sustainable development and social welfare.
                """)
            with t3:
                st.markdown("""
The Expenditure Quality Score (Percentage of public spending directed toward development priorities) tracks whether expenditures are used for key sectors.  
PEFA-WB’s Expenditure Composition Outturn is used as a proxy because it assesses if resources are allocated according to national priorities, ensuring minimal waste.
                """)
