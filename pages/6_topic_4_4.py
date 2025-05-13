import streamlit as st
import pandas as pd
from universal_viz import visualize_indicator, load_main_data, load_country_reference_data, setup_sidebar_filters, filter_dataframe_by_selections
import plotly.graph_objs as go
import altair as alt
from composite_indicator_methods import calculate_corruption_losses
from special_pages.tab_4_4_4 import render_financial_secrecy_tab
import plotly.express as px
import data_gap_visualization as dgv
import universal_viz as uv

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

# === Tabs for 4.4 subtopics ===
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "4.4.1: Magnitude of IFFs",
    "4.4.2: Types of IFFs",
    "4.4.3: Detection and Enforcement",
    "4.4.4: Financial Secrecy",
    "4.4.5: Impact on Development Finance",
    "4.4.6: Policy and Regulatory Environment"
])

africa_countries = country_ref[country_ref['Region Name'] == 'Africa']['Country or Area'].unique()
df_africa = df[df['country_or_area'].isin(africa_countries)]

with tab1:
    from special_pages.tab_4_4_1 import render_tab_4_4_1
    render_tab_4_4_1(filtered_data, filters)
    # (No Geographical Distribution section in this tab)

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
        if 'indicator_code' in filtered_data.columns:
            crime_data = filtered_data[filtered_data['indicator_code'].astype(str).str.strip() == 'UNODC.DPS.losses']
        else:
            crime_data = filtered_data[filtered_data['indicator_label'].astype(str).str.strip() == 'UNODC.DPS.losses']
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

    # Geographical Distribution for tab2
    st.markdown("#### Geographical Distribution")
    trade_mispricing_labels = [
        "The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries and 36 Advanced Economies, 2009–2018, in USD Millions",
        "The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries and all of their Global Trading Partners, 2009–2018 in USD Millions",
        "The Total Value Gaps Identified Between 134 Developing Countries and 36 Advanced Economies, 2009–2018, as a Percent of Total Trade",
        "The Total Value Gaps Identified in Trade Between 134 Developing Countries and all of their Trading Partners, 2009–2018 as a Percent of Total Trade"
    ]
    selected_map_indicator_442 = st.selectbox(
        "Select indicator for map view:",
        options=trade_mispricing_labels,
        key="topic4_4_2_map_indicator_select"
    )
    uv.render_indicator_map(
        df=filtered_data,
        indicator_label=selected_map_indicator_442,
        title="",
        description=f"Geographical distribution of latest {selected_map_indicator_442} values.",
        reference_data=country_ref,
        year_range=filters.get('year_range'),
        map_options={'color_continuous_scale': 'Blues'},
        container_key="topic4_4_2_map"
    )

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

    # 4.4.3.2: Capacity of Tax and Customs Authorities
    st.subheader("4.4.3.2: Capacity of Tax and Customs Authorities")

    # 4.4.3.2.a Operating Metrics Audit
    st.markdown("#### 4.4.3.2.a: Operating Metrics Audit")
    operational_indicators = {
        "Number of criminal investigations": "Role of the administration in tax crime investigations - Conducting investigations, under direction of other agency",
        "Number of tax dispute resolutions": "FTEs by function of the tax administration-Audit, investigation and other verification",
        "Number of audits / tax crime investigations": "FTEs by function of the tax administration-Audit, investigation and other verification"
    }
    selected_ops = st.selectbox(
        "Select Operational Capacity Indicator:",
        options=list(operational_indicators.keys()),
        key="ops_capacity_selectbox"
    )
    display_name = selected_ops
    label = operational_indicators[display_name]
    data = filtered_data[filtered_data['indicator_label'] == label]
    if not data.empty:
        visualize_indicator(
            df=data,
            indicator_label=label,
            chart_type="bar",
            title=display_name,
            y_title="Value",
            x_title="Year",
            color_by="country_or_area"
        )
        with st.expander(f"View Data Table: {display_name}"):
            st.dataframe(data)
    else:
        st.info(f"No data available for {display_name}.")

    # 4.4.3.2.b Financial & ICT Resources
    st.markdown("#### 4.4.3.2.b: Resources and ICT Infrastructure")
    financial_indicators = {
        "Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Corporate income tax": "Value of additional assessments raised from audits and verification actions by tax type (including penalties and interest) (in thousands in local currency)-Corporate income tax",
        "Salary expenditure - Derived": "Salary expenditure - Derived",
        "Operating expenditure - Derived": "Operating expenditure - Derived",
        "Operational ICT solutions of the administration are…-Custom built": "Operational ICT solutions of the administration are…-Custom built",
        "Operational ICT solutions of the administration are…-On premises commercial off the shelf (COTS)": "Operational ICT solutions of the administration are…-On premises commercial off the shelf (COTS)",
        "Operational ICT solutions of the administration are…-Software-as-a-Service (SaaS, i.e. cloud based)": "Operational ICT solutions of the administration are…-Software-as-a-Service (SaaS, i.e. cloud based)",
        "Total tax administration FTEs - Derived": "Total tax administration FTEs - Derived"
    }
    selected_fin = st.selectbox(
        "Select Financial & ICT Resource Indicator:",
        options=list(financial_indicators.keys()),
        key="fin_capacity_selectbox"
    )
    display_name = selected_fin
    label = financial_indicators[display_name]
    data = filtered_data[filtered_data['indicator_label'] == label]
    if not data.empty:
        visualize_indicator(
            df=data,
            indicator_label=label,
            chart_type="bar",
            title=display_name,
            y_title="Value",
            x_title="Year",
            color_by="country_or_area"
        )
        with st.expander(f"View Data Table: {display_name}"):
            st.dataframe(data)
    else:
        st.info(f"No data available for {display_name}.")

    # 4.4.3.2.c Human Capital Strength
    st.markdown("#### 4.4.3.2.c: Human Capital Strength")
    human_capital_indicators = {
        "Staff Strength - Departures in FY": "Staff strength levels -Departures in FY",
        "Staff Strength - No. at end of FY": "Staff strength levels -No. at end of FY",
        "Staff Strength - No. at start of FY": "Staff strength levels -No. at start of FY",
        "Staff Strength - Recruitments in FY": "Staff strength levels -Recruitments in FY",
        "Academic Qualifications - Bachelors degree": "Academic qualifications (No. of staff at the end of FY)-Bachelors degree",
        "Academic Qualifications - Masters degree (or above)": "Academic qualifications (No. of staff at the end of FY)-Masters degree (or above)",
        "Length of Service - 10-19 years": "Length of service (No. of staff at the end of FY)-10-19 years",
        "Length of Service - 5-9 years": "Length of service (No. of staff at the end of FY)-5-9 years",
        "Length of Service - Over 19 years": "Length of service (No. of staff at the end of FY)-Over 19 years",
        "Length of Service - Under 5 years": "Length of service (No. of staff at the end of FY)-Under 5 years"
    }
    selected_hc = st.selectbox(
        "Select Human Capital Strength Indicator:",
        options=list(human_capital_indicators.keys()),
        key="hc_capacity_selectbox"
    )
    display_name = selected_hc
    label = human_capital_indicators[display_name]
    data = filtered_data[filtered_data['indicator_label'] == label]
    if not data.empty:
        visualize_indicator(
            df=data,
            indicator_label=label,
            chart_type="bar",
            title=display_name,
            y_title="Number of Staff",
            x_title="Year",
            color_by="country_or_area"
        )
        with st.expander(f"View Data Table: {display_name}"):
            st.dataframe(data)
    else:
        st.info(f"No data available for {display_name}.")

    # Learn more expander after all groups
    with st.expander("Learn more about Indicator 4.4.3.2: Capacity of Tax and Customs Authorities"):
        st.markdown("""
4.4.3.2. Capacity of Tax and Customs Authorities

This indicator assesses the capacity and effectiveness of tax and customs authorities in detecting and preventing illicit financial flows (IFFs). Due to the limited availability of direct performance metrics, the analysis uses proxy indicators based on the IMF ISORA survey and related sources.

**Data Sources and Proxy Indicators**

- **Operating Metrics Audit:** Includes criminal investigations, dispute resolution, and tax crime investigation (IMF ISORA).
- **Resources and ICT Infrastructure:** Covers tax administration expenditures, FTEs, and operational ICT solutions (IMF ISORA).
- **Staff Metrics:** Measures staff strength, academic qualifications, and length of service (IMF ISORA).

**Calculation Approach**

- **Standardizing Scores:** Normalize values across different metrics to ensure comparability.
- **Composite Index:** Aggregate the standardized metrics to create a composite measure of capacity and effectiveness.
- **Trend Analysis:** Track changes over time to assess improvements or declines in capacity.

**Rationale for Using These Proxies**

- The IMF ISORA survey provides comprehensive, cross-country data on tax and customs administration operations.
- Resource allocation, staff capacity, and operational effectiveness are key determinants of the ability to detect and prevent IFFs.
        """)

    # Geographical Distribution for tab3
    st.markdown("#### Geographical Distribution")
    tab3_labels = [
        "Rule of Law",
        "Control of Corruption: Estimate",
        "Role of the administration in tax crime investigations - Conducting investigations, under direction of other agency",
        "FTEs by function of the tax administration-Audit, investigation and other verification",
        "FTEs by function of the tax administration-Enforced debt collection and related functions",
        "FTEs by function of the tax administration-Other functions",
        "FTEs by function of the tax administration-Registration, taxpayer services, returns and payment processing",
        "Total tax administration FTEs - Derived"
    ]
    selected_map_indicator_443 = st.selectbox(
        "Select indicator for map view:",
        options=tab3_labels,
        key="topic4_4_3_map_indicator_select"
    )
    uv.render_indicator_map(
        df=filtered_data,
        indicator_label=selected_map_indicator_443,
        title="",
        description=f"Geographical distribution of latest {selected_map_indicator_443} values.",
        reference_data=country_ref,
        year_range=filters.get('year_range'),
        map_options={'color_continuous_scale': 'Blues'},
        container_key="topic4_4_3_map"
    )

