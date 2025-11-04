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
filters = uv.setup_sidebar_filters(ref_data, df_main, key_prefix="topic4_2")
df_filtered = uv.filter_dataframe_by_selections(df_main, filters, ref_data)

# ========================================
# SECTION: Topic Header
# ========================================
with st.container():
    st.markdown("""
    <div class="section-header">
        <h1>Topic 4.2: Budget and Tax Revenues</h1>
        <p>Budget and tax revenues are crucial for ensuring that governments have the financial resources necessary to fund essential services and development initiatives. Efficient and effective management of tax revenues helps reduce dependency on external financing, enhance fiscal stability, and direct resources toward national priorities.</p>
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
        selected_sources = st.multiselect(
            "Data Source",
            options=["World Bank", "IMF", "OECD"],
            default=["World Bank"],
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

# Indicator 4.2.1 - Left Column
with col1:
    with st.container():
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.2.1: Tax Revenue Collection</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 1rem;">
                Measures the total tax revenue collected as a proportion of the country's GDP.
                This indicator shows how well revenue is raised from the economy and reflects fiscal independence.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Render chart
        indicator_1 = "Tax Revenue - % of GDP - value"
    uv.render_indicator_section(
            df=df_display,
            indicator_label=indicator_1,
        title="",
            description="",
        chart_type="line",
            selected_countries=display_filters.get('selected_countries'),
            year_range=display_filters.get('year_range'),
        chart_options={'x': 'year', 'y': 'value', 'color': 'country_or_area'},
        show_data_table=True,
            container_key="topic4_2_ind1_chart"
    )
        
        # Learn More Expander
        with st.expander("Learn more about this indicator"):
            tab_def, tab_rel, tab_proxy = st.tabs(["Definition", "Relevance", "Proxy Justification"])
            with tab_def:
                st.markdown("Measures the total tax revenue collected as a proportion of the country's GDP.")
            with tab_rel:
                st.markdown("- **Efficiency**: Shows how well revenue is raised from the economy.  \n- **Effectiveness**: Reflects fiscal independence.")
            with tab_proxy:
                st.markdown("This World Bank indicator is standard, widely used, and globally comparable.")

# Indicator 4.2.2 - Right Column
with col2:
    with st.container():
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.2.2: Tax Collection Efficiency</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 1rem;">
                Ratio of actual to potential revenue showing how much is captured from total capacity.
                This indicator shows the capacity of collection systems and closes gaps between potential and actual revenue.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Render chart
        indicator_2 = "Tax effort (ratio) [tax_eff]"
    uv.render_indicator_section(
            df=df_display,
            indicator_label=indicator_2,
        title="",
            description="",
        chart_type="line",
            selected_countries=display_filters.get('selected_countries'),
            year_range=display_filters.get('year_range'),
        chart_options={'x': 'year', 'y': 'value', 'color': 'country_or_area'},
        show_data_table=True,
            container_key="topic4_2_ind2_chart"
    )
        
        # Learn More Expander
        with st.expander("Learn more about this indicator"):
            tab_def, tab_rel, tab_proxy = st.tabs(["Definition", "Relevance", "Proxy Justification"])
            with tab_def:
                st.markdown("Ratio of actual to potential revenue – showing how much is captured from total capacity.")
            with tab_rel:
                st.markdown("- **Efficiency**: Shows capacity of collection systems.  \n- **Effectiveness**: Closes gaps between potential and actual.")
            with tab_proxy:
                st.markdown("Tax effort is a widely recognized proxy in global evaluations.")

# ========================================
# SECTION: Geographic Distribution
# ========================================
st.markdown("### Geographic Distribution")

col_map, col_insight = st.columns([2, 1], gap="large")

# Left: Maps in Tabs
with col_map:
    tab_map1, tab_map2 = st.tabs(["Tax Revenue", "Tax Efficiency"])
    
    with tab_map1:
        st.markdown("<h5 style='color: #002B7F; font-weight: 700;'>Regional Overview - Tax Revenue as % of GDP</h5>", unsafe_allow_html=True)
        uv.render_indicator_map(
            df=df_display,
            indicator_label=indicator_1,
            title="",
            description="",
            reference_data=ref_data,
            year_range=display_filters.get('year_range'),
            map_options={
                'color_continuous_scale': 'Blues',
                'range_color': [0, 40]
            },
            container_key="topic4_2_map1"
        )
    
    with tab_map2:
        st.markdown("<h5 style='color: #002B7F; font-weight: 700;'>Regional Overview - Tax Collection Efficiency</h5>", unsafe_allow_html=True)
    uv.render_indicator_map(
            df=df_display,
            indicator_label=indicator_2,
        title="",
            description="",
        reference_data=ref_data,
            year_range=display_filters.get('year_range'),
            map_options={
                'color_continuous_scale': 'YlGnBu',
                'range_color': [0, 2]
            },
            container_key="topic4_2_map2"
        )

# Right: Key Insights
with col_insight:
    st.markdown("""
    <div class='insight-card'>
        <h4>Key Insights</h4>
        <ul style="color: #555; line-height: 1.8;">
            <li><strong>Revenue Mobilization:</strong> Higher tax-to-GDP ratios indicate stronger revenue mobilization capacity and reduced reliance on external financing.</li>
            <li><strong>Tax System Efficiency:</strong> Tax effort ratios above 1 show countries are performing better than their structural capacity would predict.</li>
            <li><strong>Fiscal Independence:</strong> Improving tax collection efficiency directly enhances fiscal autonomy and sustainable development financing.</li>
            <li><strong>Regional Variation:</strong> Significant differences exist across African countries in both revenue levels and collection efficiency.</li>
        </ul>
    </div>
    
    <div class='insight-card' style='margin-top: 1.5rem;'>
        <h4>Data Sources</h4>
        <p style="color: #555; line-height: 1.6;"><strong>Primary Source:</strong> World Bank Development Indicators, IMF Government Finance Statistics</p>
        <p style="color: #555; line-height: 1.6;"><strong>Coverage:</strong> Annual data with country-specific availability</p>
        <p style="color: #555; line-height: 1.6;"><strong>Methodology:</strong> Standardized reporting frameworks ensuring cross-country comparability</p>
    </div>
    """, unsafe_allow_html=True)

# ========================================
# SECTION: Data Gaps / Availability
# ========================================
all_indicators_4_2 = {
    "Tax Revenue as % of GDP (4.2.1)": "Tax Revenue - % of GDP - value",
    "Tax Effort Ratio (4.2.2)": "Tax effort (ratio) [tax_eff]",
    "Tax Buoyancy": "Tax buoyancy [by_tax]"
}
africa_countries = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
df_africa = df_main[df_main['country_or_area'].isin(africa_countries)]

# Calculate coverage summary
countries_with_data = df_africa[df_africa['indicator_label'].isin(all_indicators_4_2.values())]['country_or_area'].nunique()
total_africa_countries = len(africa_countries)
coverage = round((countries_with_data / total_africa_countries * 100)) if total_africa_countries > 0 else 0

st.markdown(f"""
<div class="data-availability-box">
  <div class="left">
    <h4>Data Availability in Africa</h4>
    <p>
      Data availability determines how confidently we can interpret tax revenue trends across Africa. 
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
  <div class="right">
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
        options=list(all_indicators_4_2.keys()),
        key="topic4_2_gap_indicator_select"
    )
    uv.render_data_availability_heatmap(
        df=df_africa,
        indicator_label=all_indicators_4_2[selected_gap_indicator],
        title=f"Data Availability for {selected_gap_indicator} (Africa)",
        container_key="topic4_2_gap"
    )
