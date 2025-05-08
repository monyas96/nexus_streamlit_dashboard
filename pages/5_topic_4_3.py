import sys
from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import streamlit as st
import pandas as pd
from utils import render_logo_header
import composite_indicator_methods as cim
import universal_viz as uv
from special_pages.tab_4_3_3 import render_tab_4_3_3

# Country flag mapping (define at the very top to avoid NameError)
country_flags = {
    "South Africa": "🇿🇦",
    "Nigeria": "🇳🇬",
    "Kenya": "🇰🇪",
    "Rwanda": "🇷🇼",
    "Ghana": "🇬🇭"
}

render_logo_header()
# === Top Bar ===
col1, col2 = st.columns([0.8, 0.1])
with col1:
    st.title("📊 Topic 4.3: Capital Markets")
with col2:
    st.page_link("pages/0_home.py", label="🏠 Back to Home", use_container_width=True)

# === Intro ===
st.markdown("""
Capital markets are essential for mobilizing domestic financial resources and channeling savings into productive investments.  
A well-developed capital market reduces reliance on foreign financing, supports sustainable economic growth, and strengthens financial stability.  
**Effective management of capital markets ensures that resources are directed toward areas that maximize national development.**
""")

# Add Africa-wide concentration sentence with footnote to the intro of Tab 4.3.3
st.markdown('''In Africa, 92% of pension fund assets are concentrated in South Africa, Nigeria, Kenya, Namibia, and Botswana.<sup>1</sup>''', unsafe_allow_html=True)

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
    st.markdown("The following are the indicators for this subtopic.")
    # 4.3.1.1 Stock Market Capitalization to GDP (calculated)
    required_labels_stock_cap = [
        'Market capitalization of listed domestic companies (current US$)',
        'GDP (current US$)'
    ]
    calculation_func_stock_cap = lambda df: pd.DataFrame({
        'Stock Market Cap to GDP (%)': (df['Market capitalization of listed domestic companies (current US$)'] / df['GDP (current US$)']) * 100
    }).reset_index()
    df_stock_cap, missing_stock_cap = cim.calculate_indicator_with_gap(
        df_filtered, required_labels_stock_cap, calculation_func_stock_cap
    )
    df_stock_cap['indicator_label'] = 'Stock Market Cap to GDP (%)'
    uv.render_indicator_section(
        df=df_stock_cap.rename(columns={
            'Stock Market Cap to GDP (%)': 'value',
            'country_or_area': 'country_or_area',
            'year': 'year'
        }),
        indicator_label='Stock Market Cap to GDP (%)',
        title="Indicator 4.3.1.1: Stock Market Capitalization to GDP",
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
    uv.render_indicator_section(
        df=df_filtered,
        indicator_label="Portfolio investment, bonds (PPG + PNG) (NFL, current US$)",
        title="Indicator 4.3.1.2: Bond Market Development",
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
    required_labels_reserves = [
        'Reserves and related items (BoP, current US$)',
        'External debt stocks, short-term (DOD, current US$)'
    ]
    calculation_func_reserves = lambda df: pd.DataFrame({
        'Adequacy of International Reserves': df['Reserves and related items (BoP, current US$)'] / df['External debt stocks, short-term (DOD, current US$)']
    }).reset_index()
    df_reserves, missing_reserves = cim.calculate_indicator_with_gap(
        df_filtered, required_labels_reserves, calculation_func_reserves
    )
    df_reserves['indicator_label'] = 'Adequacy of International Reserves'
    uv.render_indicator_section(
        df=df_reserves.rename(columns={
            'Adequacy of International Reserves': 'value',
            'country_or_area': 'country_or_area',
            'year': 'year'
        }),
        indicator_label='Adequacy of International Reserves',
        title="Indicator 4.3.1.3: Adequacy of International Reserves",
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

# === Tab 2: Financial Intermediation ===
with tab2:
    st.markdown("The following are the indicators for this subtopic.")
    # 4.3.2.1: Banking Sector Development Index (calculated)
    try:
        required_labels_banking = [
            'Bank capital to assets ratio (%)',
            'Bank liquid reserves to bank assets ratio (%)',
            'Domestic credit provided by financial sector (% of GDP)'
        ]
        calculation_func_banking = lambda df: pd.DataFrame({
            'Banking Sector Development Index': (
                df['Bank capital to assets ratio (%)'] * 0.4 +
                df['Bank liquid reserves to bank assets ratio (%)'] * 0.3 +
                df['Domestic credit provided by financial sector (% of GDP)'] * 0.3
            )
        }).reset_index()
        df_banking_gap, missing_banking = cim.calculate_indicator_with_gap(
            df_main, required_labels_banking, calculation_func_banking
        )
        df_banking_gap['indicator_label'] = 'Banking Sector Development Index'
        df_banking_gap = standardize_gap_df(df_banking_gap, ref_data)
    except Exception:
        df_banking_gap = pd.DataFrame()

    # 4.3.2.2: Domestic Credit to GDP (direct)
    uv.render_indicator_section(
        df=df_filtered,
        indicator_label="Domestic credit provided by financial sector (% of GDP)",
        title="Indicator 4.3.2.2: Domestic Credit to GDP",
        description="Ratio of private sector credit to GDP. Measures the financial resources provided to the private sector by financial corporations.",
        chart_type="line",
        selected_countries=filters.get('selected_countries'),
        year_range=filters.get('year_range'),
        chart_options={'x': 'year', 'y': 'value', 'color': 'country_or_area'},
        show_data_table=True,
        container_key="topic4_3_tab2_domcredit_chart"
    )
    with st.expander("🔍 Learn more about Indicator 4.3.2.2"):
        t2_1, t2_2, t2_3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
        with t2_1:
            st.markdown("Measures the financial resources provided to the private sector by financial corporations as a percentage of GDP.")
        with t2_2:
            st.markdown("- **Efficiency**: Credit allocation.  \n- **Effectiveness**: Supports business growth and investment.")
        with t2_3:
            st.markdown("World Bank direct indicator.")
    st.divider()

    # Geographical Distribution Map Section
    st.markdown("#### Geographical Distribution of Financial Intermediation Indicators")
    df_domcredit_map = df_filtered[df_filtered['indicator_label'] == "Domestic credit provided by financial sector (% of GDP)"]
    if 'Banking Sector Development Index' in df_banking_gap.columns:
        df_banking_index_map = df_banking_gap.rename(columns={'Banking Sector Development Index': 'value'})
        df_banking_index_map['indicator_label'] = 'Banking Sector Development Index'
    else:
        df_banking_index_map = pd.DataFrame()
    map_indicators_tab2 = {
        "Banking Sector Development Index (4.3.2.1)": df_banking_index_map,
        "Domestic Credit to GDP (4.3.2.2)": df_domcredit_map
    }
    selected_map_indicator_tab2 = st.selectbox(
        "Select indicator for map view:",
        options=list(map_indicators_tab2.keys()),
        key="topic4_3_tab2_map_indicator_select"
    )
    df_map_tab2 = map_indicators_tab2[selected_map_indicator_tab2]
    indicator_label_map_tab2 = {
        "Banking Sector Development Index (4.3.2.1)": "Banking Sector Development Index",
        "Domestic Credit to GDP (4.3.2.2)": "Domestic credit provided by financial sector (% of GDP)"
    }
    if not df_map_tab2.empty:
        uv.render_indicator_map(
            df=df_map_tab2,
            indicator_label=indicator_label_map_tab2[selected_map_indicator_tab2],
            title="",
            description=f"Geographical distribution of latest {selected_map_indicator_tab2} values.",
            reference_data=ref_data,
            year_range=filters.get('year_range'),
            map_options={'color_continuous_scale': 'YlGnBu'},
            container_key="topic4_3_tab2_map"
        )
    else:
        st.info(f"No data available for {selected_map_indicator_tab2} to display on the map.")
    st.divider()

# === Tab 3: Institutional Investors ===
with tab3:
    render_tab_4_3_3(filters, ref_data, country_flags, uv, cim)

# === Data Gap Section ---
all_indicators_4_3 = {
    "Stock Market Capitalization to GDP (4.3.1.1)": "Stock Market Cap to GDP (%)",
    "Bond Market Development (4.3.1.2)": "Portfolio investment, bonds (PPG + PNG) (NFL, current US$)",
    "Adequacy of International Reserves (4.3.2.1)": "Adequacy of International Reserves",
    "Banking Sector Development Index (4.3.2.2)": "Banking Sector Development Index"
}

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

# Debug: Inspect df_filtered for required indicators
# st.write('Unique indicator_label values in df_filtered:', df_filtered['indicator_label'].unique())
# st.write('Sample rows for Market Cap in df_filtered:', df_filtered[df_filtered['indicator_label'] == 'Market capitalization of listed domestic companies (current US$)'].head())
# st.write('Sample rows for GDP in df_filtered:', df_filtered[df_filtered['indicator_label'] == 'GDP (current US$)'].head())

# Ensure all calculated DataFrames are defined before the data gap section
try:
    df_stock_cap_gap = cim.calculate_stock_market_cap_to_gdp(df_filtered)
    df_stock_cap_gap['indicator_label'] = 'Stock Market Cap to GDP (%)'
except Exception as e:
    df_stock_cap_gap = pd.DataFrame()

try:
    df_reserves_gap = cim.calculate_adequacy_of_international_reserves(df_filtered)
    df_reserves_gap['indicator_label'] = 'Adequacy of International Reserves'
except Exception as e:
    df_reserves_gap = pd.DataFrame()

try:
    df_bond_gap = df_filtered[df_filtered['indicator_label'] == "Portfolio investment, bonds (PPG + PNG) (NFL, current US$)"].copy()
except Exception as e:
    df_bond_gap = pd.DataFrame()

try:
    # If you have a calculated banking gap, use your calculation here
    df_banking_gap = pd.DataFrame()  # Placeholder, replace with actual calculation if needed
except Exception as e:
    df_banking_gap = pd.DataFrame()

# Combine only calculated DataFrames for the data gap heatmap
try:
    df_gap = pd.concat([df_stock_cap_gap, df_reserves_gap, df_bond_gap, df_banking_gap], ignore_index=True)
except Exception:
    df_gap = pd.DataFrame()

# Debug: Check if df_gap is empty and what columns it has
# st.write("df_gap shape:", df_gap.shape)
# st.write("df_gap columns:", df_gap.columns)
# st.write("df_gap head:", df_gap.head())

# Debug: Check each DataFrame before concatenation
# st.write("df_stock_cap_gap shape/columns:", df_stock_cap_gap.shape, df_stock_cap_gap.columns)
# st.write("df_reserves_gap shape/columns:", df_reserves_gap.shape, df_reserves_gap.columns)
# st.write("df_bond_gap shape/columns:", df_bond_gap.shape, df_bond_gap.columns)
# st.write("df_banking_gap shape/columns:", df_banking_gap.shape, df_banking_gap.columns)

# Only print unique indicator_label values if the column exists
# if 'indicator_label' in df_gap.columns:
#     st.write('Unique indicator_label values in df_gap:', df_gap['indicator_label'].unique())
# else:
#     st.write('No indicator_label column in df_gap. Columns are:', df_gap.columns)

# Filter for African countries
africa_countries = ref_data[ref_data['Region Name'] == 'Africa']['Country or Area'].unique()
df_africa = df_gap[df_gap['country_or_area'].isin(africa_countries)]

st.divider()
with st.expander("Understand the data gap in Africa for this topic"):
    selected_gap_indicator = st.selectbox(
        "Select indicator to view data availability:",
        options=list(all_indicators_4_3.keys()),
        key="topic4_3_gap_indicator_select_data_gap"
    )
    uv.render_data_availability_heatmap(
        df=df_africa,
        indicator_label=all_indicators_4_3[selected_gap_indicator],
        title=f"Data Availability for {selected_gap_indicator} (Africa)",
        container_key="topic4_3_gap",
        all_countries=africa_countries
    )

