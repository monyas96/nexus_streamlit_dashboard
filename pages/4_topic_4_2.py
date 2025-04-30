import streamlit as st
import pandas as pd
import sys
from pathlib import Path
# Removed pydeck import

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

# --- Remove Temporary Debug: Print relevant indicator names ---
# if 'indicator_label' in df_main.columns:
#     all_indicators = df_main['indicator_label'].dropna().unique()
#     tax_indicators_in_data = sorted([ind for ind in all_indicators if "taxpayer" in ind.lower() or "ataf" in ind.lower()])
#     if tax_indicators_in_data:
#         with st.expander("DEBUG: Found Taxpayer/ATAF Indicators in Data"):
#             st.write(tax_indicators_in_data)
#     else:
#         st.warning("DEBUG: No indicators containing 'taxpayer' or 'ATAF' found in the loaded data.")
# --- End Remove Temporary Debug ---

# --- Sidebar Filters ---
filters = uv.setup_sidebar_filters(ref_data, df_main, key_prefix="topic4_2")

# --- Filter Main Data ---
df_filtered = uv.filter_dataframe_by_selections(df_main, filters, ref_data)

# --- REMOVE START: Debugging Output ---
# with st.expander("🐞 DEBUG: Filtered Data Info", expanded=False):
#     st.write("**Selected Filters:**", filters)
#     st.write(f"**df_main rows:** {len(df_main)}")
#     st.write(f"**df_filtered rows:** {len(df_filtered)}")
#     if not df_filtered.empty:
#         st.write("**Sample of df_filtered:**")
#         st.dataframe(df_filtered.head())
#         # Check specifically for one of the problematic indicators
#         map_indicator_debug = "Tax Revenue - % of GDP - value" # Use one of the labels
#         check_indicator_data = df_filtered[df_filtered['indicator_label'] == map_indicator_debug]
#         st.write(f"**Rows in df_filtered for '{map_indicator_debug}':** {len(check_indicator_data)}")
#         if not check_indicator_data.empty:
#              st.dataframe(check_indicator_data.head())
#     else:
#         st.write("df_filtered is empty after applying sidebar selections.")
# --- REMOVE END: Debugging Output ---

# === Title and Home Button ===
col1, col2 = st.columns([0.8, 0.1])
with col1:
    st.title("📊 Topic 4.2: Budget and Tax Revenues")
with col2:
    st.page_link("pages/0_home.py", label="🏠 Back to Home")

# === Intro ===
st.markdown("""
Budget and tax revenues are crucial for ensuring that governments have the financial resources necessary to fund essential services and development initiatives.
**Efficient and effective management of tax revenues helps reduce dependency on external financing, enhance fiscal stability, and direct resources toward national priorities.**
""" + "") # Corrected concatenation error

# === Tabs Start Immediately After Intro ===
tab1, tab2 = st.tabs([
    "🧾 4.2.1: Tax Revenue Collection",
    "🧾 4.2.2: Tax Administration Efficiency"
])

