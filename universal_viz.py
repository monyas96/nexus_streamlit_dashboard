import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from pathlib import Path
import random
import altair as alt
from typing import Optional, List, Dict, Union, Any, Callable

# 1. Core visualization functions:

def visualize_indicator(
    df: pd.DataFrame,
    indicator_label: Optional[str] = None,
    indicator_code: Optional[str] = None,
    calculation_function: Optional[Callable] = None,
    chart_type: str = "bar",
    countries: Optional[List[str]] = None,
    y_title: str = "Value",
    x_title: str = "Year",
    title: Optional[str] = None,
    show_chart: bool = True,
    color_by: str = "country_or_area",
    stack: bool = False,
    color_scale: Optional[Dict[str, str]] = None,
    x_field: str = "year",
    x_sort: Optional[str] = None,
    facet_by: Optional[str] = None,
    facet_cols: int = 2,
    domain: Optional[List[str]] = None,
    width: int = 700,
    height: int = 400
) -> alt.Chart:
    """
    Enhanced visualization function for indicators with improved error handling.

    Args:
        df: Main dataset
        indicator_label: Label to match from data
        indicator_code: Optional code to match from data (takes precedence over label if provided)
        calculation_function: Optional function to compute derived indicators
        chart_type: Type of chart ('bar', 'line', 'stacked_bar', 'area', 'point')
        countries: List of ISO3 codes to filter
        y_title: Y-axis label
        x_title: X-axis label
        title: Chart title
        show_chart: Whether to display in Streamlit
        color_by: Column for color encoding
        stack: Whether to stack elements
        color_scale: Color mapping
        x_field: Field for x-axis
        x_sort: Sort order for x-axis
        facet_by: Field for faceting
        facet_cols: Number of facet columns
        domain: Domain for color scale
        width: Chart width
        height: Chart height

    Returns:
        Altair Chart object
    """
    # Check for valid chart type first
    chart_configs = {
        "bar": lambda data: alt.Chart(data).mark_bar(),
        "stacked_bar": lambda data: alt.Chart(data).mark_bar(),
        "line": lambda data: alt.Chart(data).mark_line(point=True),
        "area": lambda data: alt.Chart(data).mark_area(opacity=0.5 if not stack else 1),
        "point": lambda data: alt.Chart(data).mark_circle(size=60)
    }

    if chart_type not in chart_configs:
        raise ValueError(f"Unsupported chart_type: {chart_type}")

    try:
        # Get data based on input parameters
        if calculation_function:
            filtered = calculation_function()
            # Add debug info to session state
            if "debug" not in st.session_state:
                st.session_state.debug = {}
            st.session_state.debug["calc_function_rows"] = len(filtered)
        elif indicator_code:
            filtered = df[df["indicator_code"] == indicator_code].copy()
            # Add debug info to session state
            if "debug" not in st.session_state:
                st.session_state.debug = {}
            st.session_state.debug["indicator_code_rows"] = len(filtered)
            st.session_state.debug["indicator_code"] = indicator_code
        elif indicator_label:
            filtered = df[df["indicator_label"] == indicator_label].copy()
            # Add debug info to session state
            if "debug" not in st.session_state:
                st.session_state.debug = {}
            st.session_state.debug["indicator_rows"] = len(filtered)
            st.session_state.debug["indicator_name"] = indicator_label
        else:
            raise ValueError("Either indicator_label, indicator_code, or calculation_function must be provided")

        # Filter by countries if specified
        if countries and len(countries) > 0:
            filtered = filtered[filtered["iso3"].isin(countries)]
            # Add debug info to session state
            if "debug" not in st.session_state:
                st.session_state.debug = {}
            st.session_state.debug["after_country_filter_rows"] = len(filtered)

        # Check if we have data
        if len(filtered) == 0:
            st.warning(f"No data available for {'the selected countries' if countries else 'the selected parameters'}")

            # If no data, create a minimal placeholder visualization
            empty_data = pd.DataFrame({
                'year': [2020],
                'value': [0],
                'message': ['No data available']
            })

            empty_chart = alt.Chart(empty_data).mark_text(
                align='center',
                baseline='middle',
                fontSize=20
            ).encode(
                text='message'
            ).properties(
                width=width,
                height=height,
                title=title or "No Data Available"
            )

            if show_chart:
                st.altair_chart(empty_chart, use_container_width=True)

            return empty_chart

        # Ensure country_or_area is present for coloring
        if "country_or_area" not in filtered.columns and "iso3" in filtered.columns:
            # Handle missing country_or_area column
            if "iso3" in df.columns and "country_or_area" in df.columns:
                country_mapping = df[["iso3", "country_or_area"]].drop_duplicates()
                filtered = filtered.merge(country_mapping, on="iso3", how="left")
            else:
                # If we can't find a mapping in the main df, create a simple one
                filtered["country_or_area"] = filtered["iso3"]

        # Setup color configuration
        color_config = {}
        if color_scale:
            color_config["scale"] = alt.Scale(domain=domain, range=list(color_scale.values()))

        # Set default title if none provided
        if not title and indicator_label:
            title = indicator_label
        elif not title and calculation_function:
            title = "Custom Indicator"

        # Create base chart
        base = chart_configs[chart_type](filtered)

        # Configure x-axis
        x_encode = alt.X(f"{x_field}:O", title=x_title)
        if x_sort:
            x_encode = alt.X(f"{x_field}:O", title=x_title, sort=x_sort)

        # Configure encoding based on stacking
        if stack:
            chart = base.encode(
                x=x_encode,
                y=alt.Y("value:Q", title=y_title, stack="zero"),
                color=alt.Color(f"{color_by}:N", title=color_by.replace('_', ' ').title(), **color_config),
                tooltip=["country_or_area", x_field, "value", color_by]
            )
        else:
            chart = base.encode(
                x=x_encode,
                y=alt.Y("value:Q", title=y_title),
                color=alt.Color(f"{color_by}:N", title=color_by.replace('_', ' ').title(), **color_config),
                tooltip=["country_or_area", x_field, "value", color_by]
            )

        # Set chart properties
        chart = chart.properties(
            title=title,
            width=width,
            height=height
        )

        # Handle faceting if requested
        if facet_by and facet_by in filtered.columns:
            chart = chart.facet(
                facet=alt.Facet(f"{facet_by}:N", title=facet_by.replace('_', ' ').title()),
                columns=facet_cols
            ).resolve_scale(y='independent')

        # Display the chart if requested
        if show_chart:
            st.altair_chart(chart, use_container_width=True)

        return chart

    except Exception as e:
        # Provide detailed error information
        import traceback
        error_details = traceback.format_exc()

        # Don't catch ValueError for invalid chart_type
        if isinstance(e, ValueError) and "chart_type" in str(e):
            raise

        st.error(f"Error generating visualization: {str(e)}")
        st.error(f"Debug info: chart_type={chart_type}, countries={countries[:3] if countries else None}...")

        # Create a simple error chart
        error_data = pd.DataFrame({'x': [0], 'y': [0], 'message': ['Error in visualization']})
        error_chart = alt.Chart(error_data).mark_text(
            align='center', baseline='middle', fontSize=16, color='red'
        ).encode(text='message').properties(width=width, height=height, title="Visualization Error")

        if show_chart:
            st.altair_chart(error_chart, use_container_width=True)

        return error_chart

