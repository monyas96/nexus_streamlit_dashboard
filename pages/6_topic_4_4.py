import streamlit as st
import pandas as pd
from universal_viz import visualize_indicator, load_main_data, load_country_reference_data, setup_sidebar_filters, filter_dataframe_by_selections
import plotly.graph_objs as go
import altair as alt
from composite_indicator_methods import calculate_corruption_losses

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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "4.4.1: Magnitude of IFFs",
    "4.4.2: Types of IFFs",
    "4.4.3: Detection and Enforcement",
    "4.4.5: Impact on Development Finance",
    "4.4.6: Policy and Regulatory Environment"
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
            corruption_data = filtered_data[filtered_data['indicator_label'] == 'Control of Corruption']
            if not corruption_data.empty:
                latest_corruption = calculate_corruption_losses(corruption_data)
                bar_chart = alt.Chart(latest_corruption).mark_bar().encode(
                    x=alt.X('country_or_area', sort='-y', title='Country'),
                    y=alt.Y('corruption_loss_billion_usd', title='Estimated Corruption Loss (Billion USD, out of 148)'),
                    tooltip=['country_or_area', 'corruption_loss_billion_usd', 'value', 'normalized_score', 'inverted_score']
                ).properties(title='Estimated Annual Corruption Loss by Country (Allocated from $148B, WGI-based, Inverted)', width=700)
                st.altair_chart(bar_chart, use_container_width=True)
                with st.expander("View Calculated Losses Table"):
                    st.dataframe(
                        latest_corruption[['country_or_area', 'year', 'value', 'normalized_score', 'inverted_score', 'corruption_loss_billion_usd']]
                        .sort_values('corruption_loss_billion_usd', ascending=False)
                        .style.format({
                            'value': '{:.2f}',
                            'normalized_score': '{:.3f}',
                            'inverted_score': '{:.3f}',
                            'corruption_loss_billion_usd': '{:.2f}'
                        })
                    )
                st.write(f"Sum of all country losses: {latest_corruption['corruption_loss_billion_usd'].sum():.2f} billion USD")
            else:
                st.info("No data available for Control of Corruption")
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
        
        with st.expander("Learn more about Indicator 4.4.2.4: Corruption and Bribery"):
            tab_def, tab_rel, tab_proxy = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
            with tab_def:
                st.markdown("""
**Calculation Methodology:**

1. **Normalization and Inversion:**
   - Original scores (range: -2.5 to 2.5) are normalized to 0-1 scale
   - Formula: Normalized Score = (Original Score + 2.5) / 5.0
   - **Inversion:** Inverted Score = 1 - Normalized Score (so higher corruption = higher loss)

2. **Weight Assignment:**
   - Each country's inverted score becomes its weight
   - Total weight is calculated as sum of all country weights

3. **Share Calculation:**
   - Country Loss = (Country Weight / Total Weight) × 148
   - 148 is a scaling factor for standardized comparison (billion USD)

**Data Source:** Worldwide Governance Indicators (WGI) from World Bank
                """)
            with tab_rel:
                st.markdown("""
Corruption and bribery facilitate IFFs, erode trust in institutions, and hinder sustainable development. The normalized scores and country shares provide a standardized way to compare corruption levels across countries and track changes over time.
                """)
            with tab_proxy:
                st.markdown("""
**Proxy Justification:**
- WGI's Control of Corruption index aggregates data from 30+ sources
- Includes surveys, expert assessments, and NGO reports
- Uses Unobserved Components Model (UCM) for robust aggregation
- Provides comprehensive view of governance quality
                """)