# === Tab 1: 4.2.1 ===
with tab1:
    # --- Map for Tax Revenue % GDP ---
    st.markdown("#### Geographical Distribution (Tax Revenue % GDP)")
    indicator_tab1_main = "Tax Revenue - % of GDP - value" # Main indicator for this tab
    uv.render_indicator_map(
        df=df_filtered,
        indicator_label=indicator_tab1_main,
        title="", # No title needed, context from tab
        description="Latest available Tax Revenue as % of GDP.",
        reference_data=ref_data,
        year_range=filters.get('year_range'),
        map_options={'color_continuous_scale': 'Blues'},
        container_key="topic4_2_tab1_map" # Unique key for this map
    )
    st.divider()

    # --- Chart for Tax Revenue % GDP (Existing) ---
    # indicator_tax_rev = "Tax Revenue - % of GDP - value" # Already defined above
    uv.render_indicator_section(
        df=df_filtered,
        indicator_label=indicator_tab1_main,
        title="Indicator 4.2.1.1: Tax Revenue as % of GDP",
        description="Measures the total tax revenue collected as a proportion of the country's GDP.",
        chart_type="line", # Show trend over time
        selected_countries=filters.get('selected_countries'),
        year_range=filters.get('year_range'),
        chart_options={'x': 'year', 'y': 'value', 'color': 'country_or_area'}, # Line chart config
        show_data_table=True,
        container_key="topic4_2_tab1_taxrev_chart" # Updated key
    )
    # Expander for Tax Revenue % GDP (Existing)
    with st.expander("🔍 Learn more about Indicator 4.2.1.1"):
        t1_1, t1_2, t1_3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
        with t1_1:
            st.markdown("Measures the total tax revenue collected as a proportion of the country's GDP.")
        with t1_2:
            st.markdown("- **Efficiency**: Shows how well revenue is raised from the economy.  \n- **Effectiveness**: Reflects fiscal independence.")
        with t1_3:
            st.markdown("This World Bank indicator is standard, widely used, and globally comparable.")

    st.divider()

    # --- Indicator: Taxpayer Base Expansion (Using composition chart as proxy) (Existing) ---
    st.markdown("### 🧾 Indicator 4.2.1.2: Taxpayer Base Expansion")
    st.caption("Proxied by Tax Revenue Composition (% of GDP)") # Updated caption to reflect chart

    # --- Inserted Tax Revenue Composition Chart Logic (Existing) ---
    # Define the specific indicators for the composition chart
    tax_composition_indicators = [
        "CIT - % of GDP - Tax Revenue Percent",
        "Income Taxes - % of GDP - Tax Revenue Percent",
        "Excise Taxes - % of GDP - Tax Revenue Percent",
        "Other Taxes - % of GDP - Tax Revenue Percent",
        "Trade Taxes - % of GDP - Tax Revenue Percent",
        "VAT - % of GDP - Tax Revenue Percent"
    ]

    # Filter the main filtered data for these specific indicators
    # (df_filtered is already filtered by sidebar selections)
    df_tax_composition = df_filtered[df_filtered['indicator_label'].isin(tax_composition_indicators)].copy()

    # Add chart type selection
    chart_type_composition = st.radio(
        "Select Chart Type for Composition Proxy:", # Updated label slightly
        ("Line Chart (Trend over Time)", "Stacked Bar Chart (Latest Year by Country)"),
        key="topic4_2_tab1_composition_proxy_chart_type", # Ensure unique key
        horizontal=True
    )

    # Check if data exists after filtering for these indicators
    if not df_tax_composition.empty:
        # Ensure 'value' is numeric
        if pd.api.types.is_numeric_dtype(df_tax_composition['value']):
            try:
                # Create the chart based on selection
                import plotly.express as px
                import plotly.graph_objects as go # Ensure go is imported for empty chart case

                data_table_df = pd.DataFrame() # Initialize for data table

                if chart_type_composition == "Line Chart (Trend over Time)":
                    fig_composition = px.line(
                        df_tax_composition,
                        x='year',
                        y='value',
                        color='indicator_label',
                        hover_data=['country_or_area'],
                        title="Tax Revenue Composition Trend Over Time (% of GDP)",
                        labels={'value': '% of GDP', 'indicator_label': 'Tax Type'},
                        markers=True
                    )
                    fig_composition.update_layout(legend_title_text='Tax Type')
                    st.plotly_chart(fig_composition, use_container_width=True)
                    data_table_df = df_tax_composition # Use full data for table

                elif chart_type_composition == "Stacked Bar Chart (Latest Year by Country)":
                    # Find the latest year *value* for each country/region average
                    df_tax_composition['latest_year'] = df_tax_composition.groupby('country_or_area')['year'].transform('max')
                    # Filter to keep only rows matching the latest year for each country/region
                    df_latest_composition = df_tax_composition[df_tax_composition['year'] == df_tax_composition['latest_year']].copy()
                    # Drop the temporary column
                    df_latest_composition = df_latest_composition.drop(columns=['latest_year'])

                    if df_latest_composition.empty:
                         st.warning("Could not extract latest year data for the stacked bar chart.")
                         fig_composition = go.Figure().update_layout(title="Stacked Bar Chart (No Data for Latest Year)", height=300)
                         st.plotly_chart(fig_composition, use_container_width=True)
                         data_table_df = pd.DataFrame() # Empty df for table
                    else:
                        # Get the actual latest years to display in caption (handle potential multiple rows per country)
                        latest_year_map = df_latest_composition[['country_or_area', 'year']].drop_duplicates().set_index('country_or_area')['year'].to_dict()
                        year_text = ", ".join([f"{country} ({year})" for country, year in latest_year_map.items()])

                        fig_composition = px.bar(
                            df_latest_composition,
                            x='country_or_area',
                            y='value',
                            color='indicator_label',
                            title="Tax Revenue Composition (% GDP) - Latest Available Year by Country",
                            labels={'value': '% of GDP', 'indicator_label': 'Tax Type', 'country_or_area': 'Country'},
                            barmode='stack'
                        )
                        fig_composition.update_layout(legend_title_text='Tax Type')
                        st.plotly_chart(fig_composition, use_container_width=True)
                        st.caption(f"Showing latest available year per country/region: {year_text}")
                        data_table_df = df_latest_composition # Use latest data for table

                # Optional: Show data table for the displayed chart (check if data exists)
                if not data_table_df.empty:
                    if st.checkbox("Show Data Table for Composition Proxy Chart", key="topic4_2_tab1_composition_proxy_table_cb"):
                        st.dataframe(data_table_df[['country_or_area', 'year', 'indicator_label', 'value']].sort_values(by=['country_or_area', 'indicator_label', 'year']))

            except Exception as e:
                st.error(f"An error occurred while creating the tax composition proxy chart: {e}")
        else:
             st.warning(f"Cannot create chart: The 'value' column for one or more required tax composition indicators is not numeric (dtype: {df_tax_composition['value'].dtype}).")

    else:
        st.warning(f"No data found for the required tax composition indicators used as proxy for the selected filters: {filters.get('selected_countries')}, Years: {filters.get('year_range')}")
        st.caption(f"Required indicators for proxy: {', '.join(tax_composition_indicators)}")
    # --- END: Inserted Tax Revenue Composition Chart Logic ---

    # --- Keep the expander (Existing) ---
    with st.expander("🔍 Learn more about Indicator 4.2.1.2"):
        b1, b2, b3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
        with b1:
            st.markdown("Tracks growth in registered taxpayers to assess compliance and coverage.")
        with b2:
            st.markdown("- **Efficiency**: Reflects broadening of the tax system.  \n- **Effectiveness**: Signals outreach and inclusion.")
        with b3:
            st.markdown("ATAF metrics on large taxpayer units and general taxpayer growth are used as a proxy. **Chart above shows Domestic Revenue trend.**") # Added note to justification