# === Tab 4: Financial Secrecy ===
with tab4:
    render_financial_secrecy_tab(filtered_data, filters)
    # Geographical Distribution for tab4
    st.markdown("#### Geographical Distribution")
    fsi_labels = [label for label in filtered_data['indicator_label'].unique() if label.startswith('fsi_') and label.endswith('_value')]
    selected_map_indicator_444 = st.selectbox(
        "Select indicator for map view:",
        options=fsi_labels,
        key="topic4_4_4_map_indicator_select"
    )
    uv.render_indicator_map(
        df=filtered_data,
        indicator_label=selected_map_indicator_444,
        title="",
        description=f"Geographical distribution of latest {selected_map_indicator_444} values.",
        reference_data=country_ref,
        year_range=filters.get('year_range'),
        map_options={'color_continuous_scale': 'Blues'},
        container_key="topic4_4_4_map"
    )

# === Tab 5: Impact on Development Finance ===
with tab5:
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

    st.subheader("4.4.5.1: Tax Buoyancy (Reduction in Financial Leakages)")
    # List of available tax buoyancy indicators (from your screenshot)
    tax_buoyancy_indicators = [
        "Excise Taxes - % of GDP - Buoyancy",
        "Income Taxes - % of GDP - Buoyancy",
        "Personal income tax (PIT) buoyancy [by_pit]",
        "Property Taxes - % of GDP - Buoyancy",
        "Tax Revenue - % of GDP - Buoyancy",
        "Tax buoyancy [by_tax]",
        "Taxes on Goods and Services - % of GDP - Buoyancy",
        "Trade Taxes - % of GDP - Buoyancy",
        "Value-added tax (VAT) buoyancy [by_vat]"
    ]
    # Only show indicators that exist in the data
    available_buoyancy = [label for label in tax_buoyancy_indicators if label in filtered_data['indicator_label'].unique()]
    selected_buoyancy = st.selectbox(
        "Select Tax Buoyancy Indicator:",
        options=available_buoyancy,
        key="tax_buoyancy_selector"
    )
    buoyancy_data = filtered_data[filtered_data['indicator_label'] == selected_buoyancy]
    if not buoyancy_data.empty:
        visualize_indicator(
            df=buoyancy_data,
            indicator_label=selected_buoyancy,
            chart_type="line",
            title=selected_buoyancy,
            y_title="Buoyancy Ratio",
            x_title="Year",
            color_by="country_or_area"
        )
        with st.expander(f"View Data Table: {selected_buoyancy}"):
            st.dataframe(buoyancy_data[['country_or_area', 'year', 'value']].sort_values(['country_or_area', 'year']))
    else:
        st.info(f"No data available for {selected_buoyancy}")
    with st.expander("Learn more about Indicator 4.4.5.1: Tax Buoyancy"):
        st.markdown("""
**Definition:** Tax buoyancy is the ratio of the percentage change in tax revenue to the percentage change in GDP. It measures how responsive a taxation policy is to growth in economic activities. A buoyancy greater than 1 indicates that tax revenue is growing faster than GDP, reflecting effective tax policy and administration.

**Proxy Justification:** Used here as a proxy for reduction in financial leakages due to effective anti-IFF measures.
        """)

    def render_social_impact_of_lost_tax():
        st.markdown("### Indicator 4.4.5.2: Social Impact of Lost Tax")
        st.caption("Tax loss equivalent to the percentage of health and education budget")
        data = filtered_data[filtered_data['indicator_label'] == 'sotj20_loss_total_share_healthexpenses']
        if not data.empty:
            fig = px.line(
                data,
                x='year',
                y='value',
                color='country_or_area',
                title="Tax Loss as % of Health and Education Budget",
                labels={
                    'value': 'Tax Loss (% of Health & Education Budget)',
                    'year': 'Year',
                    'country_or_area': 'Country'
                }
            )
            fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Tax Loss (% of Health & Education Budget)",
                legend_title="Country"
            )
            st.plotly_chart(fig, use_container_width=True)
            with st.expander("View Data Table"):
                st.dataframe(
                    data[['country_or_area', 'year', 'value']]
                    .sort_values(['country_or_area', 'year'])
                    .style.format({'value': '{:.2f}%'})
                )
        else:
            st.info("No data available for Tax Loss as % of Health and Education Budget")
        with st.expander("🔍 Learn more about Indicator 4.4.5.2"):
            tab_def, tab_rel, tab_proxy = st.tabs(["📘 Definition", "📌 Relevance", "📊 Proxy Justification"])
            with tab_def:
                st.markdown("""
This indicator measures the social impact of lost tax revenue by comparing it to government spending on health and education. It shows what percentage of these essential public services could have been funded with the lost tax revenue.
                """)
            with tab_rel:
                st.markdown("""
- **Efficiency**: Shows the opportunity cost of tax losses in terms of essential public services
- **Effectiveness**: Highlights the social impact of improving tax collection
                """)
            with tab_proxy:
                st.markdown("""
The indicator uses data from the State of Tax Justice report, which provides standardized estimates of tax losses and their impact on public services across countries.
                """)

    subindicators_445 = {
        "4.4.5.2: Social Impact of Lost Tax (Improvement in Revenue Collection)": {
            "content": render_social_impact_of_lost_tax
        }
    }
    selected_sub_445 = st.selectbox("Select sub-indicator:", list(subindicators_445.keys()), key="impact_dev_finance_subindicator")
    subindicators_445[selected_sub_445]["content"]()

    # Geographical Distribution for tab5
    st.markdown("#### Geographical Distribution")
    tab5_labels = [
        "Tax Revenue - % of GDP - Buoyancy",
        "sotj20_loss_total_share_healthexpenses"
    ]
    selected_map_indicator_445 = st.selectbox(
        "Select indicator for map view:",
        options=tab5_labels,
        key="topic4_4_5_map_indicator_select"
    )
    uv.render_indicator_map(
        df=filtered_data,
        indicator_label=selected_map_indicator_445,
        title="",
        description=f"Geographical distribution of latest {selected_map_indicator_445} values.",
        reference_data=country_ref,
        year_range=filters.get('year_range'),
        map_options={'color_continuous_scale': 'Blues'},
        container_key="topic4_4_5_map"
    )

