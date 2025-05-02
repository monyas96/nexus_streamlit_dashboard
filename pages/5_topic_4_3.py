from pathlib import Path
import sys
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import universal_viz as uv
import streamlit as st
import pandas as pd
from utils import render_logo_header
import composite_indicator_methods as cim

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

# --- Data Loading ---
BASE_DIR = Path(__file__).resolve().parent.parent
ref_data = uv.load_country_reference_data()
df_main = uv.load_main_data()  # Now available from universal_viz.py

# --- Sidebar Filters ---
# Remove custom 'Select region (optional)' selectbox; use only setup_sidebar_filters
filters = uv.setup_sidebar_filters(ref_data, df_main, key_prefix="topic4_3")

# --- Filter Main Data ---
df_filtered = uv.filter_dataframe_by_selections(df_main, filters, ref_data)

# === Tabs for Subtopics/Indicators ===
tab1, tab2, tab3 = st.tabs([
    "📈 4.3.1: Market Capitalization",
    "🏦 4.3.2: Financial Intermediation",
    "💼 4.3.3: Institutional Investors"
])

# === Tab 1: Market Capitalization ===
with tab1:
    # 4.3.1.1 Stock Market Capitalization to GDP (calculated)
    st.markdown("#### Indicator: Stock Market Capitalization to GDP")
    df_stock_cap = cim.calculate_stock_market_cap_to_gdp(df_filtered)
    df_stock_cap['indicator_label'] = 'Stock Market Cap to GDP (%)'
    uv.render_indicator_section(
        df=df_stock_cap.rename(columns={
            'Stock Market Cap to GDP (%)': 'value',
            'country_or_area': 'country_or_area',
            'year': 'year'
        }),
        indicator_label='Stock Market Cap to GDP (%)',
        title="Stock Market Capitalization to GDP (%)",
        description="Total market capitalization of the stock market as a percentage of GDP.",
        chart_type="line",
        selected_countries=filters.get('selected_countries'),
        year_range=filters.get('year_range'),
        chart_options={'x': 'year', 'y': 'value', 'color': 'country_or_area'},
        show_data_table=True,
        container_key="topic4_3_tab1_stockcap_chart"
    )
    with st.expander("ℹ️ Methodology: Stock Market Capitalization to GDP"):
        st.markdown(f"""```
{cim.calculate_stock_market_cap_to_gdp.__doc__}
```""")
    with st.expander("🔍 Learn more about Indicator 4.3.1.1"):
        t1_1, t1_2, t1_3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
        with t1_1:
            st.markdown("Measures total value of listed companies as a % of GDP.")
        with t1_2:
            st.markdown("Efficiency: Capital mobilization  \nEffectiveness: Links to sectoral investment")
        with t1_3:
            st.markdown("No proxy needed. Source: World Bank.")
    st.divider()

    # 4.3.1.2 Bond Market Development (direct)
    st.markdown("#### Indicator: Bond Market Development")
    uv.render_indicator_section(
        df=df_filtered,
        indicator_label="Portfolio investment, bonds (PPG + PNG) (NFL, current US$)",
        title="Bond Market Development",
        description="Portfolio investment, bonds (PPG + PNG) (NFL, current US$)",
        chart_type="line",
        selected_countries=filters.get('selected_countries'),
        year_range=filters.get('year_range'),
        chart_options={'x': 'year', 'y': 'value', 'color': 'country_or_area'},
        show_data_table=True,
        container_key="topic4_3_tab1_bond_chart"
    )
    with st.expander("🔍 Learn more about Indicator 4.3.1.2"):
        t2_1, t2_2, t2_3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
        with t2_1:
            st.markdown("Measures volume of domestic bonds issued and traded.")
        with t2_2:
            st.markdown("Efficiency: Capital raised  \nEffectiveness: Infrastructure & development finance")
        with t2_3:
            st.markdown("Direct indicator.")
    st.divider()

    # 4.3.1.3 Adequacy of International Reserves (calculated)
    st.markdown("#### Indicator: Adequacy of International Reserves")
    df_reserves = cim.calculate_adequacy_of_international_reserves(df_filtered)
    df_reserves['indicator_label'] = 'Adequacy of International Reserves'
    uv.render_indicator_section(
        df=df_reserves.rename(columns={
            'Adequacy of International Reserves': 'value',
            'country_or_area': 'country_or_area',
            'year': 'year'
        }),
        indicator_label='Adequacy of International Reserves',
        title="Adequacy of International Reserves",
        description="Ratio of International Reserves (BoP, current US$) to External Debt Stocks, Short-Term (DOD, Current US$)",
        chart_type="line",
        selected_countries=filters.get('selected_countries'),
        year_range=filters.get('year_range'),
        chart_options={'x': 'year', 'y': 'value', 'color': 'country_or_area'},
        show_data_table=True,
        container_key="topic4_3_tab1_reserves_chart"
    )
    with st.expander("ℹ️ Methodology: Adequacy of International Reserves"):
        st.markdown(f"""```
{cim.calculate_adequacy_of_international_reserves.__doc__}
```""")
    with st.expander("🔍 Learn more about Indicator 4.3.1.3"):
        t3_1, t3_2, t3_3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
        with t3_1:
            st.markdown("Ratio of International Reserves to Short-Term External Debt.")
        with t3_2:
            st.markdown("Efficiency: Reserve sufficiency  \nEffectiveness: Shock protection")
        with t3_3:
            st.markdown("Calculated indicator. See methodology above.")
    st.divider()

    st.markdown("#### Geographical Distribution")

    # Prepare Bond Market Development data for map and graph (use same DataFrame, filter out region averages)
    bond_col = 'Portfolio investment, bonds (PPG + PNG) (NFL, current US$)'
    df_bond_map = pd.DataFrame()
    if 'indicator_label' in df_filtered.columns:
        df_bond_map = df_filtered[
            (df_filtered['indicator_label'] == bond_col) &
            (~df_filtered['country_or_area'].str.contains('Region Average', na=False)) &
            (df_filtered['country_or_area'].notnull())
        ]

    # Ensure calculated indicator DataFrames have the correct 'indicator_label' and 'value' columns
    if 'Stock Market Cap to GDP (%)' in df_stock_cap.columns:
        df_stock_cap = df_stock_cap.rename(columns={'Stock Market Cap to GDP (%)': 'value'})
    if 'Adequacy of International Reserves' in df_reserves.columns:
        df_reserves = df_reserves.rename(columns={'Adequacy of International Reserves': 'value'})
    if 'indicator_label' not in df_stock_cap.columns or not (df_stock_cap['indicator_label'] == 'Stock Market Cap to GDP (%)').all():
        df_stock_cap['indicator_label'] = 'Stock Market Cap to GDP (%)'
    if 'indicator_label' not in df_reserves.columns or not (df_reserves['indicator_label'] == 'Adequacy of International Reserves').all():
        df_reserves['indicator_label'] = 'Adequacy of International Reserves'

    # Concatenate all long-format DataFrames for the map
    df_map_all = pd.concat([
        df_filtered[df_filtered['indicator_label'] != bond_col] if 'indicator_label' in df_filtered.columns else df_filtered,
        df_stock_cap,
        df_reserves,
        df_bond_map
    ], ignore_index=True)

    map_indicators_4_3_1 = {
        "Stock Market Cap to GDP (%)": df_map_all[df_map_all['indicator_label'] == "Stock Market Cap to GDP (%)"],
        "Bond Market Development": df_map_all[df_map_all['indicator_label'] == bond_col],
        "Adequacy of International Reserves": df_map_all[df_map_all['indicator_label'] == "Adequacy of International Reserves"]
    }

    selected_map_indicator = st.selectbox(
        "Select indicator for map view:",
        options=list(map_indicators_4_3_1.keys()),
        key="topic4_3_tab1_map_indicator_select"
    )

    df_map = map_indicators_4_3_1[selected_map_indicator]

    # Remove the year selector for the map (the map will use the year range from the sidebar filter)
    # available_years = []
    # if 'year' in df_map.columns:
    #     available_years = sorted(df_map['year'].dropna().unique())
    # selected_year = None
    # if available_years:
    #     selected_year = st.selectbox(
    #         "Select year for map:",
    #         options=available_years,
    #         index=len(available_years)-1,  # Default to latest year
    #         key=f"topic4_3_tab1_map_year_{selected_map_indicator}"
    #     )
    #     df_map = df_map[df_map['year'] == selected_year]

    with st.expander("🐞 Debug: Map Data", expanded=False):
        st.write("Selected indicator for map:", selected_map_indicator)
        st.write("df_map shape:", df_map.shape)
        st.dataframe(df_map.head())
        st.write("Unique indicator_label values in df_map:")
        st.write(df_map['indicator_label'].unique())
        if 'country_or_area' in df_map.columns:
            st.write("Sample country_or_area values:", df_map['country_or_area'].dropna().unique()[:10])
        else:
            st.write("country_or_area column is missing in df_map!")

    indicator_label_map = {
        "Stock Market Cap to GDP (%)": "Stock Market Cap to GDP (%)",
        "Bond Market Development": "Portfolio investment, bonds (PPG + PNG) (NFL, current US$)",
        "Adequacy of International Reserves": "Adequacy of International Reserves"
    }

    if not df_map.empty:
        uv.render_indicator_map(
            df=df_map,
            indicator_label=indicator_label_map[selected_map_indicator],
            title="",
            description=f"Geographical distribution of latest {selected_map_indicator} values.",
            reference_data=ref_data,
            year_range=filters.get('year_range'),
            map_options={'color_continuous_scale': 'Blues'},
            container_key="topic4_3_tab1_map"
        )
    else:
        st.info(f"No data available for {selected_map_indicator} to display on the map.")
    st.divider()

    # --- Debug Section ---
    with st.expander("🐞 Debug: Data for Calculated Indicators", expanded=False):
        st.markdown("**Stock Market Capitalization to GDP**")
        market_cap_col = 'Market capitalization of listed domestic companies (current US$)'
        gdp_col = 'GDP (current US$)'
        st.write("Filtered DataFrame for required indicators:")
        st.dataframe(df_filtered[df_filtered['indicator_label'].isin([market_cap_col, gdp_col])])
        st.write("Pivoted DataFrame (before dropping NAs):")
        df_pivot_stock = df_filtered[df_filtered['indicator_label'].isin([market_cap_col, gdp_col])].pivot_table(
            index=['country_or_area', 'year'],
            columns='indicator_label',
            values='value'
        )
        st.dataframe(df_pivot_stock)
        st.write("Final Calculated DataFrame:")
        st.dataframe(df_stock_cap)

        st.markdown("**Adequacy of International Reserves**")
        reserves_col = 'International reserves (BoP, current US$)'
        debt_col = 'External debt stocks, short-term (DOD, current US$)'
        st.write("Filtered DataFrame for required indicators:")
        st.dataframe(df_filtered[df_filtered['indicator_label'].isin([reserves_col, debt_col])])
        st.write("Pivoted DataFrame (before dropping NAs):")
        df_pivot_reserves = df_filtered[df_filtered['indicator_label'].isin([reserves_col, debt_col])].pivot_table(
            index=['country_or_area', 'year'],
            columns='indicator_label',
            values='value'
        )
        st.dataframe(df_pivot_reserves)
        st.write("Final Calculated DataFrame:")
        st.dataframe(df_reserves)