def create_choropleth_map(
    data,
    location_column='country',
    value_column='value',
    title='Choropleth Map',
    reference_data=None,
    iso_column='iso3',
    color_continuous_scale="Blues",
    range_color=None,
    height=600,
    width=None
):
    """
    Creates an interactive choropleth map using Plotly Express.

    Args:
        data (pd.DataFrame): Dataframe containing the data to plot.
        location_column (str): Column name for country names or ISO codes.
        value_column (str): Column name for the values to plot.
        title (str): Title of the map.
        reference_data (pd.DataFrame, optional): Dataframe with country codes and potentially coordinates.
        iso_column (str): Column name in reference_data containing ISO Alpha-3 codes.
        color_continuous_scale (str or list): Plotly color scale.
        range_color (tuple, optional): Min and max values for the color scale.
        height (int): Height of the map figure.
        width (int, optional): Width of the map figure. Defaults to container width.

    Returns:
        plotly.graph_objects.Figure: The generated choropleth map figure.
    """
    if data is None or data.empty:
        st.warning("No data provided for choropleth map.")
        # Return an empty figure or a message figure
        fig = go.Figure()
        fig.update_layout(
            title_text=f"{title} (No Data)",
            height=height,
            width=width,
            geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='rgba(0,0,0,0)'),
            annotations=[dict(text="No data available", showarrow=False)]
        )
        return fig

    plot_data = data.copy()

    # Try to map country names to ISO codes if reference_data is provided
    location_mode = 'country names' # Default
    if reference_data is not None and not reference_data.empty:
        # Ensure ISO column exists in reference data
        if iso_column not in reference_data.columns:
            st.error(f"ISO column '{iso_column}' not found in reference data.")
            return go.Figure().update_layout(title_text=f"{title} (Error: Missing ISO Column)", height=height, width=width)

        # Standardize names in both dataframes for better matching
        if location_column in plot_data.columns:
            plot_data[f'{location_column}_std'] = plot_data[location_column].apply(standardize_country_name)
        else:
             st.error(f"Location column '{location_column}' not found in plot data.")
             return go.Figure().update_layout(title_text=f"{title} (Error: Missing Location Column)", height=height, width=width)

        ref_data_std = reference_data.copy()
        # Use the correct country column from reference data
        country_col = 'Country or Area' if 'Country or Area' in ref_data_std.columns else 'Country'
        ref_data_std['country_std'] = ref_data_std[country_col].apply(standardize_country_name)

        # Create mapping from standardized name to ISO code
        name_to_iso = ref_data_std.set_index('country_std')[iso_column].to_dict()

        # Map ISO codes
        plot_data['iso_code'] = plot_data[f'{location_column}_std'].map(name_to_iso)

        # Check how many were successfully mapped
        mapped_count = plot_data['iso_code'].notna().sum()
        if mapped_count > 0:
            location_mode = 'ISO-3'
            locations = 'iso_code'
            # Optional: Log unmapped countries
            unmapped_raw = plot_data[plot_data['iso_code'].isna()][location_column].unique()
            # Filter out None/NaN values and convert items to string before joining
            unmapped_clean = [str(item) for item in unmapped_raw if pd.notna(item)]
            if len(unmapped_clean) > 0:
                st.info(f"Could not map ISO codes for: {', '.join(unmapped_clean[:5])}{'...' if len(unmapped_clean) > 5 else ''}")
        else:
            st.warning("Could not map any countries to ISO codes. Using country names.")
            locations = location_column # Fallback to original names
    else:
        locations = location_column # Use original names if no ref data

    # Ensure value column exists
    if value_column not in plot_data.columns:
        st.error(f"Value column '{value_column}' not found in data.")
        # Return an empty figure or a message figure
        fig = go.Figure()
        fig.update_layout(
            title_text=f"{title} (Error: Missing Value Column)",
            height=height,
            width=width,
            annotations=[dict(text=f"Error: Column '{value_column}' not found.", showarrow=False)]
        )
        return fig

    # Handle potential non-numeric data in value_column
    plot_data[value_column] = pd.to_numeric(plot_data[value_column], errors='coerce')
    plot_data = plot_data.dropna(subset=[value_column]) # Remove rows where conversion failed

    if plot_data.empty:
         st.warning("No valid numeric data to plot after cleaning.")
         fig = go.Figure().update_layout(title_text=f"{title} (No Valid Data)", height=height, width=width)
         return fig


    try:
        fig = px.choropleth(
            plot_data,
            locations=locations,
            locationmode=location_mode,
            color=value_column,
            hover_name=location_column, # Show original country name on hover
            hover_data={value_column: ':.2f', locations: False}, # Format value, hide internal ID
            title=title,
            color_continuous_scale=color_continuous_scale,
            range_color=range_color,
            scope="africa" # Focus map on Africa
        )

        fig.update_layout(
            height=height,
            width=width,
            geo=dict(
                bgcolor='rgba(0,0,0,0)',
                lakecolor='rgba(0,0,0,0)',
                landcolor='rgba(217, 217, 217, 1)',
                subunitcolor='white'
            ),
            margin={"r":0,"t":40,"l":0,"b":0} # Adjust margins
        )
        return fig

    except Exception as e:
        st.error(f"Error creating choropleth map: {e}")
        # Return an empty figure or a message figure
        fig = go.Figure()
        fig.update_layout(
            title_text=f"{title} (Plotting Error)",
            height=height,
            width=width,
            annotations=[dict(text=f"Error: {e}", showarrow=False)]
        )
        return fig

def create_line_chart(
    data,
    x_column,
    y_column,
    color_column=None,
    title='Line Chart',
    x_label=None,
    y_label=None,
    legend_title=None,
    height=400,
    width=None
):
    """
    Creates an interactive line chart using Plotly Express.

    Args:
        data (pd.DataFrame): Dataframe containing the data to plot.
        x_column (str): Column name for the x-axis.
        y_column (str): Column name for the y-axis.
        color_column (str, optional): Column name for coloring lines (e.g., by country).
        title (str): Title of the chart.
        x_label (str, optional): Label for the x-axis.
        y_label (str, optional): Label for the y-axis.
        legend_title (str, optional): Title for the legend.
        height (int): Height of the chart figure.
        width (int, optional): Width of the chart figure.

    Returns:
        plotly.graph_objects.Figure: The generated line chart figure.
    """
    if data is None or data.empty:
        st.warning("No data provided for line chart.")
        # Return an empty figure or a message figure
        fig = go.Figure()
        fig.update_layout(
            title_text=f"{title} (No Data)",
            height=height,
            width=width,
            xaxis_title=x_label or x_column,
            yaxis_title=y_label or y_column,
            annotations=[dict(text="No data available", showarrow=False)]
        )
        return fig

    # Ensure essential columns exist
    required_cols = [x_column, y_column]
    if color_column:
        required_cols.append(color_column)
    missing_cols = [col for col in required_cols if col not in data.columns]
    if missing_cols:
        st.error(f"Missing required columns for line chart: {', '.join(missing_cols)}")
        fig = go.Figure().update_layout(title_text=f"{title} (Error: Missing Columns)", height=height, width=width)
        return fig

    # Convert y_column to numeric, coercing errors
    data[y_column] = pd.to_numeric(data[y_column], errors='coerce')
    # Optional: Convert x_column if it's supposed to be numeric/datetime
    # data[x_column] = pd.to_numeric(data[x_column], errors='coerce') # If x is year/numeric
    # data[x_column] = pd.to_datetime(data[x_column], errors='coerce') # If x is date

    plot_data = data.dropna(subset=[y_column]) # Remove rows where y-value is invalid

    if plot_data.empty:
         st.warning("No valid numeric data to plot after cleaning.")
         fig = go.Figure().update_layout(title_text=f"{title} (No Valid Data)", height=height, width=width)
         return fig

    try:
        fig = px.line(
            plot_data,
            x=x_column,
            y=y_column,
            color=color_column,
            title=title,
            labels={
                x_column: x_label or x_column.replace('_', ' ').title(),
                y_column: y_label or y_column.replace('_', ' ').title(),
                color_column: legend_title or (color_column.replace('_', ' ').title() if color_column else None)
            },
            markers=True # Add markers to the lines
        )

        fig.update_layout(
            height=height,
            width=width,
            legend_title_text=legend_title or (color_column.replace('_', ' ').title() if color_column else ''),
            xaxis=dict(type='category') if data[x_column].dtype == 'object' else None # Treat x as category if object type
        )
        fig.update_traces(marker=dict(size=6)) # Adjust marker size

        return fig

    except Exception as e:
        st.error(f"Error creating line chart: {e}")
        fig = go.Figure()
        fig.update_layout(
            title_text=f"{title} (Plotting Error)",
            height=height,
            width=width,
            annotations=[dict(text=f"Error: {e}", showarrow=False)]
        )
        return fig

