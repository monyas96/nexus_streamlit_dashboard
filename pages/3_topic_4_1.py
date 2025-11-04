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

# Navigation - Home button and logo
try:
    from app_core.components.navigation import render_navigation_buttons, render_page_logo
    render_page_logo("top-right")
    render_navigation_buttons()
except ImportError:
    pass  # Navigation not critical

# --- Load OSAA CSS ---
try:
    with open("app_core/styles/style_osaa.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception:
        pass

# --- Data Loading ---
@st.cache_data
def load_main_data(file_path="data/nexus.parquet"):
    """Loads the main dataset from a parquet file."""
    try:
        df = pd.read_parquet(file_path)
        required_cols = ['indicator_label', 'country_or_area', 'year', 'value', 'iso3']
        if not all(col in df.columns for col in required_cols):
             st.warning(f"Warning: Main data might be missing some expected columns ({required_cols}).")
        return df
    except FileNotFoundError:
        st.error(f"Error: The main data file was not found at {file_path}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred while loading the main data: {e}")
        return pd.DataFrame()

# --- Page Setup & Initial Data Load ---
ref_data = uv.load_country_reference_data()
df_main = load_main_data()

if df_main.empty or ref_data.empty:
    st.error("Failed to load essential data (main data or reference data). Page rendering stopped.")
    st.stop()

# --- Sidebar Filters ---
filters = uv.setup_sidebar_filters(ref_data, df_main, key_prefix="topic4_1")
df_filtered = uv.filter_dataframe_by_selections(df_main, filters, ref_data)

# ========================================
# SECTION: Topic Header
# ========================================
with st.container():
    st.markdown("""
    <div class="section-header">
        <h1>Topic 4.1: Public Expenditures</h1>
        <p>Public expenditures focus on how governments allocate resources to essential services such as education, health, and infrastructure. Effective public expenditure management ensures that resources are not wasted and are directed toward development priorities.</p>
    </div>
    """, unsafe_allow_html=True)

# ========================================
# SECTION: Global Filter Row
# ========================================
with st.container():
    st.markdown("""
    <div class="filter-bar">
        <h3>Filter Data View</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1.5])
    
    with col1:
        # Year filter - get available years from filtered data
        available_years = sorted(df_filtered['year'].dropna().unique()) if not df_filtered.empty else []
        if available_years:
            selected_year = st.selectbox(
                "Select Year",
                options=["All Years"] + available_years,
                index=0,
                key="global_year_filter"
            )
        else:
            selected_year = "All Years"
    
    with col2:
        # Country filter
        available_countries = sorted(df_filtered['country_or_area'].dropna().unique()) if not df_filtered.empty else []
        if available_countries:
            selected_country = st.selectbox(
                "Select Country",
                options=["All Countries"] + available_countries,
                index=0,
                key="global_country_filter"
            )
        else:
            selected_country = "All Countries"
    
    with col3:
        # Data source filter (showing PEFA as main source for this topic)
        selected_sources = st.multiselect(
            "Data Source",
            options=["PEFA", "World Bank", "IMF"],
            default=["PEFA"],
            key="global_source_filter"
        )

st.divider()

# Apply global filters to the data
df_display = df_filtered.copy()

# Filter by year
if selected_year != "All Years":
    df_display = df_display[df_display['year'] == selected_year]

# Filter by country
if selected_country != "All Countries":
    df_display = df_display[df_display['country_or_area'] == selected_country]

# Update filters dict to pass filtered countries/years to render functions
display_filters = filters.copy()
if selected_year != "All Years":
    display_filters['year_range'] = (selected_year, selected_year)
if selected_country != "All Countries":
    display_filters['selected_countries'] = [selected_country]

# ========================================
# SECTION: Key Indicators (2 columns)
# ========================================
st.markdown("### Key Indicators Overview")

col1, col2 = st.columns(2, gap="large")

# Indicator 4.1.1 - Left Column
with col1:
    with st.container():
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.1.1: Aggregate Expenditure Outturn</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 1rem;">
                Measures how closely actual aggregate expenditures align with the original budget. 
                This is a proxy for Public Expenditure Efficiency Index and indicates budget credibility.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Render chart
        indicator_tab1 = "PEFA: PI-1 Aggregate expenditure out-turn"
        uv.render_indicator_section(
            df=df_display,
            indicator_label=indicator_tab1,
            title="",
            description="",
            chart_type="bar",
            selected_countries=display_filters.get('selected_countries'),
            year_range=display_filters.get('year_range'),
            chart_options={'x': 'country_or_area', 'y': 'value', 'color': 'year', 'sort_x': '-y'},
            show_data_table=True,
            container_key="topic4_1_ind1_chart"
        )
        
        # Learn More Expander
        with st.expander("Learn more about this indicator"):
            tab_def, tab_rel, tab_proxy = st.tabs(["Definition", "Relevance", "Proxy Justification"])
            with tab_def:
                st.markdown("Aggregate deviation of actual expenditure from the original budget, measured as a percentage.")
            with tab_rel:
                st.markdown("- **Efficiency**: Budget credibility.  \n- **Effectiveness**: Predictable resource flow.")
            with tab_proxy:
                st.markdown("PEFA standard indicator, globally recognized.")

# Indicator 4.1.2 - Right Column
with col2:
    with st.container():
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.1.2: Expenditure Composition Outturn</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 1rem;">
                Measures the variance between budgeted and actual expenditure composition. 
                Shows strategic allocation adherence and predictability of sector funding.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Render chart
        indicator_tab2 = "PEFA: PI-2 Expenditure composition outturn"
        uv.render_indicator_section(
            df=df_display,
            indicator_label=indicator_tab2,
            title="",
            description="",
            chart_type="line",
            selected_countries=display_filters.get('selected_countries'),
            year_range=display_filters.get('year_range'),
            chart_options={'x': 'year', 'y': 'value', 'color': 'country_or_area'},
            show_data_table=True,
            container_key="topic4_1_ind2_chart"
        )
        
        # Learn More Expander
        with st.expander("Learn more about this indicator"):
            tab_def, tab_rel, tab_proxy = st.tabs(["Definition", "Relevance", "Proxy Justification"])
            with tab_def:
                st.markdown("Variance in expenditure composition compared to the original budget by functional classification.")
            with tab_rel:
                st.markdown("- **Efficiency**: Strategic allocation adherence.  \n- **Effectiveness**: Predictability of sector funding.")
            with tab_proxy:
                st.markdown("PEFA standard indicator.")

# ========================================
# SECTION: Geographic Distribution
# ========================================
st.markdown("### Geographic Distribution")

col_map, col_insight = st.columns([2, 1], gap="large")

# Left: Maps in Tabs
with col_map:
    tab_map1, tab_map2 = st.tabs(["Indicator 4.1.1", "Indicator 4.1.2"])
    
    with tab_map1:
        st.markdown("<h5 style='color: #002B7F; font-weight: 700;'>Regional Overview - Aggregate Expenditure Outturn</h5>", unsafe_allow_html=True)
        uv.render_indicator_map(
            df=df_display,
            indicator_label=indicator_tab1,
            title="",
            description="",
            reference_data=ref_data,
            year_range=display_filters.get('year_range'),
            map_options={
                'color_continuous_scale': 'Viridis',
                'range_color': [0, 4]
            },
            container_key="topic4_1_map1"
        )
    
    with tab_map2:
        st.markdown("<h5 style='color: #002B7F; font-weight: 700;'>Regional Overview - Expenditure Composition Outturn</h5>", unsafe_allow_html=True)
        uv.render_indicator_map(
            df=df_display,
            indicator_label=indicator_tab2,
            title="",
            description="",
            reference_data=ref_data,
            year_range=display_filters.get('year_range'),
            map_options={
                'color_continuous_scale': 'Plasma',
                'range_color': [0, 4]
            },
            container_key="topic4_1_map2"
        )

# Right: Key Insights
with col_insight:
    st.markdown("""
    <div class='insight-card'>
        <h4>Key Insights</h4>
        <ul style="color: #555; line-height: 1.8;">
            <li><strong>Budget Credibility:</strong> Countries with consistent expenditure alignment demonstrate stronger fiscal frameworks and better planning capacity.</li>
            <li><strong>Predictable Funding:</strong> Lower variance in composition ensures predictable resource flow to priority sectors.</li>
            <li><strong>Strategic Allocation:</strong> Adherence to planned expenditure composition reflects effective policy implementation.</li>
            <li><strong>Development Impact:</strong> Efficient public expenditure management is crucial for achieving sustainable development outcomes.</li>
        </ul>
    </div>
    
    <div class='insight-card' style='margin-top: 1.5rem;'>
        <h4>Data Sources</h4>
        <p style="color: #555; line-height: 1.6;"><strong>Primary Source:</strong> Public Expenditure and Financial Accountability (PEFA) Framework</p>
        <p style="color: #555; line-height: 1.6;"><strong>Coverage:</strong> Multi-country assessments with periodic updates</p>
        <p style="color: #555; line-height: 1.6;"><strong>Methodology:</strong> Standardized assessment framework for public financial management systems</p>
    </div>
    """, unsafe_allow_html=True)

# ========================================
# SECTION: Data Gaps / Availability
# ========================================
all_indicators_4_1 = {
    "Aggregate Expenditure Outturn (4.1.1)": "PEFA: PI-1 Aggregate expenditure out-turn",
    "Expenditure Composition Outturn (4.1.2)": "PEFA: PI-2 Expenditure composition outturn"
}
africa_countries = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
df_africa = df_main[df_main['country_or_area'].isin(africa_countries)]

# Calculate coverage summary
countries_with_data = df_africa[df_africa['indicator_label'].isin(all_indicators_4_1.values())]['country_or_area'].nunique()
total_africa_countries = len(africa_countries)
coverage = round((countries_with_data / total_africa_countries * 100)) if total_africa_countries > 0 else 0

st.markdown(f"""
<div class="data-availability-box">
  <div class="left">
    <h4>Data Availability in Africa</h4>
    <p>
      Data availability determines how confidently we can interpret trends across Africa. 
      This view highlights which countries report recent data and where gaps persist — often due to differences in statistical capacity, reporting cycles, or institutional coverage.
    </p>
    <p><strong>Use the heatmap below to explore:</strong></p>
    <ul>
      <li><strong>Countries with up-to-date reporting</strong> (strong coverage)</li>
      <li><strong>Countries with partial or outdated data</strong></li>
      <li><strong>Indicators missing post-2021 updates</strong></li>
    </ul>
    <p style="margin-top: 1rem;"><em>Current data coverage: {coverage}% of African countries</em></p>
  </div>
  <div class="centre"> 
  <p><strong>Legend:</strong></p>
    <ul style="text-align: left;">
      <li><strong>Dark cells:</strong> Recent, consistent reporting (post-2020)</li>
      <li><strong>Light cells:</strong> Partial or outdated reporting</li>
      <li><strong>Empty cells:</strong> Missing or unreported values</li>
    </ul>
    <p><em>Hover over a cell in the heatmap below to view country-year coverage.</em></p>
  </div>
</div>
""", unsafe_allow_html=True)

with st.expander("View data availability heatmap", expanded=False):
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