# === Tab 2: Financial Intermediation ===
with tab2:
    st.markdown("#### Indicator: Adequacy of International Reserves")
    st.info("[Chart for Adequacy of International Reserves will appear here]")
    with st.expander("🔍 Learn more about Indicator 4.3.2.1"):
        t1_1, t1_2, t1_3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
        with t1_1:
            st.markdown("Ratio of reserves to short-term external debt.")
        with t1_2:
            st.markdown("Efficiency: Reserve sufficiency  \nEffectiveness: Shock protection")
        with t1_3:
            st.markdown("Direct indicator. Source: IMF.")
    st.divider()
    st.markdown("#### Indicator: Banking Sector Development Index")
    st.info("[Chart for Banking Sector Development Index will appear here]")
    with st.expander("🔍 Learn more about Indicator 4.3.2.2"):
        t2_1, t2_2, t2_3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
        with t2_1:
            st.markdown("Captures depth, access, and efficiency of banking systems.")
        with t2_2:
            st.markdown("Efficiency: Credit allocation  \nEffectiveness: Inclusive growth")
        with t2_3:
            st.markdown("Proxy: IMF FAS / World Bank Findex")
    st.divider()
    st.markdown("#### Geographical Distribution")
    st.info("[Map for Financial Intermediation will appear here]")
    st.divider()

