import streamlit as st
import pandas as pd
import sys
from pathlib import Path
import io # For data exploration info capture

# Add parent directory to path for module imports
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import the universal visualization module
import universal_viz as uv

# --- Configuration ---
# MAPPING_FILE_PATH = "analysis plan/Dashboard viz plan.csv" # Removed - No longer using mapping file
MAIN_DATA_FILE = "data/nexus.parquet"
# Column indices are no longer needed as we don't use the mapping file
# CONCEPTUAL_INDICATOR_COL_IDX = 6
# DATA_LABEL_COL_IDX = 18
# VIZ_GOAL_COL_IDX = 7

# --- Data Loading ---
@st.cache_data
def load_main_data(file_path):
    """Loads the main dataset from a parquet file."""
    try:
        df = pd.read_parquet(file_path)
        # Ensure required columns exist
        required_cols = ['indicator_label', 'country_or_area', 'year', 'value']
        if not all(col in df.columns for col in required_cols):
             missing = [col for col in required_cols if col not in df.columns]
             st.error(f"Error: Main data file ({file_path}) is missing required columns: {missing}")
             return pd.DataFrame()
        return df
    except FileNotFoundError:
        st.error(f"Error: Main data file not found at {file_path}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading main data from {file_path}: {e}")
        return pd.DataFrame()

# Removed load_indicator_mapping function as it's no longer needed
# @st.cache_data
# def load_indicator_mapping(file_path): ...

# Removed get_data_label function as it's no longer needed
# def get_data_label(conceptual_id, mapping_df): ...

# --- Load All Data ---
st.title("🧪 Indicator Explorer")
st.markdown("Select an indicator label directly from the dataset and explore its data.")
# Removed warning about mapping file
# st.warning(f"Ensure your mapping file (...)")

df_main = load_main_data(MAIN_DATA_FILE)
# st.write("All indicator labels in nexus.parquet:", df_main['indicator_label'].unique())
ref_data = uv.load_country_reference_data() # For filters

# Stop if essential data is missing
if df_main.empty or ref_data.empty:
    # Updated error message
    st.error("Failed to load main data or reference data. Cannot proceed.")
    st.stop()

# === Indicator Selection (Directly from Data) ===
st.subheader("1. Select Data Indicator Label")
# Get unique indicator labels from the main dataframe
indicator_labels_list = sorted(df_main['indicator_label'].dropna().unique())

if not indicator_labels_list:
    st.error(f"No indicator labels found in the 'indicator_label' column of {MAIN_DATA_FILE}. Cannot proceed.")
    st.stop()

# Add a text input for keyword search
search_term = st.text_input("Search Indicator Label by Keywords:", "", help="Enter keywords separated by space (e.g., 'tax gdp')")

# Filter the list based on the search term
filtered_labels = indicator_labels_list
if search_term:
    keywords = search_term.lower().split()
    filtered_labels = [
        label for label in indicator_labels_list
        if all(keyword in label.lower() for keyword in keywords)
    ]

if not filtered_labels:
    st.warning(f"No indicators found matching: '{search_term}'")
    # Display the selectbox anyway, but it will be empty or show a message
    # Or optionally st.stop() here if you prefer
    # selected_indicator_label = None # Ensure it's handled later
    pass # Let the selectbox handle the empty list

# Determine default index safely
default_index = 0
if not filtered_labels:
    default_index = None # Or handle as appropriate if list is empty

selected_indicator_label = st.selectbox(
    "Select Indicator Label from Filtered List:",
    options=filtered_labels,
    index=default_index, # Use safe default index
    help="Choose the exact indicator label you want to explore from the filtered list.",
    # Add a message if the list is empty due to filtering
    format_func=lambda x: x if filtered_labels else "No matching indicators found"
)

# Proceed only if an indicator is actually selected
if selected_indicator_label:
    st.success(f"**Selected Indicator Label:** `{selected_indicator_label}`")

    # Filter main data to only this indicator initially
    data_for_indicator = df_main[df_main['indicator_label'] == selected_indicator_label].copy()
    st.info(f"Found {len(data_for_indicator)} rows for this indicator before applying filters.")
else:
    # Handle case where no indicator is selected (e.g., due to empty filtered list)
    st.info("Please select an indicator label to proceed.")
    data_for_indicator = pd.DataFrame() # Ensure it's an empty DataFrame
    # Optionally st.stop() if you want to halt execution until selection

