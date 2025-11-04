"""
Reusable layout functions for topic pages.
Provides standardized structure for all topic dashboard pages.
"""
import streamlit as st
from typing import Dict, List, Optional, Callable, Any
import pandas as pd


def render_topic_header(title: str, description: str):
    """
    Render the topic page header with title and description.
    
    Args:
        title: Topic title (e.g., "Topic 4.1: Public Expenditures")
        description: Brief description of the topic
    """
    st.markdown(f"""
    <div class="topic-header-container">
        <h1 class="topic-header">{title}</h1>
        <p class="topic-intro">{description}</p>
    </div>
    """, unsafe_allow_html=True)


def render_indicator_section(
    indicator_data: Dict[str, Any],
    render_function: Callable,
    container_key: Optional[str] = None
):
    """
    Render a section with indicators in a column layout.
    
    Args:
        indicator_data: Dictionary with indicator configs
            Format: {
                "indicator_name": {
                    "title": "Indicator Title",
                    "description": "Description",
                    "indicator_label": "Indicator Label",
                    "chart_type": "bar",
                    "chart_options": {...},
                    "map_options": {...}
                }
            }
        render_function: Function to render each indicator (e.g., uv.render_indicator_section)
        container_key: Optional key prefix for containers
    """
    st.markdown("<h2 class='section-header'>Indicator Overview</h2>", unsafe_allow_html=True)
    
    num_indicators = len(indicator_data)
    if num_indicators == 1:
        cols = [st.container()]
    elif num_indicators == 2:
        cols = st.columns(2, gap="large")
    elif num_indicators == 3:
        cols = st.columns(3, gap="medium")
    else:
        cols = st.columns(2, gap="large")
    
    for idx, (indicator_key, indicator_config) in enumerate(indicator_data.items()):
        with cols[idx % len(cols)]:
            with st.container():
                render_function(
                    df=indicator_config.get("df"),
                    indicator_label=indicator_config.get("indicator_label"),
                    title=indicator_config.get("title", indicator_key),
                    description=indicator_config.get("description", ""),
                    chart_type=indicator_config.get("chart_type", "bar"),
                    selected_countries=indicator_config.get("selected_countries"),
                    year_range=indicator_config.get("year_range"),
                    chart_options=indicator_config.get("chart_options", {}),
                    show_data_table=indicator_config.get("show_data_table", True),
                    container_key=f"{container_key}_{indicator_key}" if container_key else None
                )


def render_tabs_section(
    tabs_data: Dict[str, Dict[str, Any]],
    render_indicator_func: Callable,
    render_map_func: Optional[Callable] = None
):
    """
    Render a tabs section with subtopic indicators.
    
    Args:
        tabs_data: Dictionary with tab configurations
            Format: {
                "tab_name": {
                    "df": DataFrame,
                    "indicator_label": "...",
                    "title": "...",
                    "description": "...",
                    "chart_type": "...",
                    "chart_options": {...},
                    "map_options": {...},
                    "reference_data": DataFrame,
                    "learn_more": {
                        "definition": "...",
                        "relevance": "...",
                        "proxy": "..."
                    }
                }
            }
        render_indicator_func: Function to render indicators (e.g., uv.render_indicator_section)
        render_map_func: Optional function to render maps (e.g., uv.render_indicator_map)
    """
    tab_names = list(tabs_data.keys())
    tabs = st.tabs(tab_names)
    
    for tab, tab_config in zip(tabs, tabs_data.values()):
        with tab:
            # Render main indicator
            render_indicator_func(
                df=tab_config.get("df"),
                indicator_label=tab_config.get("indicator_label"),
                title=tab_config.get("title", ""),
                description=tab_config.get("description", ""),
                chart_type=tab_config.get("chart_type", "bar"),
                selected_countries=tab_config.get("selected_countries"),
                year_range=tab_config.get("year_range"),
                chart_options=tab_config.get("chart_options", {}),
                show_data_table=tab_config.get("show_data_table", True),
                container_key=tab_config.get("container_key")
            )
            
            # Learn More expander if provided
            if tab_config.get("learn_more"):
                learn_more = tab_config["learn_more"]
                with st.expander("Learn more about this indicator"):
                    tab_def, tab_rel, tab_proxy = st.tabs(["Definition", "Relevance", "Proxy Justification"])
                    with tab_def:
                        st.markdown(learn_more.get("definition", ""))
                    with tab_rel:
                        st.markdown(learn_more.get("relevance", ""))
                    with tab_proxy:
                        st.markdown(learn_more.get("proxy", ""))
            
            st.divider()
            
            # Render map if map configuration and render function provided
            if tab_config.get("map_options") and tab_config.get("reference_data") is not None and render_map_func:
                render_map_func(
                    df=tab_config.get("df"),
                    indicator_label=tab_config.get("indicator_label"),
                    title="",
                    description="Geographical distribution of latest scores.",
                    reference_data=tab_config.get("reference_data"),
                    year_range=tab_config.get("year_range"),
                    map_options=tab_config.get("map_options"),
                    container_key=f"{tab_config.get('container_key', '')}_map" if tab_config.get("container_key") else None
                )
                st.divider()


