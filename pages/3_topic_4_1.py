import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path for module imports
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import the universal visualization module
import universal_viz as uv


# --- Data Loading ---
# Cache main data loading
@st.cache_data
def load_main_data(file_path="data/nexus.parquet"):
    """Loads the main dataset from a parquet file."""
    try:
        df = pd.read_parquet(file_path)
        # Basic validation (optional)
        required_cols = ['indicator_label', 'country_or_area', 'year', 'value', 'iso3']
        if not all(col in df.columns for col in required_cols):
             st.warning(f"Warning: Main data might be missing some expected columns ({required_cols}).")
        return df
    except FileNotFoundError:
        st.error(f"Error: The main data file was not found at {file_path}")
        return pd.DataFrame() # Return empty DataFrame on error
    except Exception as e:
        st.error(f"An error occurred while loading the main data: {e}")
        return pd.DataFrame()

# --- Page Setup & Initial Data Load ---
render_logo_header()

# Load reference data using the universal function
ref_data = uv.load_country_reference_data()

# Load main data
df_main = load_main_data()

# Stop execution if essential data is missing
if df_main.empty or ref_data.empty:
    st.error("Failed to load essential data (main data or reference data). Page rendering stopped.")
    st.stop()

# --- Sidebar Filters --- (Reintroduced)
filters = uv.setup_sidebar_filters(ref_data, df_main, key_prefix="topic4_1")

# --- Filter Main Data --- (Reintroduced)
df_filtered = uv.filter_dataframe_by_selections(df_main, filters, ref_data)

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

# === Tabs Start Immediately After Intro ===
tab1, tab2 = st.tabs([
    "📌 4.1.1: Public Expenditure Efficiency",
    "📌 4.1.2: Expenditure Quality"
])

# === Tab 1: 4.1.1 ===
with tab1:
    indicator_tab1 = "PEFA: PI-1 Aggregate expenditure out-turn"
    uv.render_indicator_section(
        df=df_filtered,
        indicator_label=indicator_tab1,
        title="Indicator 4.1.1: Aggregate Expenditure Outturn",
        description="Proxy for Public Expenditure Efficiency Index. Measures how closely actual aggregate expenditures align with the original budget.",
        chart_type="bar",
        selected_countries=filters.get('selected_countries'),
        year_range=filters.get('year_range'),
        chart_options={'x': 'country_or_area', 'y': 'value', 'color': 'year', 'sort_x': '-y'},
        show_data_table=True,
        container_key="topic4_1_tab1_chart"
    )
    # --- Learn More Expander (directly under chart) ---
    with st.expander("🔍 Learn more about Indicator 4.1.1"):
        t1_1, t1_2, t1_3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
        with t1_1:
            st.markdown("Aggregate deviation of actual expenditure from the original budget, measured as a percentage.")
        with t1_2:
            st.markdown("- **Efficiency**: Budget credibility.  \n- **Effectiveness**: Predictable resource flow.")
        with t1_3:
            st.markdown("PEFA standard indicator, globally recognized.")
    st.divider()
    uv.render_indicator_map(
        df=df_filtered,
        indicator_label=indicator_tab1,
        title="",
        description="Geographical distribution of latest scores.",
        reference_data=ref_data,
        year_range=filters.get('year_range'),
        map_options={
            'color_continuous_scale': 'Viridis',
            'range_color': [0, 4]
        },
        container_key="topic4_1_tab1_map"
    )
    st.divider()

# === Tab 2: 4.1.2 ===
with tab2:
    indicator_tab2 = "PEFA: PI-2 Expenditure composition outturn"
    uv.render_indicator_section(
        df=df_filtered,
        indicator_label=indicator_tab2,
        title="Indicator 4.1.2: Expenditure Composition Outturn",
        description="Proxy for Public Expenditure Efficiency Index. Measures the variance between budgeted and actual expenditure composition.",
        chart_type="line",
        selected_countries=filters.get('selected_countries'),
        year_range=filters.get('year_range'),
        chart_options={'x': 'year', 'y': 'value', 'color': 'country_or_area'},
        show_data_table=True,
        container_key="topic4_1_tab2_chart"
    )
    # --- Learn More Expander (directly under chart) ---
    with st.expander("🔍 Learn more about Indicator 4.1.2"):
        t2_1, t2_2, t2_3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
        with t2_1:
            st.markdown("Variance in expenditure composition compared to the original budget by functional classification.")
        with t2_2:
            st.markdown("- **Efficiency**: Strategic allocation adherence.  \n- **Effectiveness**: Predictability of sector funding.")
        with t2_3:
            st.markdown("PEFA standard indicator.")
    st.divider()
    uv.render_indicator_map(
        df=df_filtered,
        indicator_label=indicator_tab2,
        title="",
        description="Geographical distribution of latest scores.",
        reference_data=ref_data,
        year_range=filters.get('year_range'),
        map_options={
            'color_continuous_scale': 'Plasma',
            'range_color': [0, 4]
        },
        container_key="topic4_1_tab2_map"
    )
    st.divider()

# === Data Gap Expander (once per page, after all tabs) ===
all_indicators_4_1 = {
    "Aggregate Expenditure Outturn (4.1.1)": "PEFA: PI-1 Aggregate expenditure out-turn",
    "Expenditure Composition Outturn (4.1.2)": "PEFA: PI-2 Expenditure composition outturn"
}
africa_countries = ref_data[ref_data['Region'] == 'Africa']['Country'].unique()
df_africa = df_main[df_main['country_or_area'].isin(africa_countries)]
st.divider()
with st.expander("Understand the data gap in Africa for this topic"):
    selected_gap_indicator = st.selectbox(
        "Select indicator to view data availability:",
        options=list(all_indicators_4_1.keys()),
        key="topic4_1_gap_indicator_select"
    )
    uv.render_data_availability_heatmap(
        df=df_africa,
        indicator_label=all_indicators_4_1[selected_gap_indicator],
        title=f"Data Availability for {selected_gap_indicator} (Africa)",
        container_key="topic4_1_gap"
    )

# Optional Debug section (can be uncommented if needed)
# with st.expander("Debug Info"):
#     st.write("Selected Filters:", filters)
#     st.write("Filtered Data Shape:", df_filtered.shape)