# === Tab 6: Policy and Regulatory Environment ===
with tab6:
    st.header("4.4.6: Policy and Regulatory Environment")
    with st.expander("Learn more about Indicator 4.4.6: Policy and Regulatory Environment"):
            st.markdown("""
4.4.6. Policy and Regulatory Environment

This section assesses the implementation and effectiveness of policies aimed at reducing illicit financial flows (IFFs), with a focus on sector-specific regulations and rent sharing arrangements in the mining sector.
        """)

    subindicators_446 = {
        "4.4.6.1: Implementation of Anti-IFF Policies": {
            "content": lambda: st.info("Placeholder for number and effectiveness of anti-IFF policies data visualization and table."),
            "learn_more": lambda: st.markdown("""
**Definition:** Number and effectiveness of policies aimed at reducing illicit financial flows (IFFs).

**Methodology:** Count and assess the effectiveness of national policies, laws, and regulations specifically targeting IFFs.

**Rationale:** Effective policy implementation is a key determinant of a country's ability to reduce IFFs.
            """)
        },
        "4.4.6.1.a: Specific Sectors (Taxation and Mining Laws/Regimes)": {
            "content": lambda: st.info("Placeholder for laws and regulations governing taxation and mining activity data visualization and table."),
            "learn_more": lambda: st.markdown("""
**Definition:** Lists the laws and regulations that govern the taxation and mining activity of each country. This includes counting the number of general regime and mining regime for each country.

**Methodology:** For each country, count the number of general regime and mining regime laws and regulations.

**Rationale:** Provides a comparative overview of the regulatory environment for mining and taxation across African countries.
            """)
        },
        "4.4.6.1.a: Rent Sharing Between State and Investors": {
            "content": lambda: st.info("Placeholder for rent sharing arrangements data visualization and table."),
            "learn_more": lambda: st.markdown("""
**Definition:** Examines rent sharing arrangements between the state and investors in the mining sector. Uses the Legal and Tax Database on Gold Mining in Africa to count the number of general regime and mining regime.

**Data Source:** [ICTD Legal and Tax Database on Gold Mining in Africa](https://www.ictd.ac/dataset/legal-tax-database-gold-mining-africa/)

**Methodology:** For each country, count the number of general regime and mining regime related to rent sharing.

**Rationale:** Provides insight into how mining rents are distributed between the state and private investors.
            """)
        }
    }

    selected_sub_446 = st.selectbox("Select sub-indicator:", list(subindicators_446.keys()), key="policy_reg_env_subindicator")
    subindicators_446[selected_sub_446]["content"]()
    with st.expander(f"Learn more about {selected_sub_446}"):
        subindicators_446[selected_sub_446]["learn_more"]()

    # Geographical Distribution for tab6
    st.markdown("#### Geographical Distribution")
    tab6_labels = [
        "Rule of Law Index",
        "Tax Revenue Losses"
    ]
    selected_map_indicator_446 = st.selectbox(
        "Select indicator for map view:",
        options=tab6_labels,
        key="topic4_4_6_map_indicator_select"
    )
    uv.render_indicator_map(
        df=filtered_data,
        indicator_label=selected_map_indicator_446,
        title="",
        description=f"Geographical distribution of latest {selected_map_indicator_446} values.",
        reference_data=country_ref,
        year_range=filters.get('year_range'),
        map_options={'color_continuous_scale': 'Blues'},
        container_key="topic4_4_6_map"
    )