# === Tab 3: Institutional Investors ===
with tab3:
    st.markdown("#### Indicator: Private Sector Credit to GDP")
    st.info("[Chart for Private Sector Credit to GDP will appear here]")
    with st.expander("🔍 Learn more about Indicator 4.3.3.1"):
        t1_1, t1_2, t1_3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
        with t1_1:
            st.markdown("Measures credit provided to the private sector as % of GDP.")
        with t1_2:
            st.markdown("Efficiency: Credit expansion  \nEffectiveness: Business growth")
        with t1_3:
            st.markdown("World Bank direct indicator.")
    st.divider()
    st.markdown("#### Indicator: Pension & Sovereign Wealth Fund Investments")
    st.info("[Chart for Pension & SWF Investments will appear here]")
    with st.expander("🔍 Learn more about Indicator 4.3.3.2"):
        t2_1, t2_2, t2_3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
        with t2_1:
            st.markdown("Share of pension/SWF assets invested in national markets.")
        with t2_2:
            st.markdown("Efficiency: Long-term allocation  \nEffectiveness: Domestic economic returns")
        with t2_3:
            st.markdown("Proxies from national fund reports / SWFI database.")
    st.divider()
    st.markdown("#### Geographical Distribution")
    st.info("[Map for Institutional Investors will appear here]")
    st.divider()

