import streamlit as st
import pandas as pd
import pydeck as pdk
from pathlib import Path
from utils import render_logo_header

render_logo_header()
# === Top Bar ===
col1, col2 = st.columns([0.8, 0.1])
with col1:
    st.title("📊 Topic 4.2: Budget and Tax Revenues")
with col2:
    st.page_link("pages/0_home.py", label="🏠 Back to Home")

# === Intro ===
st.markdown("""
Budget and tax revenues are crucial for ensuring that governments have the financial resources necessary to fund essential services and development initiatives.  
**Efficient and effective management of tax revenues helps reduce dependency on external financing, enhance fiscal stability, and direct resources toward national priorities.**
""")

# === Load Country Data ===
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "iso3_country_reference.csv"
ref = pd.read_csv(DATA_PATH).rename(columns={"Country or Area": "country_name"})

# === Country Selector ===
country_list = sorted(ref["country_name"].dropna().unique())
selected_country = st.selectbox("🔎 Select a country to explore:", country_list)

# === Map ===
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

# === Tabs for Subtopics ===
st.markdown("## 🧭 Indicator Insights")
tab1, tab2 = st.tabs([
    "🧾 4.2.1: Tax Revenue Collection",
    "🧾 4.2.2: Tax Administration Efficiency"
])

# === Tab 1: 4.2.1 ===
with tab1:
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 💰 Indicator 4.2.1.1: Tax Revenue as % of GDP")
            st.caption("Source: World Bank")
            st.image("logos/ Tax Revenue as Percentage of GDP.png", caption="Tax Revenue (% of GDP)", use_container_width=True)
            with st.expander("🔍 Learn more about Indicator 4.2.1.1"):
                t1, t2, t3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
                with t1:
                    st.markdown("Measures the total tax revenue collected as a proportion of the country's GDP.")
                with t2:
                    st.markdown("- **Efficiency**: Shows how well revenue is raised from the economy.  \n- **Effectiveness**: Reflects fiscal independence.")
                with t3:
                    st.markdown("This World Bank indicator is standard, widely used, and globally comparable.")

        with col2:
            st.markdown("### 🧾 Indicator 4.2.1.2: Taxpayer Base Expansion")
            st.caption("Proxied by ATAF")
            st.image("logos/Taxpayer Base Expansion.png", caption="Growth in Registered Taxpayer Base", use_container_width=True)
            with st.expander("🔍 Learn more about Indicator 4.2.1.2"):
                b1, b2, b3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
                with b1:
                    st.markdown("Tracks growth in registered taxpayers to assess compliance and coverage.")
                with b2:
                    st.markdown("- **Efficiency**: Reflects broadening of the tax system.  \n- **Effectiveness**: Signals outreach and inclusion.")
                with b3:
                    st.markdown("ATAF metrics on large taxpayer units and general taxpayer growth are used as a proxy.")

# === Tab 2: 4.2.2 ===
with tab2:
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📈 Indicator 4.2.2.1: Tax Collection Efficiency Score")
            st.caption("Proxied by USAID/OECD Tax Effort")
            st.image("logos/Tax Collection Efficiency Score.png", caption="Tax Effort Ratio", use_container_width=True)
            with st.expander("🔍 Learn more about Indicator 4.2.2.1"):
                c1, c2, c3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
                with c1:
                    st.markdown("Ratio of actual to potential revenue – showing how much is captured from total capacity.")
                with c2:
                    st.markdown("- **Efficiency**: Shows capacity of collection systems.  \n- **Effectiveness**: Closes gaps between potential and actual.")
                with c3:
                    st.markdown("Tax effort is a widely recognized proxy in global evaluations.")

        with col2:
            st.markdown("### 🚫 Indicator 4.2.2.2: Reduction in Tax Evasion")
            st.caption("Proxied by Tax Buoyancy")
            st.image("logos/Reduction in Tax Evasion.png", caption="Tax Buoyancy – Evasion Reduction", use_container_width=True)
            with st.expander("🔍 Learn more about Indicator 4.2.2.2"):
                d1, d2, d3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
                with d1:
                    st.markdown("Estimates the reduction in tax evasion over time.")
                with d2:
                    st.markdown("- **Efficiency**: Reflects stronger enforcement.  \n- **Effectiveness**: Reduces informal leakages.")
                with d3:
                    st.markdown("ATAF and OECD's buoyancy data show responsiveness of tax systems to growth.")
