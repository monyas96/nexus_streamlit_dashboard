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
# Import logo renderer if it exists in utils
try:
    from utils import render_logo_header
except ImportError:
    def render_logo_header(): # Dummy function if not found
        pass

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
    # --- Map for PEFA PI-1 ---
    st.markdown("#### Geographical Distribution (PEFA PI-1)")
    indicator_tab1 = "PEFA: PI-1 Aggregate expenditure out-turn"
    uv.render_indicator_map(
        df=df_filtered,
        indicator_label=indicator_tab1,
        title="", # No title needed, context from tab
        description="Latest available scores for PEFA PI-1.",
        reference_data=ref_data,
        year_range=filters.get('year_range'),
        map_options={
            'color_continuous_scale': 'Viridis',
            'range_color': [0, 4]
        },
        container_key="topic4_1_tab1_map" # Unique key for this map
    )
    st.divider()

    # --- Chart for PEFA PI-1 (Existing) ---
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
        container_key="topic4_1_tab1_chart" # Updated key
    )

    # --- Learn More Expander (Existing) ---
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
PEFA-WB's Aggregate Expenditure Outturn is used as a proxy since it directly measures the extent to which government spending aligns with the approved budget.
            """)

# === Tab 2: 4.1.2 ===
with tab2:
    # --- Map for PEFA PI-2 ---
    st.markdown("#### Geographical Distribution (PEFA PI-2)")
    indicator_tab2 = "PEFA: PI-2 Expenditure composition outturn"
    uv.render_indicator_map(
        df=df_filtered,
        indicator_label=indicator_tab2,
        title="", # No title needed, context from tab
        description="Latest available scores for PEFA PI-2.",
        reference_data=ref_data,
        year_range=filters.get('year_range'),
        map_options={
            'color_continuous_scale': 'Plasma', # Different scale example
            'range_color': [0, 4]
        },
        container_key="topic4_1_tab2_map" # Unique key for this map
    )
    st.divider()

    # --- Chart for PEFA PI-2 (Existing) ---
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
        container_key="topic4_1_tab2_chart" # Updated key
    )

    # --- Learn More Expander (Existing) ---
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
PEFA-WB's Expenditure Composition Outturn is used as a proxy because it assesses if resources are allocated according to national priorities, ensuring minimal waste.
            """)

# === Data Explorer (Reintroduced) ===
st.divider()
# uv.create_data_explorer(df_filtered, key_prefix="topic4_1")

# Optional Debug section (can be uncommented if needed)
# with st.expander("Debug Info"):
#     st.write("Selected Filters:", filters)
#     st.write("Filtered Data Shape:", df_filtered.shape)
