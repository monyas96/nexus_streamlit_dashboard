import streamlit as st
import pandas as pd
from universal_viz import visualize_indicator, load_main_data, load_country_reference_data, setup_sidebar_filters, filter_dataframe_by_selections
import plotly.graph_objs as go
import altair as alt

# Load data
df = load_main_data("data/nexus.parquet")
country_ref = load_country_reference_data()

# Setup filters
filters = setup_sidebar_filters(country_ref, df, key_prefix="topic4_4")

# Filter data based on selections
filtered_data = filter_dataframe_by_selections(df, filters, country_ref)

# Page title and description
st.title("Topic 4.4: Illicit Financial Flows (IFFs)")
st.markdown("""
This section analyzes illicit financial flows (IFFs) in Africa, including their magnitude, types, and enforcement measures.
""")

# Create tabs
tab1, tab2, tab3 = st.tabs([
    "4.4.1: Magnitude of IFFs",
    "4.4.2: Types of IFFs",
    "4.4.3: Enforcement & Prevention"
])

# === Tab 1: Magnitude of IFFs ===
with tab1:
    # Indicator 4.4.1.1: IFFs as % of GDP
    with st.container():
        st.markdown("### Indicator 4.4.1.1: IFFs as % of GDP")
        st.caption("Proxied by Global Financial Integrity")
        
        try:
            # Filter for the specific indicator
            iffs_data = filtered_data[filtered_data['indicator_label'] == 'IFFs as % of GDP']
            
            if not iffs_data.empty:
                chart = visualize_indicator(
                    df=iffs_data,
                    selected_countries=filters["selected_countries"],
                    year_range=filters["year_range"],
                    chart_type="line",
                    title="IFFs as % of GDP Over Time",
                    y_title="Percentage of GDP"
                )
                st.plotly_chart(chart, use_container_width=True)
                
                # Calculate and display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average %", f"{iffs_data['value'].mean():.1f}%")
                with col2:
                    st.metric("Maximum %", f"{iffs_data['value'].max():.1f}%")
                with col3:
                    st.metric("Minimum %", f"{iffs_data['value'].min():.1f}%")
            else:
                st.info("No data available for IFFs as % of GDP")
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
        
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** Illicit financial flows as a percentage of GDP.  
**Proxy:** Global Financial Integrity estimates.

This indicator shows the relative scale of IFFs compared to the size of the economy.
            """)

    # Indicator 4.4.1.2: Annual IFF Volume
    with st.container():
        st.markdown("### Indicator 4.4.1.2: Annual IFF Volume")
        st.caption("Proxied by Global Financial Integrity")
        
        try:
            # Filter for the specific indicator
            volume_data = filtered_data[filtered_data['indicator_label'] == 'Annual IFF Volume (USD)']
            
            if not volume_data.empty:
                chart = visualize_indicator(
                    df=volume_data,
                    selected_countries=filters["selected_countries"],
                    year_range=filters["year_range"],
                    chart_type="bar",
                    title="Annual IFF Volume by Country",
                    y_title="Volume (USD)"
                )
                st.plotly_chart(chart, use_container_width=True)
                
                # Calculate and display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Volume", f"${volume_data['value'].sum():,.0f}")
                with col2:
                    st.metric("Maximum Volume", f"${volume_data['value'].max():,.0f}")
                with col3:
                    st.metric("Minimum Volume", f"${volume_data['value'].min():,.0f}")
            else:
                st.info("No data available for Annual IFF Volume")
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
        
        with st.expander("Learn more"):
            st.markdown("""
**Definition:** Total value of illicit financial flows in USD.  
**Proxy:** Global Financial Integrity estimates.