# === Data Gap Section ---
all_indicators_4_3 = {
    "Stock Market Capitalization to GDP (4.3.1.1)": "Stock Market Cap to GDP (%)",
    "Bond Market Development (4.3.1.2)": "Portfolio investment, bonds (PPG + PNG) (NFL, current US$)",
    "Adequacy of International Reserves (4.3.2.1)": "Adequacy of International Reserves",
    "Banking Sector Development Index (4.3.2.2)": "Banking Sector Development Index",
    "Private Sector Credit to GDP (4.3.3.1)": "Domestic credit to private sector (% of GDP)",
    "Pension & SWF Investments (4.3.3.2)": "Pension fund assets (% of GDP)"
}

# Standardize and merge calculated indicators with ref_data for data gap

def standardize_gap_df(df, ref_data):
    if not df.empty:
        # Ensure country_or_area column
        if 'country_or_area' not in df.columns and 'Country' in df.columns:
            df['country_or_area'] = df['Country']
        # Merge iso3 if missing
        if 'iso3' not in df.columns and 'country_or_area' in df.columns:
            df = df.merge(ref_data[['Country', 'iso3']], left_on='country_or_area', right_on='Country', how='left')
        # Ensure year is int
        if 'year' in df.columns:
            df['year'] = df['year'].astype(int)
        # Ensure value column exists
        if 'value' not in df.columns and df.shape[1] > 0:
            # Try to rename the last column to value if it's the calculated value
            df.rename(columns={df.columns[-1]: 'value'}, inplace=True)
    return df

try:
    df_stock_cap_gap = cim.calculate_stock_market_cap_to_gdp(df_main)
    df_stock_cap_gap['indicator_label'] = 'Stock Market Cap to GDP (%)'
    df_stock_cap_gap = standardize_gap_df(df_stock_cap_gap, ref_data)
except Exception:
    df_stock_cap_gap = pd.DataFrame()

try:
    df_reserves_gap = cim.calculate_adequacy_of_international_reserves(df_main)
    df_reserves_gap['indicator_label'] = 'Adequacy of International Reserves'
    df_reserves_gap = standardize_gap_df(df_reserves_gap, ref_data)
except Exception:
    df_reserves_gap = pd.DataFrame()

try:
    df_bond_gap = df_main[df_main['indicator_label'] == "Portfolio investment, bonds (PPG + PNG) (NFL, current US$)"].copy()
    df_bond_gap = standardize_gap_df(df_bond_gap, ref_data)
except Exception:
    df_bond_gap = pd.DataFrame()

# Combine all for the data gap heatmap
try:
    df_gap = pd.concat([df_main, df_stock_cap_gap, df_reserves_gap, df_bond_gap], ignore_index=True)
except Exception:
    df_gap = df_main.copy()

africa_countries = ref_data[ref_data['Region'] == 'Africa']['Country'].unique()
df_africa = df_gap[df_gap['country_or_area'].isin(africa_countries) if 'country_or_area' in df_gap.columns else df_gap['Country'].isin(africa_countries)]
st.divider()
with st.expander("Understand the data gap in Africa for this topic"):
    selected_gap_indicator = st.selectbox(
        "Select indicator to view data availability:",
        options=list(all_indicators_4_3.keys()),
        key="topic4_3_gap_indicator_select"
    )
    uv.render_data_availability_heatmap(
        df=df_africa,
        indicator_label=all_indicators_4_3[selected_gap_indicator],
        title=f"Data Availability for {selected_gap_indicator} (Africa)",
        container_key="topic4_3_gap",
        all_countries=africa_countries
    )
