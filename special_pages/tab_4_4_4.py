import streamlit as st
import pandas as pd
from universal_viz import visualize_indicator

def render_financial_secrecy_tab(filtered_data, filters):
    st.header("4.4.4: Financial Secrecy")
    st.markdown("""
This section analyzes financial secrecy indicators, including offshore account usage and secrecy jurisdiction ratings.
    """)

    # 4.4.4.1: Use of Offshore Accounts
    st.subheader("4.4.4.1: Use of Offshore Accounts")
    st.caption("Proxied by Financial Secrecy Index")
    try:
        fsi_data = filtered_data[filtered_data['indicator_label'].str.startswith('fsi_') & \
                                filtered_data['indicator_label'].str.endswith('_value')]
        if not fsi_data.empty:
            years = sorted(fsi_data['indicator_label'].str.extract('fsi_(\d{4})_value')[0].unique())
            selected_year = st.selectbox(
                "Select Year:",
                options=years,
                key="fsi_year_selectbox"
            )
            year_data = fsi_data[fsi_data['indicator_label'] == f'fsi_{selected_year}_value']
            if 'country_or_area' not in year_data.columns:
                if 'country_or_area' in filtered_data.columns:
                    year_data = year_data.merge(
                        filtered_data[['country_or_area']].drop_duplicates(),
                        left_index=True, right_index=True, how='left'
                    )
            if 'country_or_area' in year_data.columns:
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
                st.warning("No country information available for this indicator/year.")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Score", f"{year_data['value'].mean():.1f}")
            with col2:
                st.metric("Maximum Score", f"{year_data['value'].max():.1f}")
            with col3:
                st.metric("Minimum Score", f"{year_data['value'].min():.1f}")
            with st.expander("View Data Table"):
                st.dataframe(
                    year_data[['country_or_area', 'year', 'value']]
                    .sort_values('value', ascending=False)
                )
        else:
            st.info("No data available for Financial Secrecy Index")
    except Exception as e:
        st.error(f"Error creating visualization: {str(e)}")
    with st.expander("Learn more about Indicator 4.4.4.1: Use of Offshore Accounts"):
        st.markdown("""
**Definition:** The Financial Secrecy Index (FSI) measures the volume and value of funds held in offshore accounts by residents.

**Data Source:** Financial Secrecy Index (FSI)

**Methodology:**
- Measures the volume of financial services provided to non-residents
- Assesses the secrecy of jurisdictions
- Combines both factors to create a comprehensive index
- Higher scores indicate greater financial secrecy

**Indicator Format:** fsi_YYYY_value (e.g., fsi_2011_value)
        """)

    # 4.4.4.2: Secrecy Jurisdiction Index
    st.subheader("4.4.4.2: Secrecy Jurisdiction Index")
    st.markdown("#### 4.4.4.2.a: Corporate Tax Haven Index")
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
    display_name = selected_th
    label = tax_haven_indicators[display_name]
    data = filtered_data[filtered_data['indicator_label'] == label]
    is_rank = "rank" in label
    y_title = "Rank" if is_rank else "Score"
    sort_order = True if is_rank else False
    if not data.empty:
        visualize_indicator(
            df=data,
            indicator_label=label,
            chart_type="bar",
            title=f"Corporate Tax Haven Index - {display_name}",
            y_title=y_title,
            x_title="Country",
            color_by="country_or_area"
        )
        with st.expander(f"View Data Table: {display_name}"):
            pass
    else:
        st.info(f"No data available for {display_name}")
    with st.expander("Learn more about Corporate Tax Haven Index"):
        st.markdown("""
**Definition:** The Corporate Tax Haven Index (CTHI) measures how much each country's tax and financial systems enable multinational corporations to avoid paying tax.

**Components:**
1. **CTHI Score:**
   - 2019 and 2021 scores available
   - Higher scores indicate greater facilitation of corporate tax abuse
   - Based on 20 key indicators of corporate tax haven activity

2. **CTHI Rank:**
   - 2021 ranking available
   - Lower rank numbers indicate higher levels of corporate tax haven activity
   - Countries are ranked from 1 (worst) to 64 (best)

**Data Source:** Corporate Tax Haven Index (CTHI)
        """)

    st.markdown("#### 4.4.4.2.b: Countries' Profit and Tax Loss to Global Corporate Tax Abuse")
    tax_loss_indicators = {
        "2020 Annual Tax Loss (USD millions)": "sotj20_loss_corp_musd",
        "2021 Annual Tax Loss (USD millions)": "sotj21_loss_corp_musd",
        "2023 Annual Tax Loss (USD millions)": "sotj23_loss_corp_musd"
    }
    selected_tl = st.selectbox(
        "Select Tax Loss Year:",
        options=list(tax_loss_indicators.keys()),
        key="tax_loss_year_selectbox"
    )
    display_name = selected_tl
    label = tax_loss_indicators[display_name]
    data = filtered_data[filtered_data['indicator_label'] == label]
    if not data.empty:
        visualize_indicator(
            df=data,
            indicator_label=label,
            chart_type="bar",
            title=f"Corporate Tax Abuse - {display_name}",
            y_title=display_name,
            x_title="Country",
            color_by="country_or_area"
        )
        with st.expander(f"View Data Table: {display_name}"):
            pass
    else:
        st.info(f"No data available for {display_name}")
    with st.expander("Learn more about Indicator 4.4.4.2: Secrecy Jurisdiction Index"):
        st.markdown("""
**Definition:** The Secrecy Jurisdiction Index rates countries based on their involvement in financial secrecy and facilitation of illicit financial flows.

**Components:**
1. **Corporate Tax Haven Index (CTHI):**
   - Score: Overall rating of tax haven characteristics
   - Rank: Relative position among all jurisdictions
   - Share: Proportion of global financial secrecy

2. **Countries' Profit and Tax Loss:**
   - Annual tax loss in USD millions
   - Annual tax loss as percentage of GDP

**Data Sources:**
- Corporate Tax Haven Index
- Global Tax Justice Network data

**Methodology:**
- Combines multiple indicators of financial secrecy
- Assesses both legal and practical aspects of tax haven status
- Measures impact on global tax revenue
        """) 