# === Tab 3: Detection and Enforcement ===
with tab3:
    st.header("4.4.3: Detection and Enforcement")
    st.markdown("""
This section covers the effectiveness of anti-IFF measures, capacity of tax and customs authorities, and related enforcement indicators. Data sources include the World Justice Project, Mo Ibrahim Foundation, World Bank, IMF ISORA, and others.
    """)

    # 4.4.3.1: Effectiveness of Anti-IFF Measures
    st.subheader("4.4.3.1: Effectiveness of Anti-IFF Measures")
    # Define chart functions and subindicators dict first
    def show_rule_of_law_chart():
        indicator_label = "Rule of Law"  # Use the exact label in your data
        data = filtered_data[filtered_data['indicator_label'] == indicator_label]
        if not data.empty:
            visualize_indicator(
                df=data,
                indicator_label=indicator_label,
                chart_type="bar",
                title="Rule of Law (WJP Factor 6: Regulatory Enforcement)",
                y_title="Score",
                x_title="Year",
                color_by="country_or_area"
            )
            with st.expander("View Data Table"):
                st.dataframe(data)
        else:
            st.info("No data available for this indicator.")

    def show_control_of_corruption_chart():
        indicator_label = "Control of Corruption: Estimate"
        data = filtered_data[filtered_data['indicator_label'] == indicator_label]
        if not data.empty:
            visualize_indicator(
                df=data,
                indicator_label=indicator_label,
                chart_type="bar",
                title="Control of Corruption: Estimate",
                y_title="Score",
                x_title="Year",
                color_by="country_or_area"
            )
            with st.expander("View Data Table"):
                st.dataframe(data)
        else:
            st.info("No data available for this indicator.")

    subindicators = {
        "4.4.3.1b: Rule of Law (WJP Factor 6: Regulatory Enforcement)": {
            "content": show_rule_of_law_chart,
        },
        "4.4.3.1c: Rule of Law & Justice (Mo Ibrahim Index)": {
            "content": lambda: st.info("Skipped: Not in nexus.parquet."),
        },
        "4.4.3.1d: Reducing Corruption (Control of Corruption: Estimate)": {
            "content": show_control_of_corruption_chart,
        },
        "4.4.3.1e: Sound Institutions (CPIA quality of public administration rating)": {
            "content": lambda: st.info("Skipped: Not in nexus.parquet."),
        },
        "4.4.3.1f: Identity Documentation": {
            "content": lambda: st.info("Skipped: Not in nexus.parquet."),
        }
        # Exclude 4.4.3.1g and 4.4.3.1h
    }
    # Now render dropdown and chart
    selected_sub = st.selectbox("Select sub-indicator:", list(subindicators.keys()), key="anti_iff_subindicator")
    subindicators[selected_sub]["content"]()
    # Now show the Learn more expander after the chart/dropdown
    with st.expander("Learn more about Indicator 4.4.3.1: Effectiveness of Anti-IFF Measures"):
        st.markdown("""
4.4.3.1. Effectiveness of Anti-IFF Measures 

This indicator assesses the efficacy of efforts to combat illicit financial flows (IFFs) by measuring successful prosecutions for IFF-related offenses. Given the challenges in obtaining direct prosecution data across jurisdictions, this study proxies effectiveness using the enablers framework outlined in Coherent Policies for Combatting Illicit Financial Flows (UNODC-OECD, 2016). 

Data Sources and Proxy Indicators 

The effectiveness of anti-IFF measures is assessed using multiple governance, regulatory, and institutional indicators that influence the ability to combat IFFs effectively. These proxies include: 

Regulation of Financial Markets: Captures the existence and enforcement of financial market regulations relevant to anti-IFF policies. 

Rule of Law (Regulatory Enforcement, Factor 6): Provided by the World Justice Project (WJP), measuring the extent to which regulations are fairly and effectively enforced. 

Rule of Law & Justice (Score and Rank): Measured by the Mo Ibrahim Index, reflecting the strength of legal institutions in preventing financial crimes. 

Reducing Corruption: Assessed using the World Bank's CPIA Transparency, Accountability, and Corruption rating, which scores the public sector's ability to prevent corruption. 

Sound Institutions: Evaluated using the CPIA Quality of Public Administration rating, indicating how well public institutions function in reducing financial crime risks. 

Identity Documentation: Sourced from the World Bank ID4D dataset, measuring the extent of legal identification coverage, crucial for tracking financial transactions and reducing anonymous illicit flows. 

Public Access to Information (Open Government, Right to Information): Analyzed using WJP's Open Government Indicator (Factor 3.2), which assesses transparency and citizens' access to government data. 

Calculation Approach 

Effectiveness is measured by compiling and analyzing the selected proxy indicators: 

Standardizing Scores: Normalize values across different indices to ensure comparability. 

Weighted Aggregation: Compute a composite measure reflecting overall effectiveness, with higher weights assigned to regulatory enforcement and corruption control. 

Trend Analysis: Assess progress over time to track improvements or declines in effectiveness. 

Rationale for Using These Proxies 

The UNODC-OECD framework identifies governance and institutional quality as key determinants of anti-IFF effectiveness. 

The World Justice Project, World Bank, and Mo Ibrahim Index provide validated, cross-country governance data relevant to financial crime control. 

Transparency and identity documentation are essential enablers for tracking and prosecuting illicit financial flows.  
        """)