def create_bar_chart(
    data,
    x_column=None,
    y_column=None,
    color_column=None,
    title='Bar Chart',
    x_label=None,
    y_label=None,
    legend_title=None,
    orientation='v', # 'v' for vertical, 'h' for horizontal
    height=400,
    width=None,
    **kwargs
):
    """
    Creates an interactive bar chart using Plotly Express.
    """
    if data is None or data.empty:
        st.warning("No data provided for bar chart.")
        fig = go.Figure().update_layout(title_text=f"{title} (No Data)", height=height, width=width)
        return fig

    # Try to get x_axis and y_axis from arguments or kwargs
    x_axis = x_column or kwargs.get('x', None)
    y_axis = y_column or kwargs.get('y', None)
    if x_axis is None or y_axis is None:
        raise ValueError("Both x_axis and y_axis must be provided to create_bar_chart. Got x_axis={} y_axis={}".format(x_axis, y_axis))

    # Ensure essential columns exist
    required_cols = [x_axis, y_axis]
    if color_column:
        required_cols.append(color_column)
    missing_cols = [col for col in required_cols if col not in data.columns]
    if missing_cols:
        st.error(f"Missing required columns for bar chart: {', '.join(missing_cols)}")
        fig = go.Figure().update_layout(title_text=f"{title} (Error: Missing Columns)", height=height, width=width)
        return fig

    # Determine axes based on orientation
    if orientation == 'h':
        x_axis, y_axis = y_axis, x_axis
    # Convert the value axis to numeric
    value_axis = x_axis if orientation == 'h' else y_axis
    data[value_axis] = pd.to_numeric(data[value_axis], errors='coerce')
    plot_data = data.dropna(subset=[value_axis])

    if plot_data.empty:
         st.warning("No valid numeric data to plot after cleaning.")
         fig = go.Figure().update_layout(title_text=f"{title} (No Valid Data)", height=height, width=width)
         return fig

    try:
        fig = px.bar(
            plot_data,
            x=x_axis,
            y=y_axis,
            color=color_column,
            title=title,
            orientation=orientation,
            labels={
                x_axis: x_label or x_axis.replace('_', ' ').title(),
                y_axis: y_label or y_axis.replace('_', ' ').title(),
                color_column: legend_title or (color_column.replace('_', ' ').title() if color_column else None)
            },
            text_auto='.2f' # Display values on bars, formatted
        )

        fig.update_layout(
            height=height,
            width=width,
            legend_title_text=legend_title or (color_column.replace('_', ' ').title() if color_column else ''),
            xaxis_title=x_label or x_axis.replace('_', ' ').title(),
            yaxis_title=y_label or y_axis.replace('_', ' ').title(),
        )
        fig.update_traces(textposition='outside')

        return fig

    except Exception as e:
        st.error(f"Error creating bar chart: {e}")
        fig = go.Figure()
        fig.update_layout(
            title_text=f"{title} (Plotting Error)",
            height=height,
            width=width,
            annotations=[dict(text=f"Error: {e}", showarrow=False)]
        )
        return fig

# 2. Data handling functions:

def load_country_reference_data(file_path=None):
    """
    Loads country reference data from a CSV file.
    Keeps original column names from the CSV file.

    Args:
        file_path (str, optional): Path to the CSV file. If None, tries default paths.

    Returns:
        pd.DataFrame: Loaded reference data. Returns empty DataFrame on error.
    """
    # Define potential default paths relative to this script or a known location
    default_paths = [
        "data/iso3_country_reference.csv", # Primary expected location
        "../data/iso3_country_reference.csv", # If called from pages/
        Path(__file__).parent.parent / "data" / "iso3_country_reference.csv" # Relative to this file's location
    ]

    if file_path:
        paths_to_try = [file_path]
    else:
        paths_to_try = default_paths

    ref_data = None
    loaded_path = None

    for p in paths_to_try:
        try:
            # Ensure path exists before attempting to read
            path_obj = Path(p)
            if path_obj.is_file():
                ref_data = pd.read_csv(path_obj)
                loaded_path = path_obj
                break # Stop after successful load
        except Exception as e:
            st.error(f"Error loading reference data from {p}: {e}")
            continue

    if ref_data is None:
        st.error(f"Could not find or load country reference data. Tried paths: {[str(p) for p in paths_to_try]}")
        return pd.DataFrame()

    # Ensure essential columns exist
    required_ref_cols = ['Region Name', 'Country or Area', 'iso3']
    missing_cols = [col for col in required_ref_cols if col not in ref_data.columns]
    if missing_cols:
         st.warning(f"Reference data loaded from {loaded_path} is missing expected columns: {missing_cols}. Expected: {required_ref_cols}. Found: {list(ref_data.columns)}")

    # Optional: Fill missing regions if necessary
    if 'Region Name' in ref_data.columns:
        ref_data['Region Name'] = ref_data['Region Name'].fillna('Unknown')

    return ref_data