This indicator shows the absolute scale of IFFs in monetary terms.
            """)

# === Tab 2: Types of IFFs ===
with tab2:
    # Indicator 4.4.2.1: Trade Mispricing
    with st.container():
        st.markdown("### Indicator 4.4.2.1: Trade Mispricing")
        st.caption("Proxied by GFI Trade Gap Data")
        
        # Define trade mispricing indicators with both label and code
        trade_mispricing_indicators = {
            "Developing vs Advanced Economies (USD Millions)": {
                "label": "The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries and 36 Advanced Economies, 2009–2018, in USD Millions",
                "code": "GFI.TableA.gap_usd_adv",
                "y_title": "Value Gap (USD Millions)",
                "chart_type": "bar"
            },
            "Global Trading Partners (USD Millions)": {
                "label": "The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries and all of their Global Trading Partners, 2009–2018 in USD Millions",
                "code": "GFI.TableE.gap_usd_all",
                "y_title": "Value Gap (USD Millions)",
                "chart_type": "bar"
            },
            "Developing vs Advanced Economies (% of Total Trade)": {
                "label": "The Total Value Gaps Identified Between 134 Developing Countries and 36 Advanced Economies, 2009–2018, as a Percent of Total Trade",
                "code": "GFI.TableC.gap_pct_adv",
                "y_title": "Percent of Total Trade",
                "chart_type": "line"
            },
            "Global Trading Partners (% of Total Trade)": {
                "label": "The Total Value Gaps Identified in Trade Between 134 Developing Countries and all of their Trading Partners, 2009–2018 as a Percent of Total Trade",
                "code": "GFI.TableG.gap_pct_all",
                "y_title": "Percent of Total Trade",
                "chart_type": "line"
            }
        }
        selected_indicator = st.selectbox(
            "Select Trade Mispricing Indicator:",
            options=list(trade_mispricing_indicators.keys()),
            key="trade_mispricing_selector"
        )
        try:
            indicator_details = trade_mispricing_indicators[selected_indicator]
            chart = visualize_indicator(
                df=filtered_data,
                indicator_label=indicator_details["label"],
                indicator_code=indicator_details["code"],
                chart_type=indicator_details["chart_type"],
                title=indicator_details["label"],
                y_title=indicator_details["y_title"],
                x_title="Year",
                color_by="country_or_area",
                show_chart=False
            )
            st.altair_chart(chart, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            st.error(f"Debug info: chart_type={indicator_details['chart_type']}, indicator_label={indicator_details['label']}, indicator_code={indicator_details['code']}")
        
        with st.expander("Learn more about Indicator 4.4.2.1: Trade Mispricing"):
            tab_def, tab_rel, tab_proxy = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
            with tab_def:
                st.markdown("""
Manipulating trade values to illegally shift capital. GFI's bilateral trade mismatch analysis is used as a proxy. The indicators show trade mispricing between developing and advanced economies (USD and % of trade) and with all global trading partners (USD, % of trade, % of GDP). Data covers 2009-2018 for 134 developing countries and 36 advanced economies.
                """)
            with tab_rel:
                st.markdown("""
Trade mispricing is a major channel for illicit financial flows, undermining domestic resource mobilization and economic stability.
                """)
            with tab_proxy:
                st.markdown("""
Proxy justification: GFI's trade gap data is widely used for estimating IFFs due to trade mispricing, as direct measurement is not feasible.
                """)

    # Indicator 4.4.2.2: Tax Evasion
    with st.container():
        st.markdown("### Indicator 4.4.2.2: Tax Evasion")
        st.caption("Proxied by IMF Tax Registration Data")

        # Expanded mapping for both active and inactive indicators
        tax_evasion_label_map = {
            "Active taxpayers on PIT register as percentage of Labor Force": "Active taxpayers on PIT register as % of Labor Force",
            "Active taxpayers on PIT register as percentage of Population": "Active taxpayers on PIT register as % of Population",
            "On PIT register": "Percentage inactive taxpayers on PIT register",
            "On CIT register": "Percentage inactive taxpayers on CIT register",
            "On VAT register": "Percentage inactive taxpayers on VAT register",
            "On PAYE register": "Percentage inactive taxpayers on PAYE register",
            "On Excise register": "Percentage inactive taxpayers on Excise register"
        }

        # Only include labels that exist in your data
        available_labels = [
            label for label in tax_evasion_label_map.keys()
            if label in filtered_data['indicator_label'].unique()
        ]

        # Build dropdown options as display labels
        dropdown_options = [tax_evasion_label_map[label] for label in available_labels]

        selected_display_labels = st.multiselect(
            "Select Tax Evasion Indicators:",
            options=dropdown_options,
            default=dropdown_options,  # Optionally select all by default
            key="tax_evasion_multiselect"
        )

        # Find the raw labels corresponding to the selected display labels
        selected_raw_labels = [
            raw for raw, display in tax_evasion_label_map.items()
            if display in selected_display_labels
        ]

        def get_selected_tax_data():
            return filtered_data[filtered_data['indicator_label'].isin(selected_raw_labels)]

        if selected_raw_labels:
            chart = visualize_indicator(
                df=filtered_data,
                calculation_function=get_selected_tax_data,
                chart_type="line",
                title="Tax Evasion Indicators",
                y_title="Percentage",
                x_title="Year",
                color_by="indicator_label",
                show_chart=False
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("No data available for the selected indicators.")

        with st.expander("Learn more about Indicator 4.4.2.2: Tax Evasion"):
            tab_def, tab_rel, tab_proxy = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
            with tab_def:
                st.markdown("""