def render_geographic_section(
    map_data: pd.DataFrame,
    summary_data: Optional[pd.DataFrame] = None,
    map_title: str = "Regional Data Overview",
    map_width_ratio: int = 3,
    table_width_ratio: int = 2
):
    """
    Render geographic map and summary data side by side.
    
    Args:
        map_data: DataFrame for map visualization
        summary_data: Optional DataFrame for summary table
        map_title: Title for the section
        map_width_ratio: Width ratio for map column
        table_width_ratio: Width ratio for table column
    """
    st.markdown(f"<h2 class='section-header'>{map_title}</h2>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([map_width_ratio, table_width_ratio])
        
        with col1:
            if not map_data.empty:
                st.map(map_data)
            else:
                st.info("No geographic data available for visualization.")
        
        with col2:
            if summary_data is not None and not summary_data.empty:
                st.dataframe(summary_data, use_container_width=True)
            else:
                st.info("No summary data available.")


def render_context_section(
    insights: str,
    data_source: str,
    metadata: Optional[str] = None
):
    """
    Render context section with insights and data source in two columns.
    
    Args:
        insights: Key insights text
        data_source: Data source information
        metadata: Optional metadata text
    """
    st.markdown("<h2 class='section-header'>Understanding the Patterns</h2>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Key Insights:** {insights}")
        
        with col2:
            st.markdown(f"**Data Source:** {data_source}")
            if metadata:
                st.markdown(f"**Metadata:** {metadata}")


def render_data_gaps_section(
    df: pd.DataFrame,
    indicators_dict: Dict[str, str],
    title: str = "Understand the data gap in Africa for this topic",
    container_key: Optional[str] = None,
    render_function: Optional[Callable] = None
):
    """
    Render data gaps section with expandable heatmap.
    
    Args:
        df: DataFrame for data availability analysis
        indicators_dict: Dictionary mapping indicator names to indicator labels
        title: Title for the expander
        container_key: Optional key prefix for containers
        render_function: Optional function to render data availability (e.g., uv.render_data_availability_heatmap)
    """
    st.divider()
    
    if render_function:
        with st.expander(title):
            selected_indicator = st.selectbox(
                "Select indicator to view data availability:",
                options=list(indicators_dict.keys()),
                key=f"{container_key}_gap_indicator_select" if container_key else "gap_indicator_select"
            )
            render_function(
                df=df,
                indicator_label=indicators_dict[selected_indicator],
                title=f"Data Availability for {selected_indicator} (Africa)",
                container_key=f"{container_key}_gap" if container_key else "gap"
            )
    else:
        st.markdown(f"""
        <div class='data-gap-box'>
            <h3>Data Gaps and Limitations</h3>
            <p>{title}</p>
        </div>
        """, unsafe_allow_html=True)


def render_topic_page(
    title: str,
    description: str,
    tabs_data: Optional[Dict[str, Dict[str, Any]]] = None,
    indicators_data: Optional[Dict[str, Dict[str, Any]]] = None,
    render_indicator_func: Optional[Callable] = None,
    geographic_data: Optional[pd.DataFrame] = None,
    summary_data: Optional[pd.DataFrame] = None,
    insights: Optional[str] = None,
    data_source: Optional[str] = None,
    data_gaps: Optional[Dict[str, Any]] = None
):
    """
    Master function to render a complete topic page with standardized layout.
    
    Args:
        title: Topic title
        description: Topic description
        tabs_data: Optional dictionary for tabs section
        indicators_data: Optional dictionary for indicators section
        render_indicator_func: Function to render indicators
        geographic_data: Optional DataFrame for map
        summary_data: Optional DataFrame for summary table
        insights: Optional insights text
        data_source: Optional data source text
        data_gaps: Optional dictionary for data gaps section
            Format: {
                "df": DataFrame,
                "indicators_dict": Dict[str, str],
                "render_function": Callable
            }
    """
    # Header
    render_topic_header(title, description)
    
    # Tabs section (if provided)
    if tabs_data and render_indicator_func:
        render_tabs_section(tabs_data, render_indicator_func)
    
    # Indicators section (if provided, alternative to tabs)
    elif indicators_data and render_indicator_func:
        render_indicator_section(indicators_data, render_indicator_func)
    
    # Geographic section (if provided)
    if geographic_data is not None:
        render_geographic_section(geographic_data, summary_data)
    
    # Context section (if provided)
    if insights and data_source:
        render_context_section(insights, data_source)
    
    # Data gaps section (if provided)
    if data_gaps:
        render_data_gaps_section(
            df=data_gaps.get("df"),
            indicators_dict=data_gaps.get("indicators_dict", {}),
            title=data_gaps.get("title", "Understand the data gap in Africa for this topic"),
            container_key=data_gaps.get("container_key"),
            render_function=data_gaps.get("render_function")
        )