@st.cache_data # Cache the filtered result
def filter_dataframe_by_selections(df, filters, ref_data):
    """
    Filters the main dataframe based on selections from setup_sidebar_filters,
    handling both individual country selections and regional aggregations.

    Args:
        df (pd.DataFrame): The main dataframe to filter.
        filters (dict): Dictionary containing filter selections
                        (selected_region, selected_countries, year_range).
                        'selected_countries' can contain country names and/or
                        regional aggregate labels (e.g., "Africa (Region Average)").
        ref_data (pd.DataFrame): Country reference data with 'Region Name' and 'Country or Area'.

    Returns:
        pd.DataFrame: The filtered (and potentially aggregated) dataframe.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    # Ensure ref_data has the necessary columns ('Region Name', 'Country or Area')
    if ref_data is None or ref_data.empty or 'Region Name' not in ref_data.columns or 'Country or Area' not in ref_data.columns:
         st.warning("Reference data is missing or incomplete ('Region Name', 'Country or Area' columns). Skipping regional filtering/aggregation.")
         # Fallback to just year filtering if ref_data is bad
         filtered_df = df.copy()
         start_year, end_year = filters.get('year_range', (df['year'].min(), df['year'].max()))
         if start_year is not None and end_year is not None:
             filtered_df = filtered_df[(filtered_df['year'] >= start_year) & (filtered_df['year'] <= end_year)]
         return filtered_df

    # Make a copy to avoid modifying the original DataFrame
    df_processed = df.copy()

    # Extract filter values
    selected_countries_or_aggregates = filters.get('selected_countries', [])
    year_range = filters.get('year_range', (None, None))
    start_year, end_year = year_range

    # Separate individual countries and regional aggregate requests
    individual_countries = [c for c in selected_countries_or_aggregates if not c.endswith(" (Region Average)")]
    region_aggregate_labels = [c for c in selected_countries_or_aggregates if c.endswith(" (Region Average)")]

    results_dfs = [] # To store results for concatenation

    # --- 1. Filter by Year Range (apply to all further processing) ---
    if start_year is not None and end_year is not None:
        df_processed = df_processed[(df_processed['year'] >= start_year) & (df_processed['year'] <= end_year)]
    elif start_year is not None:
        df_processed = df_processed[df_processed['year'] >= start_year]
    elif end_year is not None:
        df_processed = df_processed[df_processed['year'] <= end_year]

    # --- Handle Empty Selection Case ---
    # If no specific countries or regional averages are selected, return the year-filtered data for all relevant countries
    # (This depends on whether a specific region was selected in the first dropdown)
    if not individual_countries and not region_aggregate_labels:
        selected_region = filters.get('selected_region')
        if selected_region == "All Regions" or selected_region is None:
            # If All Regions, return the fully year-filtered data
            return df_processed
        else:
            # If a specific region was selected, filter df_processed by that region
            countries_in_region = ref_data[ref_data['Region Name'] == selected_region]['Country or Area'].unique().tolist()
            country_col_in_df = 'country_or_area' if 'country_or_area' in df_processed.columns else 'Country'
            if country_col_in_df in df_processed.columns and countries_in_region:
                return df_processed[df_processed[country_col_in_df].isin(countries_in_region)].copy()
            else:
                # If filtering by region fails (missing col or no countries), return the year-filtered data as fallback
                 st.warning(f"Could not filter by selected region '{selected_region}' due to missing data/column. Showing all regions.")
                 return df_processed

    # --- 2. Process Individual Country Selections ---
    if individual_countries:
        # Determine the correct country column name in the main df
        country_col_in_df = 'country_or_area' if 'country_or_area' in df_processed.columns else 'Country' # Use 'Country' as fallback
        if country_col_in_df in df_processed.columns:
            df_individual = df_processed[df_processed[country_col_in_df].isin(individual_countries)].copy()
            if not df_individual.empty:
                results_dfs.append(df_individual)
        else:
             # If neither standard column name is found
             st.warning(f"Could not find a suitable country column ('country_or_area' or 'Country') in main data for filtering individual countries.")


    # --- 3. Process Regional Aggregate Selections ---
    if region_aggregate_labels:
        required_value_col = 'value' # Column to aggregate
        grouping_cols = ['year', 'indicator_label']
        country_col_in_df = 'country_or_area' if 'country_or_area' in df_processed.columns else 'Country'
        for region_label in region_aggregate_labels:
            region_name = region_label.replace(" (Region Average)", "")
            countries_in_region = ref_data[ref_data['Region Name'] == region_name]['Country or Area'].unique().tolist()
            region_df = df_processed[df_processed[country_col_in_df].isin(countries_in_region)]
            if not region_df.empty and required_value_col in region_df.columns:
                # Group by year, indicator, and calculate mean
                agg_df = region_df.groupby(['year', 'indicator_label'], as_index=False)[required_value_col].mean()
                agg_df[country_col_in_df] = region_label
                results_dfs.append(agg_df)

    # --- 4. Combine Results ---
    if not results_dfs:
        # Return empty DataFrame with original columns if no results
        return pd.DataFrame(columns=df.columns)
    else:
        # Concatenate all results
        final_df = pd.concat(results_dfs, ignore_index=True, sort=False)
         # Ensure final DataFrame has columns in roughly the same order as original (optional)
        cols_ordered = [col for col in df.columns if col in final_df.columns] + \
                       [col for col in final_df.columns if col not in df.columns]
        return final_df[cols_ordered]

def find_indicators_in_data(df, indicator_patterns=None, fuzzy_match=False):
    """
    Finds indicators in the dataframe that match given patterns.

    Args:
        df (pd.DataFrame): The dataframe containing indicator data (needs 'indicator_label').
        indicator_patterns (list or dict, optional):
            - List of exact strings or regex patterns to match.
            - Dict where keys are categories and values are lists of patterns.
        fuzzy_match (bool): If True, use fuzzy matching (not implemented yet).

    Returns:
        list or dict: List of matching indicator labels found in the data,
                      or a dict mapping categories to lists of found indicators.
                      Returns empty list/dict if 'indicator_label' column is missing.
    """
    if 'indicator_label' not in df.columns:
        st.error("Column 'indicator_label' not found in DataFrame.")
        return [] if isinstance(indicator_patterns, list) or indicator_patterns is None else {}

    available_indicators = df['indicator_label'].dropna().unique()
    found_indicators = [] if isinstance(indicator_patterns, list) or indicator_patterns is None else {}

    if indicator_patterns is None:
        # If no patterns provided, return all unique indicators found
        return list(available_indicators)

    if fuzzy_match:
        st.warning("Fuzzy matching not yet implemented in find_indicators_in_data.")
        # Placeholder for future fuzzywuzzy or similar implementation

    # --- Pattern Matching Logic ---
    if isinstance(indicator_patterns, list):
        for pattern in indicator_patterns:
            # Simple check if pattern is exactly in the available indicators
            if pattern in available_indicators:
                found_indicators.append(pattern)
            else:
                # Optional: Add regex matching here if needed
                # import re
                # try:
                #     regex = re.compile(pattern, re.IGNORECASE) # Example: case-insensitive regex
                #     matches = [ind for ind in available_indicators if regex.search(ind)]
                #     found_indicators.extend(matches)
                # except re.error:
                #     st.warning(f"Invalid regex pattern skipped: {pattern}")
                pass # Keep it simple for now, exact match or direct list item check
        found_indicators = sorted(list(set(found_indicators))) # Unique and sorted

    elif isinstance(indicator_patterns, dict):
        for category, patterns in indicator_patterns.items():
            category_matches = []
            for pattern in patterns:
                 if pattern in available_indicators:
                     category_matches.append(pattern)
                 # Optional: Regex matching per category
            found_indicators[category] = sorted(list(set(category_matches)))
    else:
        st.error("Invalid 'indicator_patterns' format. Must be a list or dictionary.")
        return []

    return found_indicators

def add_country_coordinates(df, ref_df, country_col='country_or_area', iso_col='iso3'):
    """Adds latitude and longitude from a reference dataframe."""
    # Ensure reference dataframe has coordinates and necessary keys
    if ref_df is None or not all(c in ref_df.columns for c in ['iso3', 'Latitude', 'Longitude']):
        print("Reference dataframe missing required columns: iso3, Latitude, Longitude")
        return df

    if df is None:
        print("Input dataframe is None")
        return df

    # Prepare the mapping dictionary {iso3: (lat, lon)}
    coord_map = ref_df.set_index('iso3')[['Latitude', 'Longitude']].apply(tuple, axis=1).to_dict()

    # Function to apply mapping
    def get_coords(row):
        iso = row.get(iso_col)
        if pd.notna(iso) and iso in coord_map:
            return coord_map[iso]
        # Optional: Add fallback using country name standardization if iso fails?
        # name = standardize_country_name(row.get(country_col)) ... lookup in ref_df ...
        return (None, None)

    # Apply mapping to get coordinates
    coords = df.apply(get_coords, axis=1, result_type='expand')
    df['latitude'] = coords[0]
    df['longitude'] = coords[1]

    return df

def generate_placeholder_data(base_value=10.0, trend=0.1, noise=0.5, years=range(2010, 2024), countries=['Country A', 'Country B', 'Country C']):
    """Generates placeholder data for charts when real data is missing."""
    data = []
    for country in countries:
        value = base_value + random.uniform(-2, 2) # Start near base
        for year in years:
            value += trend * random.uniform(0.5, 1.5) + random.gauss(0, noise)
            data.append({'country_or_area': country, 'year': year, 'value': round(max(0, value), 2)}) # Ensure non-negative
    placeholder_df = pd.DataFrame(data)
    # Add iso3 code if possible (using simplified mapping here)
    country_to_iso = {name: f"P{i+1:03}" for i, name in enumerate(countries)} # Placeholder ISO
    placeholder_df['iso3'] = placeholder_df['country_or_area'].map(country_to_iso)
    return placeholder_df

# 3. UI component functions:

def create_country_selector(
    df,
    country_column='country',
    sidebar=True,
    max_selections=10,
    key=None,
    default_all=False
):
    """
    Create a multi-select widget for selecting countries

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing country data
    country_column : str, optional
        Column name in df containing country names
    sidebar : bool, optional
        If True, place the selector in the sidebar
    max_selections : int, optional
        Maximum number of countries that can be selected
    key : str, optional
        Unique key for the widget
    default_all : bool, optional
        If True, select "All Countries" by default

    Returns:
    --------
    list
        List of selected countries
    """
    # Get unique countries
    available_countries = sorted(df[country_column].unique().tolist())

    # Add "All Countries" option
    options = ["All Countries"] + available_countries

    # Default selection
    default = ["All Countries"] if default_all else []

    # Create the selector
    if sidebar:
        selected = st.sidebar.multiselect(
            "Select Countries",
            options=options,
            default=default,
            key=key or "country_selector"
        )
    else:
        selected = st.multiselect(
            "Select Countries",
            options=options,
            default=default,
            key=key or "country_selector"
        )

    # If "All Countries" is selected, return all countries
    if "All Countries" in selected:
        return available_countries

    # If max_selections is provided, enforce it
    if max_selections and len(selected) > max_selections:
        if sidebar:
            st.sidebar.warning(f"You can select at most {max_selections} countries")
        else:
            st.warning(f"You can select at most {max_selections} countries")
        selected = selected[:max_selections]

    return selected

def render_indicator_section(
    df,
    indicator_label=None,
    title=None,
    description=None,
    chart_type="bar",
    selected_countries=None,
    year_range=None,
    chart_options=None,
    fallback_function=None,
    show_data_table=True,
    container_key=None
):
    """
    Renders a standard section for displaying an indicator, including title,
    description, chart, and optional data table. Handles missing data gracefully.

    Args:
        df (pd.DataFrame): The main dataframe.
        indicator_label (str, optional): The specific indicator to display.
        title (str, optional): Title for the section. Defaults to indicator label.
        description (str, optional): Text description to display above the chart.
        chart_type (str): Type of chart ('bar', 'line', etc.).
        selected_countries (list, optional): List of countries to filter by.
        year_range (tuple, optional): (min_year, max_year) tuple for filtering.
        chart_options (dict, optional): Additional options for the chart function.
        fallback_function (callable, optional): Function returning a DataFrame if indicator_label fails.
        show_data_table (bool): Whether to show a data table below the chart.
        container_key (str, optional): Unique key for Streamlit elements.
    """
    # Use a unique container key if provided, otherwise generate one based on title/label
    if container_key is None:
        container_key = f"container_{title or indicator_label or random.randint(1000, 9999)}".replace(" ", "_")

    with st.container(): # Use container for better layout control
        # --- Title and Description ---
        section_title = title or indicator_label or "Indicator Analysis"
        st.subheader(section_title)

        if description:
            st.markdown(description)
        elif indicator_label:
             # Attempt to get metadata if no explicit description given
             meta_desc = get_indicator_metadata(indicator_label)
             if meta_desc != "No description available for this indicator.":
                 st.markdown(meta_desc)

        # --- Prepare Data ---
        data_to_plot = pd.DataFrame()
        indicator_found = False

        if indicator_label and indicator_label in df['indicator_label'].unique():
            data_to_plot = df[df['indicator_label'] == indicator_label].copy()
            indicator_found = True

        # If indicator not found or explicitly using fallback
        if not indicator_found and fallback_function:
            st.info(f"Indicator '{indicator_label}' not found directly, attempting to use fallback function.")
            try:
                data_to_plot = fallback_function()
                if data_to_plot is None or data_to_plot.empty:
                     st.warning("Fallback function did not return valid data.")
                     return # Stop processing this section
                st.info("Using data generated by fallback function.")
            except Exception as e:
                st.error(f"Error executing fallback function: {e}")
                return # Stop processing this section

        # If still no data after trying indicator and fallback
        if data_to_plot.empty:
            st.warning(f"No data available for indicator: '{indicator_label or 'N/A'}'")
            # Placeholder empty chart
            fig = go.Figure()
            fig.update_layout(title_text=f"{section_title} (No Data Available)", height=300)
            fig.add_annotation(text="No data found for this indicator and selection.",
                               xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            st.plotly_chart(fig, use_container_width=True)
            return

        # Apply filters (Year Range and Countries)
        if year_range and 'year' in data_to_plot.columns:
            min_year, max_year = year_range
            # Ensure year is numeric before filtering
            data_to_plot['year'] = pd.to_numeric(data_to_plot['year'], errors='coerce')
            data_to_plot = data_to_plot.dropna(subset=['year'])
            data_to_plot = data_to_plot[
                (data_to_plot['year'] >= min_year) & (data_to_plot['year'] <= max_year)
            ]

        if selected_countries and 'country_or_area' in data_to_plot.columns:
             # Ensure selected_countries isn't the "All" placeholder if used
             if "All African Countries" not in selected_countries:
                data_to_plot = data_to_plot[data_to_plot['country_or_area'].isin(selected_countries)]
        elif selected_countries and 'iso3' in data_to_plot.columns:
             # Fallback to iso3 if country_or_area missing but iso3 present
             if "All African Countries" not in selected_countries:
                 # Need a way to map selected country names back to iso3 codes maybe?
                 # This part might need adjustment based on how selected_countries are stored
                 # Assuming selected_countries are names, need ref_data here ideally.
                 # For now, we skip this filtering if direct country_or_area isn't available.
                 st.warning("Country filtering skipped: 'country_or_area' column missing, direct ISO3 mapping not implemented here.")


        # Check again if data remains after filtering
        if data_to_plot.empty:
            st.warning(f"No data available for '{indicator_label or 'N/A'}' after applying filters (Years: {year_range}, Countries: {len(selected_countries) if selected_countries else 'All'}).")
            # Placeholder chart
            fig = go.Figure()
            fig.update_layout(title_text=f"{section_title} (No Data for Selection)", height=300)
            fig.add_annotation(text="No data matches the current filter criteria.",
                               xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            st.plotly_chart(fig, use_container_width=True)
            return

        # --- Create Chart ---
        chart_options = chart_options or {}
        x_col = chart_options.get('x', 'year' if chart_type == 'line' else 'country_or_area')
        y_col = chart_options.get('y', 'value')
        color_col = chart_options.get('color') # Get color if specified

        # Ensure required columns exist for the chosen chart type
        required_chart_cols = [x_col, y_col]
        if color_col:
            required_chart_cols.append(color_col)
        if not all(col in data_to_plot.columns for col in required_chart_cols):
            st.error(f"Missing columns required for '{chart_type}' chart ({required_chart_cols}). Available: {list(data_to_plot.columns)}")
            return

        # Dynamically choose the plotting function based on chart_type
        plot_df = data_to_plot # Default to using the fully filtered data

        if chart_type == "line":
            fig = create_line_chart(
                plot_df, # Use plot_df
                x_column=x_col,
                y_column=y_col,
                color_column=color_col,
                title="", # Title is handled by st.subheader
                **chart_options.get('kwargs', {}) # Pass extra kwargs
            )
        elif chart_type == "bar":
             # For bar charts, only show latest year if x is country AND color is NOT specified
            if x_col == 'country_or_area' and 'year' in data_to_plot.columns and color_col is None:
                 try:
                     latest_data = data_to_plot.loc[data_to_plot.groupby('country_or_area')['year'].idxmax()]
                     plot_df = latest_data # Use only latest data in this specific case
                 except Exception as e:
                     st.warning(f"Could not determine latest year for bar chart: {e}. Using all available data.")
                     # Keep plot_df as data_to_plot if finding latest fails

            fig = create_bar_chart(
                plot_df, # Use potentially modified plot_df
                x_column=x_col,
                y_column=y_col,
                color_column=color_col, # Pass color_col for potential stacking
                title="",
                **chart_options.get('kwargs', {})
            )
        else:
            st.warning(f"Chart type '{chart_type}' not explicitly supported in render_indicator_section. Add specific logic or use a default.")
            # Default fallback or error
            fig = go.Figure().update_layout(title_text="Unsupported Chart Type", height=300)

        st.plotly_chart(fig, use_container_width=True)

        # --- Optional Data Table ---
        if show_data_table:
            with st.expander("View Data Table"):
                # Show relevant columns, potentially rename for clarity
                cols_to_show = ['country_or_area', 'year', 'value']
                display_df = data_to_plot[[col for col in cols_to_show if col in data_to_plot.columns]].copy()
                # Rename 'value' to the indicator label if possible
                if indicator_label and 'value' in display_df.columns:
                    display_df = display_df.rename(columns={'value': indicator_label})
                st.dataframe(display_df)

def render_indicator_map(
    df,
    indicator_label,
    title=None,
    description=None,
    reference_data=None,
    selected_countries=None,
    year_range=None,
    map_options=None,
    fallback_function=None,
    container_key=None
):
    """
    Renders a standard section for displaying an indicator as a choropleth map.

    Args:
        df (pd.DataFrame): The main dataframe.
        indicator_label (str): The specific indicator to display on the map.
        title (str, optional): Title for the section. Defaults to indicator label.
        description (str, optional): Text description to display above the map.
        reference_data (pd.DataFrame): Dataframe containing country ISO codes, names, etc. Required for mapping.
        selected_countries (list, optional): List of selected countries (might be used for context or highlighting in future).
        year_range (tuple, optional): (min_year, max_year) tuple. Usually, a single year is chosen for maps.
        map_options (dict, optional): Additional options for the create_choropleth_map function.
        fallback_function (callable, optional): Function returning a DataFrame if indicator_label fails.
        container_key (str, optional): Unique key for Streamlit elements.
    """
    if container_key is None:
        container_key = f"map_container_{title or indicator_label or random.randint(1000, 9999)}".replace(" ", "_")

    with st.container():
        # --- Title and Description ---
        section_title = title or indicator_label or "Indicator Map"
        st.subheader(section_title)

        if description:
            st.markdown(description)
        elif indicator_label:
             meta_desc = get_indicator_metadata(indicator_label)
             if meta_desc != "No description available for this indicator.":
                 st.markdown(meta_desc)

        if reference_data is None or reference_data.empty:
            st.error("Reference data with country codes is required to render a map.")
            return

        # --- Prepare Data for Map ---
        map_data = pd.DataFrame()
        indicator_found = False

        if indicator_label and indicator_label in df['indicator_label'].unique():
            map_data = df[df['indicator_label'] == indicator_label].copy()
            indicator_found = True

        # Fallback if necessary
        if not indicator_found and fallback_function:
            st.info(f"Indicator '{indicator_label}' not found, using fallback function.")
            try:
                map_data = fallback_function()
                if map_data is None or map_data.empty:
                     st.warning("Fallback function did not return valid map data.")
                     return
                st.info("Using map data generated by fallback function.")
            except Exception as e:
                st.error(f"Error executing fallback function for map: {e}")
                return

        # If still no data
        if map_data.empty:
            st.warning(f"No data available for map indicator: '{indicator_label or 'N/A'}'")
            fig = go.Figure().update_layout(title_text=f"{section_title} (No Data)", height=400, geo_scope='africa')
            fig.add_annotation(text="No data found.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            st.plotly_chart(fig, use_container_width=True)
            return

        # --- Year Selection for Map ---
        map_year = None
        if 'year' in map_data.columns:
            map_data['year'] = pd.to_numeric(map_data['year'], errors='coerce')
            available_years = sorted(map_data['year'].dropna().unique().astype(int), reverse=True)

            if not available_years:
                st.warning("No valid years found in the data for the map.")
                return

            # Use year_range to set default if provided and valid
            default_year = available_years[0] # Default to latest
            if year_range:
                range_min, range_max = year_range
                valid_years_in_range = [y for y in available_years if range_min <= y <= range_max]
                if valid_years_in_range:
                    default_year = max(valid_years_in_range) # Default to latest within range

            # Create a year selector - use a unique key
            year_selector_key = f"map_year_selector_{container_key}"
            map_year = st.selectbox(
                "Select Year for Map",
                options=available_years,
                index=available_years.index(default_year), # Set default index
                key=year_selector_key
            )
            # Filter data for the selected year
            map_data = map_data[map_data['year'] == map_year]

        else:
            st.warning("Year column not found. Map will show aggregated or first available data points.")
            # Decide on aggregation strategy if no year - e.g., mean, latest?
            # For simplicity, let's take the first value per country if no year
            if 'country_or_area' in map_data.columns:
                map_data = map_data.groupby('country_or_area').first().reset_index()
            elif 'iso3' in map_data.columns:
                 map_data = map_data.groupby('iso3').first().reset_index()


        # Check again if data remains after year selection/aggregation
        if map_data.empty:
            st.warning(f"No data available for '{indicator_label or 'N/A'}' for the year {map_year}.")
            fig = go.Figure().update_layout(title_text=f"{section_title} (No Data for {map_year})", height=400, geo_scope='africa')
            fig.add_annotation(text=f"No data found for {map_year}.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            st.plotly_chart(fig, use_container_width=True)
            return

        # --- Create and Display Map ---
        map_options = map_options or {}
        value_col = map_options.get('value_column', 'value')
        location_col = map_options.get('location_column', 'country_or_area') # Prefer name if available
        iso_ref_col = map_options.get('iso_column', 'iso3')

        # Ensure value and location columns are present
        if value_col not in map_data.columns:
             st.error(f"Value column '{value_col}' needed for map not found in data.")
             return
        if location_col not in map_data.columns and 'iso3' not in map_data.columns:
             st.error("Neither location column ('country_or_area') nor 'iso3' found for map.")
             return
        # If primary location col missing, try iso3
        if location_col not in map_data.columns and 'iso3' in map_data.columns:
            location_col = 'iso3'
            # Adjust location mode if using ISO directly
            map_options['locationmode'] = 'ISO-3'


        fig = create_choropleth_map(
            data=map_data,
            location_column=location_col,
            value_column=value_col,
            title="", # Title handled by subheader
            reference_data=reference_data,
            iso_column=iso_ref_col,
            # Pass other options like color scale, range etc.
            color_continuous_scale=map_options.get('color_continuous_scale', "Blues"),
            range_color=map_options.get('range_color', None),
            height=map_options.get('height', 500),
            width=map_options.get('width', None)
        )

        # Display the chart if data is available
        if fig:
            st.plotly_chart(fig, use_container_width=True, key=f"{container_key}_plotly") # Added unique key

        # Optional: Data table display
        show_map_data = map_options.get('show_data_table', True) # Default to True
        if show_map_data:
            with st.expander(f"View Data for {map_year or 'Selected Data'}"):
                cols_to_show = [location_col, value_col, 'year'] # Add year if it exists
                display_map_df = map_data[[col for col in cols_to_show if col in map_data.columns]].copy()
                if indicator_label and value_col in display_map_df.columns:
                     display_map_df = display_map_df.rename(columns={value_col: indicator_label})
                st.dataframe(display_map_df)

def setup_page_config(title="Nexus Dashboard", icon="📊", layout="wide"):
    """Sets the Streamlit page configuration and applies custom CSS."""
    st.set_page_config(page_title=title, page_icon=icon, layout=layout)

    # Custom CSS for styling - consider moving to a separate CSS file later
    css = """
    <style>
        /* General styling */
        body {
            font-family: 'Arial', sans-serif; /* Example: Change default font */
        }
        /* Sidebar styling */
        .css-1d391kg { /* Sidebar background */
            background-color: #f0f2f6;
        }
        /* Main content area */
        .main .block-container {
            padding-top: 2rem; /* Add some padding at the top */
            padding-bottom: 2rem;
        }
        /* Titles and headers */
        h1, h2, h3 {
            color: #004080; /* Example: Dark blue color for headers */
        }
        /* Styling for selectbox/multiselect */
        .stSelectbox>div[data-baseweb="select"]>div {
            background-color: #ffffff;
        }
         /* Make expander headers slightly bolder or different color */
        .streamlit-expanderHeader {
            font-weight: bold;
            /* background-color: #e8e8e8; */ /* Optional background */
        }

        /* Dataframe styling */
        .stDataFrame {
            border: 1px solid #e0e0e0;
            border-radius: 5px;
        }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def setup_sidebar_filters(ref_data, df=None, key_prefix=""):
    """
    Sets up sidebar filters for region, country, and year range selection.

    Args:
        ref_data (pd.DataFrame): Reference data containing region and country information.
        df (pd.DataFrame, optional): Main data for year range determination.
        key_prefix (str): Prefix for widget keys to avoid conflicts.

    Returns:
        dict: Dictionary containing filter selections:
              {'selected_region': str, 'selected_countries': list, 'year_range': tuple}.
              'selected_countries' can contain country names and/or regional aggregate labels.
    """
    st.sidebar.header("Filters")

    # --- Region Selection ---
    regions = sorted(ref_data['Region Name'].dropna().unique())
    selected_region = st.sidebar.selectbox(
        "Select Region",
        regions,
        key=f"{key_prefix}_region_select"
    )

    # --- Country Selection (with Regional Aggregate) ---
    # Get all countries in the selected region
    countries_in_region = sorted(ref_data[ref_data['Region Name'] == selected_region]['Country or Area'].dropna().unique())
    # Add region average if it exists in the data
    region_average_label = f"{selected_region} (Region Average)"
    region_countries_with_avg = countries_in_region.copy()
    region_countries_with_avg.append(region_average_label)

    selected_countries = st.sidebar.multiselect(
        "Select Countries / Regional Average",
        options=region_countries_with_avg,
        default=region_countries_with_avg,  # All selected by default
        key=f"{key_prefix}_country_multiselect"
    )

    # --- Year Range Selection ---
    min_year, max_year = 1960, 2024 # Default fallback range
    if df is not None and 'year' in df.columns and not df['year'].isnull().all():
        min_year = int(df['year'].min())
        max_year = int(df['year'].max())

    # Ensure min_year is less than max_year
    if min_year >= max_year:
         min_year_slider = max_year - 1
         max_year_slider = max_year
    else:
         min_year_slider = min_year
         max_year_slider = max_year

    start_year, end_year = st.sidebar.slider(
        "Select Year Range",
        min_value=min_year_slider,
        max_value=max_year_slider,
        value=(min_year_slider, max_year_slider), # Default to full range initially
        key=f"{key_prefix}_year_slider"
    )

    return {
        "selected_region": selected_region,
        "selected_countries": selected_countries,
        "year_range": (start_year, end_year)
    }

