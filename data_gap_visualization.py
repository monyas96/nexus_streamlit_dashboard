import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional, Union

def create_data_gap_map(
    df: pd.DataFrame,
    indicator_label: str,
    reference_data: pd.DataFrame,
    title: str = "Data Availability Map",
    container_key: Optional[str] = None
) -> None:
    """
    Creates a choropleth map showing data availability for a specific indicator.
    
    Args:
        df: Main dataframe containing the indicator data
        indicator_label: The indicator to check for data availability
        reference_data: Reference dataframe containing country codes
        title: Title for the map
        container_key: Unique key for Streamlit elements
    """
    # Filter for the indicator
    df_ind = df[df['indicator_label'] == indicator_label].copy()
    
    # Create availability dataframe
    if not df_ind.empty:
        # Get latest year per country
        latest_data = df_ind.sort_values('year').groupby('country_or_area').last().reset_index()
        # Merge with reference data to get all countries
        availability_df = reference_data[['Country or Area', 'iso3']].merge(
            latest_data[['country_or_area', 'value']],
            left_on='Country or Area',
            right_on='country_or_area',
            how='left'
        )
        # Create binary availability column
        availability_df['has_data'] = availability_df['value'].notna().astype(int)
    else:
        # If no data, create empty availability dataframe
        availability_df = reference_data[['Country or Area', 'iso3']].copy()
        availability_df['has_data'] = 0
    
    # Create choropleth map
    fig = px.choropleth(
        availability_df,
        locations='iso3',
        locationmode='ISO-3',
        color='has_data',
        hover_name='Country or Area',
        color_continuous_scale='Blues',
        title=title,
        scope="africa"
    )
    
    fig.update_layout(
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            lakecolor='rgba(0,0,0,0)',
            landcolor='rgba(217, 217, 217, 1)',
            subunitcolor='white'
        ),
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    
    # Display the map
    st.plotly_chart(fig, use_container_width=True, key=f"{container_key}_gap_map" if container_key else None)
    
    # Add legend explanation
    st.caption("🟢 Data Available | 🔴 Data Not Available")

def create_data_gap_heatmap(
    df: pd.DataFrame,
    indicator_label: str,
    title: str = "Data Availability Heatmap",
    container_key: Optional[str] = None
) -> None:
    """
    Creates a heatmap showing data availability across years and countries.
    
    Args:
        df: Main dataframe containing the indicator data
        indicator_label: The indicator to check for data availability
        title: Title for the heatmap
        container_key: Unique key for Streamlit elements
    """
    # Filter for the indicator
    df_ind = df[df['indicator_label'] == indicator_label].copy()
    
    if not df_ind.empty:
        # Create binary availability column
        df_ind['has_data'] = 1
        
        # Pivot to create heatmap data
        heatmap_df = df_ind.pivot_table(
            index='country_or_area',
            columns='year',
            values='has_data',
            aggfunc='max',
            fill_value=0
        )
        
        # Sort years for readability
        heatmap_df = heatmap_df.sort_index(axis=1)
        
        # Create heatmap with discrete red/green color scale
        fig = px.imshow(
            heatmap_df,
            labels=dict(x="Year", y="Country", color="Data Present"),
            color_continuous_scale="Blues",
            aspect="auto",
            title=title
        )
        fig.update_xaxes(side="top")
        fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
        
        # Display the heatmap
        st.plotly_chart(fig, use_container_width=True, key=f"{container_key}_gap_heatmap" if container_key else None)
    else:
        st.info(f"No data available for indicator: {indicator_label}")

def render_data_gap_section(
    df: pd.DataFrame,
    indicator_label: str,
    reference_data: pd.DataFrame,
    title: str = "Data Availability Analysis",
    container_key: Optional[str] = None
) -> None:
    """
    Renders a complete data gap analysis section with both map and heatmap.
    
    Args:
        df: Main dataframe containing the indicator data
        indicator_label: The indicator to analyze
        reference_data: Reference dataframe containing country codes
        title: Title for the section
        container_key: Unique key for Streamlit elements
    """
    st.markdown(f"### {title}")
    
    # Create tabs for different visualizations
    tab1, tab2 = st.tabs(["Geographical Distribution", "Temporal Coverage"])
    
    with tab1:
        create_data_gap_map(
            df=df,
            indicator_label=indicator_label,
            reference_data=reference_data,
            title="Data Availability by Country",
            container_key=f"{container_key}_map" if container_key else None
        )
    
    with tab2:
        create_data_gap_heatmap(
            df=df,
            indicator_label=indicator_label,
            title="Data Availability by Year and Country",
            container_key=f"{container_key}_heatmap" if container_key else None
        ) 