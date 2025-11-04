import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path for module imports
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from universal_viz import visualize_indicator, load_main_data, load_country_reference_data, setup_sidebar_filters, filter_dataframe_by_selections
import plotly.graph_objs as go
import altair as alt
from composite_indicator_methods import calculate_corruption_losses
import plotly.express as px
import data_gap_visualization as dgv
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

# Load data
df = load_main_data("data/nexus.parquet")
country_ref = load_country_reference_data()

# Setup filters
filters = setup_sidebar_filters(country_ref, df, key_prefix="topic4_4")

# Filter data based on selections
filtered_data = filter_dataframe_by_selections(df, filters, country_ref)

# ========================================
# SECTION: Topic Header
# ========================================
with st.container():
    st.markdown("""
    <div class="section-header">
        <h1>Topic 4.4: Illicit Financial Flows (IFFs)</h1>
        <p>This section analyzes illicit financial flows (IFFs) in Africa, including their magnitude, types, and enforcement measures. IFFs undermine domestic resource mobilization, erode trust in institutions, and hinder sustainable development. Understanding and combating IFFs is crucial for achieving fiscal stability and development goals.</p>
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
        available_years = sorted(filtered_data['year'].dropna().unique()) if not filtered_data.empty else []
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
        available_countries = sorted(filtered_data['country_or_area'].dropna().unique()) if not filtered_data.empty else []
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
            options=["GFI", "World Bank", "UNODC", "IMF"],
            default=["GFI", "World Bank"],
            key="global_source_filter"
        )

st.divider()

# Apply global filters
df_display = filtered_data.copy()
if selected_year != "All Years":
    df_display = df_display[df_display['year'] == selected_year]
if selected_country != "All Countries":
    df_display = df_display[df_display['country_or_area'] == selected_country]

display_filters = filters.copy()
if selected_year != "All Years":
    display_filters['year_range'] = (selected_year, selected_year)
if selected_country != "All Countries":
    display_filters['selected_countries'] = [selected_country]

# ========================================
# SECTION: Main Content with Tabs
# ========================================
st.markdown("### Key Indicators by Subtopic")

africa_countries = country_ref[country_ref['Region Name'] == 'Africa']['Country or Area'].unique()
df_africa = df[df['country_or_area'].isin(africa_countries)]

# Create tabs for all 6 subtopics
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "4.4.1: Magnitude of IFFs",
    "4.4.2: Types of IFFs",
    "4.4.3: Detection & Enforcement",
    "4.4.4: Financial Secrecy",
    "4.4.5: Impact on Dev. Finance",
    "4.4.6: Policy Environment"
])

# =============================================
# TAB 1: 4.4.1 Magnitude of IFFs (2 indicators)
# =============================================
with tab1:
    st.markdown("This section presents headline estimates of the scale of illicit financial flows (IFFs) in Africa, both as a share of GDP and in absolute terms.")
    
    # 2-column layout for 2 indicators
    col1, col2 = st.columns(2, gap="large")
    
    # Indicator 4.4.1.1 - Left Column
    with col1:
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.4.1.1: IFFs as % of GDP</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 0.8rem;">
                Africa loses an estimated <strong>3.7% of its GDP annually</strong> to illicit financial flows (IFFs). 
                West Africa experiences the highest relative burden at 10.3% of GDP, while North Africa has the lowest at 2.7%.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("View Details", expanded=False):
            st.markdown("""
**Definition:**  
Illicit financial flows (IFFs) are cross-border movements of money that are illegal in origin, transfer, or use. This includes tax evasion, trade mispricing, corruption, and proceeds from criminal activity.

**Africa-wide Estimates:**  
- Africa loses an estimated **3.7% of its GDP annually** to IFFs, based on mid-2010s data.  
- Over 2000–2015, the average was around **2.6% of GDP**, suggesting the scale has grown.  
- This ratio is among the highest globally.

**Regional Variations:**  
- **West Africa:** Median IFFs reach **10.3% of GDP**, the highest in the continent.  
- **North Africa:** Experiences the lowest relative levels, at around **2.7% of GDP**.

**Policy Relevance:**  
IFFs of this magnitude reduce fiscal space, increase debt dependence, and compromise SDG financing.

**Source:** UNCTAD (2020). Economic Development in Africa Report: Tackling Illicit Financial Flows for Sustainable Development in Africa.
            """)
    
    # Indicator 4.4.1.2 - Right Column
    with col2:
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.4.1.2: Annual IFF Volume</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 0.8rem;">
                Africa loses approximately <strong>USD 88.6 billion each year</strong> through IFFs. 
                This far exceeds annual aid inflows (~USD 48 billion) and FDI (~USD 54 billion) received by the continent.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("View Details", expanded=False):
            st.markdown("""
**Annual Estimate:**  
UNCTAD estimates that Africa loses approximately **USD 88.6 billion each year** through illicit financial flows.

**Country-Level Figures (2013–2015):**  
- **Nigeria:** USD 41 billion  
- **Egypt:** USD 17.5 billion  
- **South Africa:** USD 14.1 billion

**Cumulative Losses:**  
From 2000–2015, cumulative IFFs from Africa amounted to about **USD 836 billion**.

**Main Channels of IFFs:**  
- **Commercial Tax Practices** (e.g. trade mispricing, profit shifting): ~65% of total IFFs  
- **Corruption-related flows:** Bribery, embezzlement, and public sector theft  
- **Illicit Markets and Smuggling:** Drugs, arms, wildlife, etc.  
- **Terrorist Financing and Criminal Proceeds**

**Sector Spotlight – Extractives:**  
In 2015, under-invoicing of African extractive exports accounted for **USD 40 billion in losses** — with gold alone representing 77% of the total mispriced value.

**Source:** UNCTAD (2020). Economic Development in Africa Report.
            """)

# =============================================
# TAB 2: 4.4.2 Types of IFFs (4 indicators → 3 columns)
# =============================================
with tab2:
    st.markdown("This section analyzes different types of illicit financial flows, including trade mispricing, tax evasion, criminal activities, and corruption.")
    
    # First row: 3 indicators
    col1, col2, col3 = st.columns(3, gap="medium")
    
    # Indicator 4.4.2.1 - Trade Mispricing
    with col1:
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.4.2.1: Trade Mispricing</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 0.8rem;">
                Manipulating trade values to illegally shift capital. Proxied by GFI's bilateral trade mismatch analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("View Chart and Data", expanded=False):
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
            
            st.markdown("---")
            st.markdown("**Learn More:**")
            st.markdown("Trade mispricing is a major channel for IFFs, undermining domestic resource mobilization. GFI's trade gap data is widely used for estimating IFFs due to trade mispricing.")
    
    # Indicator 4.4.2.2 - Tax Evasion
    with col2:
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.4.2.2: Tax Evasion</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 0.8rem;">
                Measures the share of active and inactive taxpayers on various registers as a percentage of the labor force or population. Proxied by IMF Tax Registration Data.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("View Chart and Data", expanded=False):
            tax_evasion_label_map = {
                "Active taxpayers on PIT register as percentage of Labor Force": "Active taxpayers on PIT register as % of Labor Force",
                "Active taxpayers on PIT register as percentage of Population": "Active taxpayers on PIT register as % of Population"
            }
            
            available_labels = [
                label for label in tax_evasion_label_map.keys()
                if label in filtered_data['indicator_label'].unique()
            ]
            
            dropdown_options = [tax_evasion_label_map[label] for label in available_labels]
            
            selected_display_labels = st.multiselect(
                "Select Tax Evasion Indicators:",
                options=dropdown_options,
                default=dropdown_options if dropdown_options else [],
                key="tax_evasion_multiselect"
            )
            
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
            
            st.markdown("---")
            st.markdown("**Learn More:**")
            st.markdown("Tax evasion reduces government revenue, limits public investment, and distorts economic incentives. IMF tax registration data provides standardized estimates.")
    
    # Indicator 4.4.2.3 - Criminal Activities
    with col3:
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.4.2.3: Criminal Activities</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 0.8rem;">
                Monetary losses (in USD) to drug sales. Calculated as drug seizures in kilograms multiplied by drug price per kilogram. Proxied by UNODC Crime Flow Data.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("View Chart and Data", expanded=False):
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
            
            st.markdown("---")
            st.markdown("**Learn More:**")
            st.markdown("Criminal activities, such as drug trafficking, are a significant source of IFFs, undermining rule of law and economic development.")
    
    # Second row: 1 indicator
    st.markdown("---")
    col1, col2, col3 = st.columns(3, gap="medium")
    
    # Indicator 4.4.2.4 - Corruption and Bribery
    with col1:
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.4.2.4: Corruption and Bribery</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 0.8rem;">
                Measures corruption levels using World Bank Governance Indicators. Estimated annual corruption losses are allocated from $148B based on inverted control of corruption scores.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("View Chart and Data", expanded=False):
            try:
                corruption_data = filtered_data[filtered_data['indicator_label'] == 'Control of Corruption']
                if not corruption_data.empty:
                    latest_corruption = calculate_corruption_losses(corruption_data)
                    bar_chart = alt.Chart(latest_corruption).mark_bar().encode(
                        x=alt.X('country_or_area', sort='-y', title='Country'),
                        y=alt.Y('corruption_loss_billion_usd', title='Estimated Corruption Loss (Billion USD)'),
                        tooltip=['country_or_area', 'corruption_loss_billion_usd', 'value']
                    ).properties(title='Estimated Annual Corruption Loss by Country', width=700)
                    st.altair_chart(bar_chart, use_container_width=True)
                else:
                    st.info("No data available for Control of Corruption")
            except Exception as e:
                st.error(f"Error creating visualization: {str(e)}")
            
            st.markdown("---")
            st.markdown("**Learn More:**")
            st.markdown("Corruption and bribery facilitate IFFs, erode trust in institutions, and hinder sustainable development. WGI's Control of Corruption index aggregates data from 30+ sources.")

# =============================================
# TAB 3: 4.4.3 Detection and Enforcement (2 indicators)
# =============================================
with tab3:
    st.markdown("This section covers the effectiveness of anti-IFF measures and capacity of tax and customs authorities. Data sources include World Justice Project, World Bank, and IMF ISORA.")
    
    # 2-column layout for 2 main indicators
    col1, col2 = st.columns(2, gap="large")
    
    # Indicator 4.4.3.1 - Effectiveness of Anti-IFF Measures
    with col1:
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.4.3.1: Effectiveness of Anti-IFF Measures</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 0.8rem;">
                Assesses the efficacy of efforts to combat IFFs using governance and regulatory indicators including Rule of Law and Control of Corruption.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("View Chart and Data", expanded=False):
            def show_rule_of_law_chart():
                indicator_label = "Rule of Law"
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
                else:
                    st.info("No data available for this indicator.")
            
            subindicators = {
                "Rule of Law (WJP)": {"content": show_rule_of_law_chart},
                "Control of Corruption": {"content": show_control_of_corruption_chart}
            }
            
            selected_sub = st.selectbox("Select sub-indicator:", list(subindicators.keys()), key="anti_iff_subindicator")
            subindicators[selected_sub]["content"]()
            
            st.markdown("---")
            st.markdown("**Learn More:**")
            st.markdown("The UNODC-OECD framework identifies governance and institutional quality as key determinants of anti-IFF effectiveness. The World Justice Project, World Bank, and Mo Ibrahim Index provide validated, cross-country governance data relevant to financial crime control.")
    
    # Indicator 4.4.3.2 - Capacity of Tax and Customs Authorities
    with col2:
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.4.3.2: Capacity of Tax and Customs Authorities</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 0.8rem;">
                Assesses the capacity and effectiveness of tax and customs authorities in detecting and preventing IFFs. Includes operational metrics, resources, and human capital strength.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("View Chart and Data", expanded=False):
            operational_indicators = {
                "Number of criminal investigations": "Role of the administration in tax crime investigations - Conducting investigations, under direction of other agency",
                "Total tax administration FTEs": "Total tax administration FTEs - Derived"
            }
            
            selected_ops = st.selectbox(
                "Select Capacity Indicator:",
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
            else:
                st.info(f"No data available for {display_name}.")
            
            st.markdown("---")
            st.markdown("**Learn More:**")
            st.markdown("The IMF ISORA survey provides comprehensive, cross-country data on tax and customs administration operations. Resource allocation, staff capacity, and operational effectiveness are key determinants of the ability to detect and prevent IFFs.")

# =============================================
# TAB 4: 4.4.4 Financial Secrecy (2 indicators)
# =============================================
with tab4:
    st.markdown("This section analyzes financial secrecy indicators, including offshore account usage and secrecy jurisdiction ratings.")
    
    # 2-column layout for 2 main indicators
    col1, col2 = st.columns(2, gap="large")
    
    # Indicator 4.4.4.1 - Use of Offshore Accounts
    with col1:
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.4.4.1: Use of Offshore Accounts</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 0.8rem;">
                The Financial Secrecy Index (FSI) measures the volume and value of funds held in offshore accounts. Higher scores indicate greater financial secrecy.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("View Chart and Data", expanded=False):
            try:
                fsi_data = filtered_data[filtered_data['indicator_label'].str.contains('fsi_', na=False) & 
                                        filtered_data['indicator_label'].str.contains('_value', na=False)]
                
                if not fsi_data.empty:
                    years = sorted(fsi_data['indicator_label'].str.extract(r'fsi_(\d{4})_value')[0].dropna().unique())
                    if years:
                        selected_year = st.selectbox(
                            "Select Year:",
                            options=years,
                            key="fsi_year_selectbox"
                        )
                        year_data = fsi_data[fsi_data['indicator_label'] == f'fsi_{selected_year}_value']
                        
                        if not year_data.empty:
                            visualize_indicator(
                                df=year_data,
                                indicator_label=f'fsi_{selected_year}_value',
                                chart_type="bar",
                                title=f"Financial Secrecy Index - {selected_year}",
                                y_title="Index Score",
                                x_title="Country",
                                color_by="country_or_area"
                            )
                        else:
                            st.info(f"No data available for {selected_year}")
                    else:
                        st.info("No year data found in FSI indicators")
                else:
                    st.info("No data available for Financial Secrecy Index")
            except Exception as e:
                st.error(f"Error creating visualization: {str(e)}")
            
            st.markdown("---")
            st.markdown("**Learn More:**")
            st.markdown("The FSI measures the volume of financial services provided to non-residents and assesses the secrecy of jurisdictions. It combines both factors to create a comprehensive index of financial opacity.")
    
    # Indicator 4.4.4.2 - Secrecy Jurisdiction Index
    with col2:
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.4.4.2: Secrecy Jurisdiction Index</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 0.8rem;">
                The Corporate Tax Haven Index (CTHI) measures how much each country's tax and financial systems enable multinational corporations to avoid paying tax.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("View Chart and Data", expanded=False):
            tax_haven_indicators = {
                "CTHI 2019 Score": "cthi_2019_score",
                "CTHI 2021 Score": "cthi_2021_score",
                "CTHI 2021 Rank": "cthi_2021_rank"
            }
            
            selected_th = st.selectbox(
                "Select Corporate Tax Haven Indicator:",
                options=list(tax_haven_indicators.keys()),
                key="tax_haven_selectbox"
            )
            
            label = tax_haven_indicators[selected_th]
            data = filtered_data[filtered_data['indicator_label'] == label]
            is_rank = "rank" in label
            y_title = "Rank" if is_rank else "Score"
            
            if not data.empty:
                visualize_indicator(
                    df=data,
                    indicator_label=label,
                    chart_type="bar",
                    title=f"Corporate Tax Haven Index - {selected_th}",
                    y_title=y_title,
                    x_title="Country",
                    color_by="country_or_area"
                )
            else:
                st.info(f"No data available for {selected_th}")
            
            st.markdown("---")
            st.markdown("**Learn More:**")
            st.markdown("The CTHI is based on 20 key indicators of corporate tax haven activity. Higher scores indicate greater facilitation of corporate tax abuse. Countries are ranked from 1 (worst) to 64 (best).")

# =============================================
# TAB 5: 4.4.5 Impact on Development Finance (2 indicators)
# =============================================
with tab5:
    st.markdown("This section assesses the impact of IFFs on development finance, focusing on reductions in financial leakages and improvements in government revenue collection.")
    
    # 2-column layout for 2 indicators
    col1, col2 = st.columns(2, gap="large")
    
    # Indicator 4.4.5.1 - Tax Buoyancy
    with col1:
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.4.5.1: Tax Buoyancy</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 0.8rem;">
                Ratio of change in tax revenue in relation to change in GDP. Measures how responsive a taxation policy is to growth in economic activities. Used as a proxy for reduction in financial leakages.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("View Chart and Data", expanded=False):
            tax_buoyancy_indicators = [
                "Tax Revenue - % of GDP - Buoyancy",
                "Income Taxes - % of GDP - Buoyancy",
                "Property Taxes - % of GDP - Buoyancy"
            ]
            
            available_buoyancy = [label for label in tax_buoyancy_indicators if label in filtered_data['indicator_label'].unique()]
            
            if available_buoyancy:
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
                else:
                    st.info(f"No data available for {selected_buoyancy}")
            else:
                st.info("No tax buoyancy indicators available")
            
            st.markdown("---")
            st.markdown("**Learn More:**")
            st.markdown("A buoyancy greater than 1 indicates that tax revenue is growing faster than GDP, reflecting effective tax policy and administration. Tax buoyancy reflects the effectiveness of tax policy in mobilizing domestic resources for development.")
    
    # Indicator 4.4.5.2 - Social Impact of Lost Tax
    with col2:
        st.markdown("""
        <div class='indicator-card'>
            <h4>Indicator 4.4.5.2: Social Impact of Lost Tax</h4>
            <p style="color: #555; line-height: 1.6; margin-bottom: 0.8rem;">
                Tax loss equivalent to the percentage of health and education budget. Shows what percentage of essential public services could have been funded with lost tax revenue.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("View Chart and Data", expanded=False):
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
            else:
                st.info("No data available for Tax Loss as % of Health and Education Budget")
            
            st.markdown("---")
            st.markdown("**Learn More:**")
            st.markdown("This indicator shows the opportunity cost of tax losses in terms of essential public services. The indicator uses data from the State of Tax Justice report, which provides standardized estimates of tax losses and their impact on public services across countries.")

# =============================================
# TAB 6: 4.4.6 Policy Environment (Narrative only)
# =============================================
with tab6:
    st.markdown("""
    ### Policy and Regulatory Environment
    
    This section assesses the implementation and effectiveness of policies aimed at reducing illicit financial flows (IFFs), with a focus on sector-specific regulations and international cooperation frameworks.
    
    #### Policy Areas Assessed:
    
    **1. National Anti-IFF Policies**  
    Laws and regulations targeting money laundering, tax evasion, and corruption. Effective policy implementation is a key determinant of a country's ability to reduce IFFs.
    
    **2. Sectoral Regulations**  
    Mining, extractives, and natural resources taxation frameworks. Lists the laws and regulations that govern the taxation and mining activity of each country, including general regime and mining regime counts.
    
    **3. International Cooperation**  
    Treaty participation (OECD BEPS, FATF recommendations, UN Conventions). Includes:
    - Tax treaty network coverage
    - Participation in automatic exchange of information (AEOI)
    - Beneficial ownership transparency requirements
    - Anti-money laundering (AML) framework strength
    - Extractive industries transparency (EITI) participation
    - Cross-border cooperation mechanisms
    
    **4. Beneficial Ownership**  
    Corporate transparency and registry requirements to track ultimate ownership and control of companies and assets.
    
    **5. Tax Information Exchange**  
    Bilateral and multilateral agreements for automatic information sharing between tax authorities to combat cross-border tax evasion.
    
    **6. Rent Sharing in Mining**  
    Examines rent sharing arrangements between the state and investors in the mining sector. Uses the Legal and Tax Database on Gold Mining in Africa to assess how mining rents are distributed between the state and private investors.
    
    ---
    
    **Assessment Methodology:**
    
    1. **Policy Count**: Number of anti-IFF laws and regulations enacted
    2. **Implementation Score**: Effectiveness of policy enforcement (qualitative assessment)
    3. **International Alignment**: Compliance with global standards (FATF, OECD BEPS)
    4. **Institutional Capacity**: Adequacy of enforcement agencies and resources
    
    ---
    
    **Data Sources:**  
    - OECD Global Forum on Transparency and Exchange of Information for Tax Purposes
    - FATF Mutual Evaluation Reports
    - UNODC Anti-Corruption and Anti-Money Laundering Database
    - ICTD Legal and Tax Database on Gold Mining in Africa
    - National legislation databases
    
    *Note: Detailed policy assessment data requires manual compilation from multiple sources and is not included in quantitative indicators.*
    """)

# ========================================
# SECTION: Data Gaps / Availability
# ========================================
st.divider()
st.markdown("### Data Availability in Africa")

all_indicators_4_4 = {
    "Trade Mispricing - USD Millions": "The Sums of the Value Gaps Identified in Trade Between 134 Developing Countries and 36 Advanced Economies, 2009–2018, in USD Millions",
    "Trade Mispricing - % of Trade": "The Total Value Gaps Identified Between 134 Developing Countries and 36 Advanced Economies, 2009–2018, as a Percent of Total Trade",
    "Control of Corruption": "Control of Corruption",
    "Rule of Law": "Rule of Law",
    "Tax Buoyancy": "Tax Revenue - % of GDP - Buoyancy"
}

# Calculate coverage summary
countries_with_data = df_africa[df_africa['indicator_label'].isin(all_indicators_4_4.values())]['country_or_area'].nunique()
total_africa_countries = len(africa_countries)
coverage = round((countries_with_data / total_africa_countries * 100)) if total_africa_countries > 0 else 0

st.markdown(f"""
<div class="data-availability-box">
  <div class="left">
    <h4>Data Availability in Africa</h4>
    <p>
      Data availability determines how confidently we can interpret IFF trends across Africa. 
      This view highlights which countries report recent data and where gaps persist — often due to differences in measurement capacity, reporting cycles, or data sensitivity.
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
        options=list(all_indicators_4_4.keys()),
        key="topic4_4_gap_indicator_select"
    )
    uv.render_data_availability_heatmap(
        df=df_africa,
        indicator_label=all_indicators_4_4[selected_gap_indicator],
        title=f"Data Availability for {selected_gap_indicator} (Africa)",
        container_key="topic4_4_gap"
    )