def create_data_explorer(df, key_prefix=""):
    """
    Creates an expandable 'Data Exploration' section.
    Shows available indicators and allows viewing sample data for a selected indicator.

    Args:
        df (pd.DataFrame): The DataFrame to explore (needs 'indicator_label', 'year', 'value', 'country_or_area').
        key_prefix (str): Optional prefix for widget keys.

    Returns:
        None: Renders the section directly using Streamlit elements.
    """
    with st.expander("Data Exploration", expanded=False):

        if df is None or df.empty:
            st.info("No data loaded to explore.")
            return

        if 'indicator_label' not in df.columns:
            st.warning("Cannot display indicators: 'indicator_label' column missing.")
            st.dataframe(df.head()) # Show head of what data IS available
            return

        st.markdown("**Available Indicators in Filtered Data**")
        unique_indicators = sorted(df['indicator_label'].dropna().unique())

        if not unique_indicators:
            st.info("No unique indicators found in the currently filtered data.")
            return

        # Display count and list
        st.write(f"Found {len(unique_indicators)} unique indicators.")
        # Use columns for better layout if many indicators
        col1, col2 = st.columns(2, gap=None)
        split_point = (len(unique_indicators) + 1) // 2
        with col1:
            st.dataframe(pd.DataFrame({'Indicator': unique_indicators[:split_point]}), hide_index=True)
        with col2:
             if len(unique_indicators) > split_point:
                 st.dataframe(pd.DataFrame({'Indicator': unique_indicators[split_point:]}), hide_index=True)

        st.markdown("**View Sample Data for an Indicator**")
        select_key = f"{key_prefix}_data_explorer_select"
        selected_indicator = st.selectbox(
            "Choose an indicator to see its structure:",
            unique_indicators,
            key=select_key,
            index=0 # Default to the first indicator
        )

        if selected_indicator:
            sample_df = df[df['indicator_label'] == selected_indicator].copy()
            st.write(f"Sample data for: **{selected_indicator}**")

            # Show relevant columns by default
            cols_to_show = ['country_or_area', 'iso3', 'year', 'value', 'unit']
            sample_df_display = sample_df[[col for col in cols_to_show if col in sample_df.columns]]

            st.dataframe(sample_df_display.head()) # Show the first few rows
            st.caption(f"Showing top 5 rows. Total rows for this indicator (in current filter): {len(sample_df)}")

