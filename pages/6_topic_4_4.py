import streamlit as st
import pandas as pd
import pydeck as pdk
from pathlib import Path
from utils import render_logo_header

render_logo_header()
# === Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "iso3_country_reference.csv"

# === Top Bar ===
col1, col2 = st.columns([0.8, 0.1])
with col1:
    st.title("Topic 4.4: Illicit Financial Flows (IFFs)")
with col2:
    st.page_link("pages/0_home.py", label="Back to Home", use_container_width=True)

# === Overview ===
st.markdown("""
Illicit financial flows (IFFs) represent a significant loss of resources that could fund development.  
They include trade mispricing, tax evasion, corruption, and illegal activity. Tackling IFFs strengthens domestic resource mobilization.
""")

# === Country Selector ===
ref = pd.read_csv(DATA_PATH).rename(columns={"Country or Area": "country_name"})
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

# === Indicator Tabs ===
st.subheader("Indicator Insights")
tab1, tab2, tab3 = st.tabs([
    "4.4.1: Magnitude of Illicit Financial Flows",
    "4.4.2: Types of IFFs",
    "4.4.3: Detection and Enforcement"
])

# === Tab 1: Magnitude of IFFs ===
with tab1:
    with st.container():
        st.markdown("### Indicator 4.4.1.1: IFFs as % of GDP")
        st.caption("Proxied by Global Financial Integrity")
        st.info("Graph Placeholder: IFFs as a % of GDP")
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** Estimated value of IFFs relative to GDP, showing macro-level impact.  
**Proxy:** Based on GFI trade gap & capital flight data.
            """)

    with st.container():
        st.markdown("### Indicator 4.4.1.2: Annual IFF Volume")
        st.caption("Proxied by Global Financial Integrity")
        st.info("Graph Placeholder: Total IFF Volume")
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** Total illicit outflows per year (USD).  
**Proxy:** GFI estimate of unrecorded transfers, trade mismatches.
            """)

# === Tab 2: Types of IFFs ===
with tab2:
    with st.container():
        st.markdown("### Indicator 4.4.2.1: Trade Mispricing")
        st.caption("Proxied by GFI Trade Gap Data")
        st.info("Graph Placeholder: Trade Mispricing")
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** Manipulating trade values to illegally shift capital.  
**Proxy:** GFI's bilateral trade mismatch analysis.
            """)

    with st.container():
        st.markdown("### Indicator 4.4.2.2: Tax Evasion")
        st.caption("Proxied by IMF Tax Registration Data")
        st.info("Graph Placeholder: Tax Evasion Trends")
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** Illegally avoiding taxes via underreporting or offshore hiding.  
**Proxy:** Share of taxpayers vs. population (IMF compliance benchmark).
            """)

    with st.container():
        st.markdown("### Indicator 4.4.2.3: Criminal Activities")
        st.caption("Proxied by UNODC Crime Flow Data")
        st.info("Graph Placeholder: Crime-Linked IFFs")
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** IFFs generated from organized crime, trafficking, and corruption.  
**Proxy:** UNODC estimates on proceeds from criminal activity.
            """)

# === Tab 3: Detection and Enforcement ===
with tab3:
    with st.container():
        st.markdown("### Indicator 4.4.3.1: Anti-IFF Enforcement Effectiveness")
        st.caption("Proxied by WJP & CPIA Ratings")
        st.info("Graph Placeholder: Enforcement Metrics")
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** Number of successful investigations and prosecutions.  
**Proxy:** Governance & transparency scores from WJP and CPIA.
            """)

    with st.container():
        st.markdown("### Indicator 4.4.3.2: Corruption & Bribery")
        st.caption("Proxied by WJP & World Bank Governance Indicators")
        st.info("Graph Placeholder: Corruption Index")
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** Perceptions and incidents of corruption in public/private sectors.  
**Proxy:** Control of Corruption index, WJP bribery prevalence score.
            """)
