import sys
from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import streamlit as st
import pandas as pd
import composite_indicator_methods as cim
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
ref_data = uv.load_country_reference_data()
df_main = uv.load_main_data()

if df_main.empty or ref_data.empty:
    st.error("Failed to load essential data (main data or reference data). Page rendering stopped.")
    st.stop()

# --- Sidebar Filters ---
filters = uv.setup_sidebar_filters(ref_data, df_main, key_prefix="topic4_3")
df_filtered = uv.filter_dataframe_by_selections(df_main, filters, ref_data)

# ========================================
# SECTION: Topic Header
# ========================================
with st.container():
    st.markdown("""
    <div class="section-header">
        <h1>Topic 4.3: Capital Markets</h1>
        <p>Capital markets are essential for mobilizing domestic financial resources and channeling savings into productive investments. A well-developed capital market reduces reliance on foreign financing, supports sustainable economic growth, and strengthens financial stability. Effective management of capital markets ensures that resources are directed toward areas that maximize national development.</p>
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
            options=["World Bank", "IMF"],
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
# SECTION: Key Indicators (3 columns with expandable cards)
# ========================================
st.markdown("### Key Indicators Overview")

# Calculate Stock Market Capitalization to GDP
required_labels_stock_cap = [
    'Market capitalization of listed domestic companies (current US$)',
    'GDP (current US$)'
]
calculation_func_stock_cap = lambda df: pd.DataFrame({
    'Stock Market Cap to GDP (%)': (df['Market capitalization of listed domestic companies (current US$)'] / df['GDP (current US$)']) * 100
}).reset_index()
df_stock_cap, missing_stock_cap = cim.calculate_indicator_with_gap(
    df_display, required_labels_stock_cap, calculation_func_stock_cap
)
df_stock_cap['indicator_label'] = 'Stock Market Cap to GDP (%)'
df_stock_cap = df_stock_cap.rename(columns={'Stock Market Cap to GDP (%)': 'value'})

col1, col2, col3 = st.columns(3, gap="medium")

# Indicator 4.3.1 - Left Column
with col1:
    st.markdown("""
    <div class='indicator-card'>
        <h4>Indicator 4.3.1: Stock Market Capitalization to GDP</h4>
        <p style="color: #555; line-height: 1.6; margin-bottom: 0.8rem;">
            Measures total value of listed companies as a percentage of GDP.
            This indicator shows capital mobilization capacity and links to sectoral investment.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("View Chart and Data", expanded=False):
        # Render chart
        if not df_stock_cap.empty:
            uv.render_indicator_section(
                df=df_stock_cap,
                indicator_label='Stock Market Cap to GDP (%)',
                title="",
                description="",
                chart_type="line",
                selected_countries=display_filters.get('selected_countries'),
                year_range=display_filters.get('year_range'),
                chart_options={'x': 'year', 'y': 'value', 'color': 'country_or_area'},
                show_data_table=False,
                container_key="topic4_3_ind1_chart"
            )
            
            # Data table checkbox (outside of nested expander)
            if st.checkbox("Show Data Table", key="data_table_431"):
                st.dataframe(df_stock_cap[['country_or_area', 'year', 'value']].sort_values(by=['country_or_area', 'year']))
        else:
            st.info("Insufficient data to calculate Stock Market Cap to GDP ratio for selected filters.")
        
        # Learn More sub-tabs
        st.markdown("---")
        st.markdown("**Learn More:**")
        tab_def, tab_rel, tab_proxy = st.tabs(["Definition", "Relevance", "Source"])
        with tab_def:
            st.markdown("Measures total value of listed companies as a % of GDP.")
        with tab_rel:
            st.markdown("- **Efficiency**: Capital mobilization.  \n- **Effectiveness**: Links to sectoral investment.")
        with tab_proxy:
            st.markdown("No proxy needed. Source: World Bank.")

# Indicator 4.3.2 - Middle Column
with col2:
    st.markdown("""
    <div class='indicator-card'>
        <h4>Indicator 4.3.2: Domestic Credit to GDP</h4>
        <p style="color: #555; line-height: 1.6; margin-bottom: 0.8rem;">
            Measures the financial resources provided to the private sector by financial corporations as a percentage of GDP.
            This indicator reflects credit allocation efficiency and supports business growth and investment.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("View Chart and Data", expanded=False):
        # Render chart
        indicator_2 = "Domestic credit provided by financial sector (% of GDP)"
        uv.render_indicator_section(
            df=df_display,
            indicator_label=indicator_2,
            title="",
            description="",
            chart_type="line",
            selected_countries=display_filters.get('selected_countries'),
            year_range=display_filters.get('year_range'),
            chart_options={'x': 'year', 'y': 'value', 'color': 'country_or_area'},
            show_data_table=False,
            container_key="topic4_3_ind2_chart"
        )
        
        # Data table checkbox (outside of nested expander)
        df_credit_data = df_display[df_display['indicator_label'] == indicator_2]
        if not df_credit_data.empty:
            if st.checkbox("Show Data Table", key="data_table_432"):
                st.dataframe(df_credit_data[['country_or_area', 'year', 'value']].sort_values(by=['country_or_area', 'year']))
        
        # Learn More sub-tabs
        st.markdown("---")
        st.markdown("**Learn More:**")
        tab_def, tab_rel, tab_proxy = st.tabs(["Definition", "Relevance", "Source"])
        with tab_def:
            st.markdown("Measures the financial resources provided to the private sector by financial corporations as a percentage of GDP.")
        with tab_rel:
            st.markdown("- **Efficiency**: Credit allocation.  \n- **Effectiveness**: Supports business growth and investment.")
        with tab_proxy:
            st.markdown("World Bank direct indicator.")

# Indicator 4.3.3 - Right Column
with col3:
    st.markdown("""
    <div class='indicator-card'>
        <h4>Indicator 4.3.3: Institutional Investors</h4>
        <p style="color: #555; line-height: 1.6; margin-bottom: 0.8rem;">
            Institutional investors—especially public pension funds—are playing an increasingly important role in mobilizing long-term capital in Africa. 
            <strong>Approximately 92% of pension fund assets on the continent are concentrated in South Africa, Nigeria, Kenya, Namibia, and Botswana</strong><sup>1</sup>. 
            Most African pension funds invest primarily in domestic capital markets, often due to regulatory requirements and limited viable foreign opportunities.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("View Key Trends and Country Examples", expanded=False):
        st.markdown("""
        **Key Trends:**
        
        - Asset allocation remains conservative, with a dominant focus on government bonds and local equities.
        - A gradual shift is underway toward real estate, infrastructure, and private equity, although allocations to these alternative assets are still low.
        - Regulatory reforms in countries like Zambia and Nigeria are enabling co-investment in infrastructure and private equity.
        """)
        
        st.markdown("---")
        st.markdown("**Country Examples:**")
        
        # Create tabs for countries instead of nested expanders
        tab_sa, tab_ng, tab_ke = st.tabs(["South Africa", "Nigeria", "Kenya"])
        
        with tab_sa:
            st.markdown("""
**Overview:**  
South Africa has the most developed pension fund sector in Africa, with significant assets under management.

**Key Characteristics:**
- **Asset Size:** Dominates African pension fund landscape
- **Asset Allocation:** Diversified portfolio including equities, bonds, and alternative investments
- **Regulatory Environment:** Well-established regulatory framework (Pension Funds Act)
- **Investment Focus:** Domestic and international diversification

**Challenges:**
- Pressure to increase local infrastructure investment
- Balancing returns with developmental objectives
- Managing currency risk in international investments
            """)
        
        with tab_ng:
            st.markdown("""
**Overview:**  
Nigeria's pension industry has grown significantly since pension reform in 2004, making it one of Africa's largest.

**Key Characteristics:**
- **Asset Size:** Second-largest pension market in Africa
- **Asset Allocation:** Heavy concentration in government securities and equities
- **Regulatory Environment:** Managed by National Pension Commission (PenCom)
- **Investment Focus:** Primarily domestic investments

**Challenges:**
- Limited investment options outside government bonds
- Infrastructure investment regulations still developing
- Need for greater diversification opportunities
            """)
        
        with tab_ke:
            st.markdown("""
**Overview:**  
Kenya has a dynamic pension sector with both public and private schemes playing important roles.

**Key Characteristics:**
- **Asset Size:** Third-largest pension market in sub-Saharan Africa
- **Asset Allocation:** Government securities, equities, and real estate
- **Regulatory Environment:** Retirement Benefits Authority (RBA) oversight
- **Investment Focus:** Growing interest in alternative assets

**Recent Developments:**
- Increasing allocation to real estate and infrastructure
- Development of private equity investment frameworks
- Cross-border pension portability initiatives within East Africa
            """)

# ========================================
# SECTION: Geographic Distribution
# ========================================
st.markdown("### Geographic Distribution")

col_map, col_insight = st.columns([2, 1], gap="large")

# Left: Maps in Tabs
with col_map:
    tab_map1, tab_map2 = st.tabs(["Stock Market Development", "Domestic Credit"])
    
    with tab_map1:
        st.markdown("<h5 style='color: #002B7F; font-weight: 700;'>Regional Overview - Stock Market Capitalization to GDP</h5>", unsafe_allow_html=True)
        if not df_stock_cap.empty:
            uv.render_indicator_map(
                df=df_stock_cap,
                indicator_label='Stock Market Cap to GDP (%)',
                title="",
                description="",
                reference_data=ref_data,
                year_range=display_filters.get('year_range'),
                map_options={
                    'color_continuous_scale': 'Blues',
                    'range_color': [0, 100]
                },
                container_key="topic4_3_map1"
            )
        else:
            st.info("Insufficient data to display map for selected filters.")
    
    with tab_map2:
        st.markdown("<h5 style='color: #002B7F; font-weight: 700;'>Regional Overview - Domestic Credit to GDP</h5>", unsafe_allow_html=True)
        uv.render_indicator_map(
            df=df_display,
            indicator_label=indicator_2,
            title="",
            description="",
            reference_data=ref_data,
            year_range=display_filters.get('year_range'),
            map_options={
                'color_continuous_scale': 'YlGnBu',
                'range_color': [0, 100]
            },
            container_key="topic4_3_map2"
        )

# Right: Key Insights
with col_insight:
    st.markdown("""
    <div class='insight-card'>
        <h4>Key Insights</h4>
        <ul style="color: #555; line-height: 1.8;">
            <li><strong>Market Depth:</strong> Higher stock market capitalization reflects deeper financial markets and better access to long-term financing.</li>
            <li><strong>Credit Access:</strong> Domestic credit levels indicate the availability of financing for private sector development and investment.</li>
            <li><strong>Financial Inclusion:</strong> Well-functioning capital markets contribute to broader financial inclusion and economic participation.</li>
            <li><strong>Regional Concentration:</strong> Capital markets in Africa remain concentrated in a few countries, with 92% of pension fund assets in South Africa, Nigeria, Kenya, Namibia, and Botswana.</li>
        </ul>
    </div>
    
    <div class='insight-card' style='margin-top: 1.5rem;'>
        <h4>Data Sources</h4>
        <p style="color: #555; line-height: 1.6;"><strong>Primary Source:</strong> World Bank Development Indicators, IMF Financial Access Survey</p>
        <p style="color: #555; line-height: 1.6;"><strong>Coverage:</strong> Annual data with varying country availability</p>
        <p style="color: #555; line-height: 1.6;"><strong>Methodology:</strong> Standardized international reporting frameworks</p>
    </div>
    """, unsafe_allow_html=True)

# ========================================
# SECTION: Data Gaps / Availability
# ========================================
all_indicators_4_3 = {
    "Stock Market Capitalization to GDP (4.3.1)": 'Market capitalization of listed domestic companies (current US$)',
    "Domestic Credit to GDP (4.3.2)": "Domestic credit provided by financial sector (% of GDP)",
    "Pension Fund Assets (4.3.3)": "Pension fund assets to GDP (%)",
    "Bond Market Development": "Portfolio investment, bonds (PPG + PNG) (NFL, current US$)"
}
africa_countries = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
df_africa = df_main[df_main['country_or_area'].isin(africa_countries)]

# Calculate coverage summary
countries_with_data = df_africa[df_africa['indicator_label'].isin(all_indicators_4_3.values())]['country_or_area'].nunique()
total_africa_countries = len(africa_countries)
coverage = round((countries_with_data / total_africa_countries * 100)) if total_africa_countries > 0 else 0

st.markdown(f"""
<div class="data-availability-box">
  <div class="left">
    <h4>Data Availability in Africa</h4>
    <p>
      Data availability determines how confidently we can interpret capital market trends across Africa. 
      This view highlights which countries report recent data and where gaps persist — often due to differences in market development, reporting capacity, or institutional coverage.
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
        options=list(all_indicators_4_3.keys()),
        key="topic4_3_gap_indicator_select"
    )
    uv.render_data_availability_heatmap(
        df=df_africa,
        indicator_label=all_indicators_4_3[selected_gap_indicator],
        title=f"Data Availability for {selected_gap_indicator} (Africa)",
        container_key="topic4_3_gap"
    )