def create_topic_page(
    page_title,
    overview_text,
    main_dataframe,
    # Define sections more explicitly
    map_section: Optional[Dict[str, Any]] = None, # e.g., {'indicator': 'PEFA PI-1', 'title': 'PEFA Scores', ...}
    tab_sections: Optional[Dict[str, List[Dict[str, Any]]]] = None, # e.g., {'Tab 1 Title': [{'indicator': '...', 'chart_type': 'bar'}, ...]}
    data_explorer: bool = True, # Whether to include the data explorer section
    reference_data_path=None,
    page_key="topic" # Base key for widgets on this page
):
    """
    Creates a standard topic page structure with optional map, tabs, and data explorer.

    Args:
        page_title (str): The title of the page.
        overview_text (str): Introductory markdown text for the page.
        main_dataframe (pd.DataFrame): The primary data for this topic.
        map_section (dict, optional): Configuration for the indicator map section.
            Requires keys like 'indicator_label', 'title'. Optional: 'description', 'map_options'.
        tab_sections (dict, optional): Configuration for tabbed indicator sections.
            Keys are tab titles, values are lists of indicator section configs.
            Each indicator config requires 'indicator_label' or 'fallback_function'.
            Optional keys: 'title', 'description', 'chart_type', 'chart_options', 'show_data_table'.
        data_explorer (bool): If True, include the standard data explorer section.
        reference_data_path (str, optional): Path to the country reference CSV.
        page_key (str): Unique prefix for widgets on this page.
    """
    # --- 1. Setup Page and Load Reference Data ---
    setup_page_config(title=page_title)
    ref_data = load_country_reference_data(reference_data_path)
    if ref_data.empty:
        st.error("Failed to load essential country reference data. Page cannot render correctly.")
        return # Stop execution if reference data failed

    # --- 2. Setup Sidebar Filters ---
    filters = setup_sidebar_filters(ref_data, main_dataframe, key_prefix=page_key)

    # --- 3. Filter Main Data Based on Selections ---
    df_filtered = filter_dataframe_by_selections(main_dataframe, filters, ref_data)

    # --- 4. Page Title and Overview ---
    st.title(page_title)
    st.markdown(overview_text)

    # --- 5. Render Indicator Map Section (if configured) ---
    if map_section and isinstance(map_section, dict):
        indicator = map_section.get('indicator_label')
        if indicator:
            render_indicator_map(
                df=df_filtered,
                indicator_label=indicator,
                title=map_section.get('title', indicator),
                description=map_section.get('description'),
                reference_data=ref_data, # Pass loaded ref_data
                year_range=filters.get('year_range'), # Pass year range for year selection
                map_options=map_section.get('map_options', {}),
                fallback_function=map_section.get('fallback_function'),
                container_key=f"{page_key}_map_{indicator.replace(' ', '_')[:10]}" # Generate key
            )
        else:
            st.warning("Map section configured but 'indicator_label' is missing.")

    # --- 6. Render Tabbed Indicator Sections (if configured) ---
    if tab_sections and isinstance(tab_sections, dict):
        tab_titles = list(tab_sections.keys())
        tabs = st.tabs(tab_titles)

        for i, tab_title in enumerate(tab_titles):
            with tabs[i]:
                indicator_configs = tab_sections[tab_title]
                if not isinstance(indicator_configs, list):
                    st.error(f"Configuration for tab '{tab_title}' should be a list of indicator dictionaries.")
                    continue

                for j, config in enumerate(indicator_configs):
                    if not isinstance(config, dict):
                         st.error(f"Invalid item in configuration list for tab '{tab_title}'. Expected a dictionary.")
                         continue

                    indicator_label = config.get('indicator_label')
                    fallback_func = config.get('fallback_function')

                    if not indicator_label and not fallback_func:
                        st.warning(f"Skipping item {j+1} in tab '{tab_title}': Must provide 'indicator_label' or 'fallback_function'.")
                        continue

                    # Generate a unique key for each section within the tab
                    base_key = indicator_label or f"fallback_{j}"
                    section_key = f"{page_key}_tab{i}_{base_key.replace(' ', '_')[:15]}"

                    render_indicator_section(
                        df=df_filtered,
                        indicator_label=indicator_label,
                        title=config.get('title', indicator_label), # Default title to label
                        description=config.get('description'),
                        chart_type=config.get('chart_type', 'bar'), # Default chart type
                        selected_countries=filters.get('selected_countries'), # Pass selected countries
                        year_range=filters.get('year_range'), # Pass selected year range
                        chart_options=config.get('chart_options', {}),
                        fallback_function=fallback_func,
                        show_data_table=config.get('show_data_table', True), # Default to show table
                        container_key=section_key
                    )

    # --- 7. Render Data Explorer (if enabled) ---
    if data_explorer:
        st.divider() # Add a visual separator
        create_data_explorer(df_filtered, key_prefix=page_key)

    # --- Optional: Debug Info ---
    # with st.expander("Debug Info"):
    #     st.write("Filters:", filters)
    #     st.write("Filtered Data Shape:", df_filtered.shape)
    #     st.write("Reference Data Columns:", ref_data.columns.tolist())