# === Tab 4: Impact on Development Finance ===
with tab4:
    st.header("4.4.5: Impact on Development Finance")
    with st.expander("Learn more about Indicator 4.4.5: Impact on Development Finance"):
        st.markdown("""
4.4.5. Impact on Development Finance

This section assesses the impact of illicit financial flows (IFFs) on development finance, focusing on reductions in financial leakages and improvements in government revenue collection. The analysis uses proxy indicators to measure the responsiveness of tax systems and the social impact of lost tax revenue.

**Data Sources and Proxy Indicators**

- **Tax Buoyancy:** Ratio of change in tax revenue in relation to change in gross domestic product (GDP) of an economy. Measures how responsive a taxation policy is to growth in economic activities.
- **Social Impact of Lost Tax:** Tax loss equivalent to the percentage of health and education budget (e.g., sotj20_loss_total_share_healthexpenses, all years).

**Calculation Approach**

- **Tax Buoyancy:** Calculated as the ratio of the percentage change in tax revenue to the percentage change in GDP over a given period.
- **Social Impact:** Assessed by comparing tax losses to government spending on health and education.

**Rationale for Using These Proxies**

- Tax buoyancy reflects the effectiveness of tax policy in mobilizing domestic resources for development.
- The social impact indicator highlights the opportunity cost of lost tax revenue for essential public services.
        """)

    subindicators_445 = {
        "4.4.5.1: Tax Buoyancy (Reduction in Financial Leakages)": {
            "content": lambda: st.info("Placeholder for Tax Buoyancy data visualization and table."),
        },
        "4.4.5.2: Social Impact of Lost Tax (Improvement in Revenue Collection)": {
            "content": lambda: st.info("Placeholder for Social Impact of Lost Tax data visualization and table."),
        }
    }

    selected_sub_445 = st.selectbox("Select sub-indicator:", list(subindicators_445.keys()), key="impact_dev_finance_subindicator")
    subindicators_445[selected_sub_445]["content"]()

# === Tab 5: Policy and Regulatory Environment ===
with tab5:
    st.header("4.4.6: Policy and Regulatory Environment")
    with st.expander("Learn more about Indicator 4.4.6: Policy and Regulatory Environment"):
        st.markdown("""
4.4.6. Policy and Regulatory Environment

This section assesses the implementation and effectiveness of policies aimed at reducing illicit financial flows (IFFs), with a focus on sector-specific regulations and rent sharing arrangements in the mining sector.

**Data Sources and Proxy Indicators**

- **Implementation of Anti-IFF Policies:** Number and effectiveness of policies aimed at reducing IFFs.
- **Specific Sectors:** Lists the laws and regulations that govern the taxation and mining activity of each country, including counts of general regime and mining regime.
- **Rent Sharing:** Examines rent sharing arrangements between the state and investors in the mining sector.

**Calculation Approach**

- **Policy Count:** Count the number of relevant laws and regulations for each country and sector.
- **Effectiveness Assessment:** Qualitatively or quantitatively assess the effectiveness of these policies where data is available.

**Rationale for Using These Proxies**

- The presence and quality of sector-specific regulations and rent sharing arrangements are key determinants of a country's ability to reduce IFFs, especially in resource-rich sectors like mining.
        """)

    subindicators_446 = {
        "4.4.6.1.a: Specific Sectors (Taxation and Mining Laws/Regimes)": {
            "content": lambda: st.info("Placeholder for laws and regulations governing taxation and mining activity data visualization and table."),
        },
        "4.4.6.1.a: Rent Sharing Between State and Investors": {
            "content": lambda: st.info("Placeholder for rent sharing arrangements data visualization and table."),
        }
    }

    selected_sub_446 = st.selectbox("Select sub-indicator:", list(subindicators_446.keys()), key="policy_reg_env_subindicator")
    subindicators_446[selected_sub_446]["content"]()