Tax evasion indicators measure the share of active and inactive taxpayers on various registers (PIT, CIT, VAT, PAYE, Excise) as a percentage of the labor force or population. Proxied by IMF Tax Registration Data.
                """)
            with tab_rel:
                st.markdown("""
Tax evasion reduces government revenue, limits public investment, and distorts economic incentives.
                """)
            with tab_proxy:
                st.markdown("""
Proxy justification: IMF tax registration data provides a standardized approach to estimate taxpayer activity and evasion across countries.
                """)

    # Indicator 4.4.2.3: Criminal Activities
    with st.container():
        st.markdown("### Indicator 4.4.2.3: Criminal Activities")
        st.caption("Proxied by UNODC Crime Flow Data")
        
        # Remove debugging lines
        # Set chart_type to 'line' for the Criminal Activities indicator
        crime_data = filtered_data[filtered_data['indicator_code'].astype(str).str.strip() == 'UNODC.DPS.losses']
        if not crime_data.empty:
            chart = visualize_indicator(
                df=crime_data,
                indicator_code='UNODC.DPS.losses',
                chart_type="line",
                title="Criminal Activities: Proceeds from Illegal Activities",
                y_title="Value (USD)",
                x_title="Year",
                color_by="country_or_area"
            )
            if chart is not None and isinstance(chart, go.Figure):
                pass  # Removed duplicate chart rendering
            elif chart is not None and isinstance(chart, alt.Chart):
                pass  # Removed duplicate chart rendering
            else:
                st.warning("No chart could be generated for this indicator.")
        else:
            st.info("No data available for Criminal Activities")
        
        with st.expander("Learn more about Indicator 4.4.2.3: Criminal Activities"):
            tab_def, tab_rel, tab_proxy = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
            with tab_def:
                st.markdown("""
**Definition:** Monetary losses (in USD) to drug sales. This indicator is calculated as the amount of drugs seized in kilograms multiplied by the drug price per kilogram. All seizures not measured in grams or kilograms are excluded from the calculation.

**Calculation Methodology:**
- Only drug seizures reported in kilograms or grams are included.
- If the seizure is reported in grams, it is converted to kilograms (1 kg = 1000 g).
- The monetary loss is computed as:  
  `Monetary Loss (USD) = Seizure Quantity (kg) × Drug Price (USD per kg)`
- The total value is aggregated by country and year.
                """)
            with tab_rel:
                st.markdown("""
Criminal activities, such as drug trafficking, are a significant source of illicit financial flows (IFFs), undermining rule of law and economic development. Quantifying the monetary losses from drug sales provides insight into the scale of financial resources diverted from the legal economy.
                """)
            with tab_proxy:
                st.markdown("""
Proxy justification: This indicator uses UNODC drug seizure and price data, which are internationally recognized and reported by national authorities. The methodology ensures comparability and reliability by standardizing units and excluding ambiguous measurements.
                """)

    # Indicator 4.4.2.4: Corruption and Bribery
    with st.container():
        st.markdown("### Indicator 4.4.2.4: Corruption and Bribery")
        st.caption("Proxied by WJP & World Bank Governance Indicators")
        
        try:
            # Filter for the specific indicator
            corruption_data = filtered_data[filtered_data['indicator_label'] == 'Corruption Index Score']
            
            if not corruption_data.empty:
                chart = visualize_indicator(
                    df=corruption_data,
                    chart_type="bar",
                    title="Corruption Index Score",
                    y_title="Score",
                    x_title="Year",
                    color_by="country_or_area"
                )
                st.plotly_chart(chart, use_container_width=True)
                
                # Calculate and display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average Score", f"{corruption_data['value'].mean():.1f}")
                with col2:
                    st.metric("Maximum Score", f"{corruption_data['value'].max():.1f}")
                with col3:
                    st.metric("Minimum Score", f"{corruption_data['value'].min():.1f}")
            else:
                st.info("No data available for Corruption Index")
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
        
        with st.expander("Learn more about Indicator 4.4.2.4: Corruption and Bribery"):
            tab_def, tab_rel, tab_proxy = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
            with tab_def:
                st.markdown("""
Perceptions and incidents of corruption in public/private sectors. Proxied by Control of Corruption index and WJP bribery prevalence score. Calculation method includes normalization and weighting of governance scores.
                """)
            with tab_rel:
                st.markdown("""
Corruption and bribery facilitate IFFs, erode trust in institutions, and hinder sustainable development.
                """)
            with tab_proxy:
                st.markdown("""
Proxy justification: The Control of Corruption index and WJP Rule of Law indicators are internationally recognized proxies for corruption and bribery.
                """)

# === Tab 3: Enforcement & Prevention ===
with tab3:
    st.info("This section is under development. Check back later for updates on enforcement and prevention measures.")