# === Tab 2: 4.2.2 ===
with tab2:
    # --- START: Map Section for Tab 2 Indicators ---
    st.markdown("#### Geographical Distribution")

    map_indicators_tab2 = {
        "Tax Effort Ratio": "Tax effort (ratio) [tax_eff]",
        "Tax Buoyancy": "Tax buoyancy [by_tax]"
    }

    selected_map_indicator_name_tab2 = st.selectbox(
        "Select Indicator for Map View:",
        options=list(map_indicators_tab2.keys()),
        key="topic4_2_tab2_map_indicator_select"
    )
    map_indicator_label_tab2 = map_indicators_tab2[selected_map_indicator_name_tab2]
    # st.markdown(f"**Map:** {selected_map_indicator_name_tab2}") # Optional: Show which indicator is mapped

    uv.render_indicator_map(
        df=df_filtered,
        indicator_label=map_indicator_label_tab2,
        title="", # No title needed, context from tab/selection
        description=f"Latest available data for {selected_map_indicator_name_tab2}.",
        reference_data=ref_data,
        year_range=filters.get('year_range'),
        map_options={'color_continuous_scale': 'YlGnBu'}, # Example color scale
        container_key="topic4_2_tab2_map" # Unique key for this map
    )
    st.divider()
    # --- END: Map Section for Tab 2 Indicators ---

    # --- Indicator 4.2.2.1: Tax Collection Efficiency Score (Using Data Proxy) ---
    st.markdown("### 📈 Indicator 4.2.2.1: Tax Collection Efficiency Score")
    indicator_tab2_eff = "Tax effort (ratio) [tax_eff]" # Proxy indicator label
    st.caption(f"Proxied by: {indicator_tab2_eff}") # Updated caption

    # --- Render chart instead of image ---
    uv.render_indicator_section(
        df=df_filtered,
        indicator_label=indicator_tab2_eff,
        title="", # Title handled by markdown above
        description="Trend of the tax effort ratio.",
        chart_type="line", # Line chart for trend
        selected_countries=filters.get('selected_countries'),
        year_range=filters.get('year_range'),
        chart_options={'x': 'year', 'y': 'value', 'color': 'country_or_area'},
        show_data_table=True,
        container_key="topic4_2_tab2_eff_chart"
    )

    # --- Keep Expander ---
    with st.expander("🔍 Learn more about Indicator 4.2.2.1"):
        c1, c2, c3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
        with c1:
            st.markdown("Ratio of actual to potential revenue – showing how much is captured from total capacity.")
        with c2:
            st.markdown("- **Efficiency**: Shows capacity of collection systems.  \n- **Effectiveness**: Closes gaps between potential and actual.")
        with c3:
            st.markdown("Tax effort is a widely recognized proxy in global evaluations. **Chart above shows Tax effort (ratio) [tax_eff] trend.**") # Updated justification note

    st.divider()

    # --- Indicator 4.2.2.2: Reduction in Tax Evasion (Using Data Proxy) ---
    st.markdown("### 🚫 Indicator 4.2.2.2: Reduction in Tax Evasion")
    indicator_tab2_buoy = "Tax buoyancy [by_tax]" # Proxy indicator label
    st.caption(f"Proxied by: {indicator_tab2_buoy}") # Updated caption

    # --- Render chart instead of image ---
    uv.render_indicator_section(
        df=df_filtered,
        indicator_label=indicator_tab2_buoy,
        title="", # Title handled by markdown above
        description="Trend of tax buoyancy.",
        chart_type="line", # Line chart for trend
        selected_countries=filters.get('selected_countries'),
        year_range=filters.get('year_range'),
        chart_options={'x': 'year', 'y': 'value', 'color': 'country_or_area'},
        show_data_table=True,
        container_key="topic4_2_tab2_buoy_chart"
    )

    # --- Keep Expander ---
    with st.expander("🔍 Learn more about Indicator 4.2.2.2"):
        d1, d2, d3 = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
        with d1:
            st.markdown("Estimates the reduction in tax evasion over time.")
        with d2:
            st.markdown("- **Efficiency**: Reflects stronger enforcement.  \n- **Effectiveness**: Reduces informal leakages.")
        with d3:
            st.markdown("ATAF and OECD's buoyancy data show responsiveness of tax systems to growth. **Chart above shows Tax buoyancy [by_tax] trend.**") # Updated justification note

# === REMOVE Data Explorer ===
st.divider()
# uv.create_data_explorer(df_filtered, key_prefix="topic4_2")