def standardize_country_name(country: str) -> str:
    """
    Standardize country names to improve matching with coordinates dictionary.
    Removes common prefixes/suffixes and standardizes known variations.

    Args:
        country: Country name to standardize

    Returns:
        Standardized country name
    """
    if pd.isna(country):
        return ""
    
    # Convert to string and lowercase
    name = str(country).lower().strip()
    
    # Remove common prefixes/suffixes
    prefixes = ["republic of ", "democratic republic of ", "kingdom of ", "state of ", "the "]
    for prefix in prefixes:
        if name.startswith(prefix):
            name = name[len(prefix):]
    
    # Handle specific country name variations
    name_mapping = {
        "united states of america": "united states",
        "usa": "united states",
        "u.s.a.": "united states",
        "u.s.": "united states",
        "uk": "united kingdom",
        "great britain": "united kingdom",
        "congo, dem. rep.": "democratic republic of the congo",
        "congo, republic of": "congo",
        "drc": "democratic republic of the congo",
        "ivory coast": "côte d'ivoire",
        "ivory coast": "cote d'ivoire",
        "côte d'ivoire": "cote d'ivoire",
        "tanzania, united republic of": "tanzania",
        "congo-brazzaville": "congo",
        "congo-kinshasa": "democratic republic of the congo",
        "uae": "united arab emirates",
        "cabo verde": "cape verde",
        "timor leste": "timor-leste"
    }
    
    return name_mapping.get(name, name)