# Collect all indicators used in the Geographical Distribution sections of tabs 4.4.2–4.4.6
trade_mispricing_labels = [
    "The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries and 36 Advanced Economies, 2009–2018, in USD Millions",
    "The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries and all of their Global Trading Partners, 2009–2018 in USD Millions",
    "The Total Value Gaps Identified Between 134 Developing Countries and 36 Advanced Economies, 2009–2018, as a Percent of Total Trade",
    "The Total Value Gaps Identified in Trade Between 134 Developing Countries and all of their Trading Partners, 2009–2018 as a Percent of Total Trade"
]
tab3_labels = [
    "Rule of Law",
    "Control of Corruption: Estimate",
    "Role of the administration in tax crime investigations - Conducting investigations, under direction of other agency",
    "FTEs by function of the tax administration-Audit, investigation and other verification",
    "FTEs by function of the tax administration-Enforced debt collection and related functions",
    "FTEs by function of the tax administration-Other functions",
    "FTEs by function of the tax administration-Registration, taxpayer services, returns and payment processing",
    "Total tax administration FTEs - Derived"
]
fsi_labels = [label for label in filtered_data['indicator_label'].unique() if label.startswith('fsi_') and label.endswith('_value')]
tab5_labels = [
    "Tax Revenue - % of GDP - Buoyancy",
    "sotj20_loss_total_share_healthexpenses"
]
tab6_labels = [
    "Rule of Law Index",
    "Tax Revenue Losses"
]
# Combine and deduplicate
all_gap_indicators = list(dict.fromkeys(
    trade_mispricing_labels + tab3_labels + fsi_labels + tab5_labels + tab6_labels
))

st.divider()
with st.expander("Understand the data gap in Africa for this topic"):
    selected_gap_indicator = st.selectbox(
        "Select indicator to view data availability:",
        options=all_gap_indicators,
        key="topic4_4_gap_indicator_select"
    )
    uv.render_data_availability_heatmap(
        df=df_africa,
        indicator_label=selected_gap_indicator,
        title=f"Data Availability for {selected_gap_indicator} (Africa)",
        container_key="topic4_4_gap"
    )