st.divider() # Use divider instead of subheader for visual separation

# === Sidebar Filters ===
st.sidebar.header("🔍 Filters for Selected Indicator")
if not data_for_indicator.empty:
    # Pass the filtered data for the selected indicator to get relevant year range etc.
    filters = uv.setup_sidebar_filters(ref_data, data_for_indicator, key_prefix="explorer")
    # Apply filters
    df_filtered = uv.filter_dataframe_by_selections(data_for_indicator, filters, ref_data)
    st.sidebar.success(f"Filtered Data Rows: {len(df_filtered)}")
else:
    st.sidebar.warning("No data found for the selected indicator label.")
    # Create dummy filters dict and empty df if no data
    filters = {'selected_region': None, 'selected_countries': [], 'year_range': (None, None)}
    df_filtered = pd.DataFrame()

# === Data Exploration Section ===
st.subheader("2. Explore Filtered Data") # Renumbered section
if not df_filtered.empty:
    with st.expander("View Data Details", expanded=True):
        st.markdown("**Filtered Data Head:**")
        st.dataframe(df_filtered.head())

        st.markdown("**Data Info:**")
        buffer = io.StringIO()
        df_filtered.info(buf=buffer)
        st.text(buffer.getvalue())

        st.markdown("**Value Summary Statistics:**")
        if 'value' in df_filtered.columns and pd.api.types.is_numeric_dtype(df_filtered['value']):
            st.dataframe(df_filtered['value'].describe())
        elif 'value' in df_filtered.columns:
             st.text(f"'value' column exists but is not numeric (type: {df_filtered['value'].dtype}). Cannot compute stats.")
        else:
            st.text("'value' column not found.")

        col1, col2 = st.columns(2, gap=None)
        with col1:
            st.markdown("**Unique Countries:**")
            if 'country_or_area' in df_filtered.columns:
                st.dataframe(sorted(df_filtered['country_or_area'].unique()), width=300, height=200) # Added sorting and height
            else:
                 st.text("'country_or_area' column not found.")
        with col2:
            st.markdown("**Unique Years:**")
            if 'year' in df_filtered.columns:
                st.dataframe(sorted(df_filtered['year'].unique()), width=300, height=200) # Added sorting and height
            else:
                 st.text("'year' column not found.")
else:
    st.warning("No data available to explore after filtering.")

# === Optional Visualization ===
st.divider()
st.subheader("3. Visualize Filtered Data (Optional)") # Renumbered section
if not df_filtered.empty:
    chart_type = st.radio("Select Chart Type:", ["line", "bar"], index=0, key="explorer_chart_type", horizontal=True) # Added horizontal layout
    st.info(f"Rendering {chart_type} chart for: {selected_indicator_label}")
    # Ensure 'value' column is numeric for visualization
    if 'value' in df_filtered.columns and pd.api.types.is_numeric_dtype(df_filtered['value']):
        uv.render_indicator_section(
            df=df_filtered,
            indicator_label=selected_indicator_label, # Use the directly selected label
            title="", # Keep title empty as context is above
            chart_type=chart_type,
            selected_countries=filters.get('selected_countries'),
            year_range=filters.get('year_range'),
            # Adjust chart options based on type (consider if year/country is best axis)
            chart_options={'x': 'year', 'y': 'value', 'color': 'country_or_area'} if chart_type == 'line' else {'x': 'country_or_area', 'y': 'value', 'color': 'year'},
            show_data_table=False, # Keep explorer focused
            container_key="explorer_chart" # Use a unique key
        )
    elif 'value' in df_filtered.columns:
        st.warning(f"Cannot visualize: 'value' column is not numeric (type: {df_filtered['value'].dtype}).")
    else:
        st.warning("Cannot visualize: 'value' column not found.")

else:
    st.warning("No data available to visualize.")

# === Download Button ===
st.divider()
st.subheader("4. Download Filtered Data") # Renumbered section
if not df_filtered.empty:
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        # Generate filename from the selected indicator label
        file_name=f"indicator_data_{selected_indicator_label[:30].replace(' ', '_').replace('/', '_')}.csv",
        mime='text/csv',
        key='explorer_download_csv'
    )
else:
    st.info("No data to download.")