def get_indicator_metadata(indicator_label):
    """
    Retrieves metadata for a given indicator label.
    Returns a default description if no specific metadata is found.
    """
    # Example metadata - replace with actual source if available
    metadata = {
        "Expenditure outturn compared to original approved budget": "Measures the difference between actual primary expenditure and the originally approved budget.",
        "PEFA PI-1: Aggregate expenditure out-turn": "Indicator assessing the extent to which aggregate budget expenditure outturn reflects the amount originally approved, as defined in government budget documentation and fiscal reports.",
        "PEFA PI-2: Expenditure composition out-turn": "Indicator assessing the extent to which the variance in expenditure composition during the last three fiscal years departed from the original budget.",
        # Add more descriptions here
    }
    return metadata.get(indicator_label, "No description available for this indicator.")

def render_data_availability_heatmap(
    df,
    indicator_label,
    country_col='country_or_area',
    year_col='year',
    value_col='value',
    title="Data Availability Heatmap",
    container_key=None,
    all_countries=None
):
    """
    Displays a heatmap showing which countries and years have data for a given indicator.
    Presence = 1, Absence = 0. If all_countries is provided, ensures all are shown.
    """
    import streamlit as st
    import plotly.express as px
    # Filter for the indicator
    df_ind = df[df['indicator_label'] == indicator_label].copy()
    # Pivot: countries as rows, years as columns, 1 if data exists
    if not df_ind.empty:
        df_ind['has_data'] = 1
        heatmap_df = df_ind.pivot_table(
            index=country_col,
            columns=year_col,
            values='has_data',
            aggfunc='max',
            fill_value=0
        )
    else:
        # If no data at all, create an empty DataFrame with no columns
        heatmap_df = pd.DataFrame()
    # If all_countries is provided, reindex to show all (fill missing with 0)
    if all_countries is not None:
        heatmap_df = heatmap_df.reindex(all_countries, fill_value=0)
    # If still empty, show info
    if heatmap_df.empty or heatmap_df.shape[1] == 0:
        st.info(f"No data available for indicator: {indicator_label}")
        return
    # Sort years for readability
    heatmap_df = heatmap_df.sort_index(axis=1)
    # Plotly heatmap
    fig = px.imshow(
        heatmap_df,
        labels=dict(x="Year", y="Country", color="Data Present"),
        color_continuous_scale=[(0, "#eee"), (1, "#1f77b4")],
        aspect="auto",
        title=title
    )
    fig.update_xaxes(side="top")
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True, key=f"{container_key}_heatmap" if container_key else None)

def load_main_data(file_path="data/nexus.parquet"):
    """
    Loads the main dataset from a parquet file, with basic validation and error handling.
    Returns a DataFrame with columns: indicator_label, country_or_area, year, value, iso3 (if available).
    """
    @st.cache_data
    def _load(file_path):
        try:
            df = pd.read_parquet(file_path)
            required_cols = ['indicator_label', 'country_or_area', 'year', 'value', 'iso3']
            if not all(col in df.columns for col in required_cols):
                st.warning(f"Warning: Main data might be missing some expected columns ({required_cols}).")
            return df
        except FileNotFoundError:
            st.error(f"Error: The main data file was not found at {file_path}")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"An error occurred while loading the main data: {e}")
            return pd.DataFrame()
    return _load(file_path)