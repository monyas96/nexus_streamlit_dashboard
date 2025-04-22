import streamlit as st
import pandas as pd
import pydeck as pdk
from pathlib import Path
from utils import render_logo_header

render_logo_header()
# === Top Bar ===
col1, col2 = st.columns([0.8, 0.1])
with col1:
    st.title("📊 Topic 4.3: Capital Markets")
with col2:
    st.page_link("pages/0_home.py", label="🏠 Back to Home")

# === Intro ===
st.markdown("""
Capital markets are essential for mobilizing domestic financial resources and channeling savings into productive investments.  
A well-developed capital market reduces reliance on foreign financing, supports sustainable economic growth, and strengthens financial stability.  
**Effective management of capital markets ensures that resources are directed toward areas that maximize national development.**
""")

# === Country Selector & Map ===
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "iso3_country_reference.csv"
ref = pd.read_csv(DATA_PATH).rename(columns={"Country or Area": "country_name"})

country_list = sorted(ref["country_name"].dropna().unique())
selected_country = st.selectbox("🔎 Select a country to explore:", country_list)

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

# === Main Tabs for Each Subtopic ===
st.markdown("## 🧭 Indicator Insights")
tab1, tab2, tab3 = st.tabs([
    "📈 4.3.1: Market Capitalization",
    "🏦 4.3.2: Financial Intermediation",
    "💼 4.3.3: Institutional Investors"
])

# === Tab 1: Market Capitalization ===
with tab1:
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Indicator: Stock Market Capitalization to GDP**")
            st.image("logos/Market Capitalization of Listed Domestic Companies (Current $US.png", use_container_width=True)
            with st.expander("Learn more about this indicator"):
                d1, d2, d3 = st.tabs(["Definition", "Relevance", "Proxy Justification"])
                with d1:
                    st.write("Measures total value of listed companies as a % of GDP.")
                with d2:
                    st.write("Efficiency: Capital mobilization  \nEffectiveness: Links to sectoral investment")
                with d3:
                    st.write("No proxy needed. Source: World Bank.")
        with col2:
            st.markdown("**Indicator: Bond Market Development**")
            st.image("logos/Portfoilo Investment Bonds (Current US$).png", use_container_width=True)
            with st.expander("Learn more about this indicator"):
                d1, d2, d3 = st.tabs(["Definition", "Relevance", "Proxy Justification"])
                with d1:
                    st.write("Measures volume of domestic bonds issued and traded.")
                with d2:
                    st.write("Efficiency: Capital raised  \nEffectiveness: Infrastructure & development finance")
                with d3:
                    st.write("Direct indicator.")

# === Tab 2: Financial Intermediation ===
with tab2:
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Indicator: Adequacy of International Reserves**")
            st.image("logos/Adequacy of International Reserves.png", use_container_width=True)
            with st.expander("Learn more about this indicator"):
                d1, d2, d3 = st.tabs(["Definition", "Relevance", "Proxy Justification"])
                with d1:
                    st.write("Ratio of reserves to short-term external debt.")
                with d2:
                    st.write("Efficiency: Reserve sufficiency  \nEffectiveness: Shock protection")
                with d3:
                    st.write("Direct indicator. Source: IMF.")
        with col2:
            st.markdown("**Indicator: Banking Sector Development Index**")
            st.image("logos/Banking Sector Development Index.png", use_container_width=True)
            with st.expander("Learn more about this indicator"):
                d1, d2, d3 = st.tabs(["Definition", "Relevance", "Proxy Justification"])
                with d1:
                    st.write("Captures depth, access, and efficiency of banking systems.")
                with d2:
                    st.write("Efficiency: Credit allocation  \nEffectiveness: Inclusive growth")
                with d3:
                    st.write("Proxy: IMF FAS / World Bank Findex")

# === Tab 3: Institutional Investors ===
with tab3:
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Indicator: Private Sector Credit to GDP**")
            
            with st.expander("Learn more about this indicator"):
                d1, d2, d3 = st.tabs(["Definition", "Relevance", "Proxy Justification"])
                with d1:
                    st.write("Measures credit provided to the private sector as % of GDP.")
                with d2:
                    st.write("Efficiency: Credit expansion  \nEffectiveness: Business growth")
                with d3:
                    st.write("World Bank direct indicator.")
        with col2:
            st.markdown("**Indicator: Pension & Sovereign Wealth Fund Investments**")
            
            with st.expander("Learn more about this indicator"):
                d1, d2, d3 = st.tabs(["Definition", "Relevance", "Proxy Justification"])
                with d1:
                    st.write("Share of pension/SWF assets invested in national markets.")
                with d2:
                    st.write("Efficiency: Long-term allocation  \nEffectiveness: Domestic economic returns")
                with d3:
                    st.write("Proxies from national fund reports / SWFI database.")
