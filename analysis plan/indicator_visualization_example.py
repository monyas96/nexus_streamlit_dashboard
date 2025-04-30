import streamlit as st
import pandas as pd
import numpy as np
from postprocessed import visualize_indicator

st.set_page_config(
    page_title="Indicator Visualization Examples",
    layout="wide"
)

st.title("🧪 Indicator Visualization Examples")
st.markdown("""
This page demonstrates how to use the `visualize_indicator` function for both standard indicators
and custom calculated indicators. These techniques can be applied throughout the Nexus Dashboard.
""")

# Load data
@st.cache_data
def load_data():
    return pd.read_parquet("../data/nexus.parquet")

df = load_data()

# ------------------------------------
# Example 1: Basic Indicator Plotting
# ------------------------------------
st.header("📊 Example 1: Basic Indicator Visualization")

# Select an indicator
indicators = sorted(df['indicator_label'].dropna().unique())
selected_indicator = st.selectbox("Choose an indicator", indicators)

# Select countries
countries = sorted(df['country_or_area'].dropna().unique())
selected_countries = st.multiselect(
    "Select countries", 
    countries, 
    default=countries[:3] if len(countries) > 3 else countries
)

# Get ISO3 codes for selected countries
selected_iso3 = df[df['country_or_area'].isin(selected_countries)]['iso3'].unique().tolist()

# Choose chart type
chart_type = st.radio("Chart type", ["bar", "line"], horizontal=True)

# Basic visualization
st.subheader("Standard Indicator Visualization")
with st.expander("Show code", expanded=True):
    st.code("""
# Basic usage with a standard indicator
visualize_indicator(
    df=df,
    indicator_label=selected_indicator,
    countries=selected_iso3,
    chart_type=chart_type,
    y_title="Value"
)
""")

# Plot the indicator
if selected_indicator and selected_iso3:
    visualize_indicator(
        df=df,
        indicator_label=selected_indicator,
        countries=selected_iso3,
        chart_type=chart_type,
        y_title="Value"
    )
else:
    st.warning("Please select an indicator and at least one country.")

# ---------------------------------------
# Example 2: Custom Calculated Indicator
# ---------------------------------------
st.header("🧪 Example 2: Custom Calculated Indicator")
st.markdown("""
This example demonstrates how to create a custom indicator by calculating a ratio 
between two existing indicators.
""")

# Select base indicators for custom calculation
st.subheader("Select two indicators to create a ratio")
indicator_1 = st.selectbox("Numerator indicator", indicators, index=0)
indicator_2 = st.selectbox("Denominator indicator", indicators, index=1 if len(indicators) > 1 else 0)

# Countries for comparison
custom_countries = st.multiselect(
    "Select countries for comparison", 
    countries, 
    default=countries[:3] if len(countries) > 3 else countries,
    key="custom_countries"
)

# Get ISO3 codes for custom countries
custom_iso3 = df[df['country_or_area'].isin(custom_countries)]['iso3'].unique().tolist()

# Custom visualization
st.subheader("Custom Calculated Indicator")
with st.expander("Show code", expanded=True):
    st.code(f"""
# Define a function that calculates the custom indicator
def calculate_indicator_ratio():
    # Get data for first indicator
    df1 = df[df["indicator_label"] == "{indicator_1}"].copy()
    
    # Get data for second indicator
    df2 = df[df["indicator_label"] == "{indicator_2}"].copy()
    
    # Merge on country and year
    merged = pd.merge(
        df1[["year", "country_or_area", "iso3", "value"]],
        df2[["year", "country_or_area", "iso3", "value"]],
        on=["year", "country_or_area", "iso3"],
        suffixes=("_1", "_2")
    )
    
    # Calculate ratio (handling division by zero)
    merged["value"] = np.where(
        merged["value_2"] != 0,
        merged["value_1"] / merged["value_2"],
        np.nan
    )
    
    return merged

# Use the function with visualize_indicator
visualize_indicator(
    df=df,  # Original dataframe is passed but not used directly
    calculation_function=calculate_indicator_ratio,
    chart_type="line",
    countries=custom_iso3,
    y_title=f"Ratio: {indicator_1} / {indicator_2}"
)
""")

# Define the calculation function
def calculate_indicator_ratio():
    # Get data for both indicators
    df1 = df[df["indicator_label"] == indicator_1].copy()
    df2 = df[df["indicator_label"] == indicator_2].copy()
    
    # Merge on country and year
    merged = pd.merge(
        df1[["year", "country_or_area", "iso3", "value", "region_name"]],
        df2[["year", "country_or_area", "iso3", "value"]],
        on=["year", "country_or_area", "iso3"],
        suffixes=("_1", "_2")
    )
    
    # Calculate ratio (handling division by zero)
    merged["value"] = np.where(
        merged["value_2"] != 0,
        merged["value_1"] / merged["value_2"],
        np.nan
    )
    
    return merged

# Plot the custom indicator
if indicator_1 and indicator_2 and custom_iso3:
    visualize_indicator(
        df=df,
        calculation_function=calculate_indicator_ratio,
        chart_type="line",
        countries=custom_iso3,
        y_title=f"Ratio: {indicator_1} / {indicator_2}"
    )
else:
    st.warning("Please select two indicators and at least one country.")

# Add some tips and best practices
st.header("🔍 Tips & Best Practices")
st.markdown("""
### When to use a custom calculation function:
- When you need to derive new indicators from existing ones
- For complex transformations that require multiple indicators
- To aggregate or transform data beyond simple filtering

### Best practices:
1. Always handle potential data issues (missing values, division by zero)
2. Ensure your calculation function returns all required columns (year, value, country_or_area, iso3)
3. Document what your calculation does so others can understand it
4. Consider performance with large datasets - use efficient pandas operations
""")

# Add information about more advanced visualization techniques
st.header("🔄 Advanced Techniques")
st.markdown("""
You can extend the `visualize_indicator` function with:

1. **Custom Aggregations**: Group by regions or time periods
```python
def calculate_regional_averages():
    # Get indicator data
    data = df[df["indicator_label"] == "Tax Revenue - % of GDP - value"].copy()
    
    # Group by region and year
    grouped = data.groupby(["region_name", "year"])["value"].mean().reset_index()
    
    # Rename region_name to country_or_area for compatibility
    grouped["country_or_area"] = grouped["region_name"]
    grouped["iso3"] = grouped["region_name"]  # Use region as iso3 for filtering
    
    return grouped
```

2. **Year-over-Year Growth**: Calculate percentage changes
```python
def calculate_yoy_growth():
    # Get indicator data
    data = df[df["indicator_label"] == "Tax Revenue - % of GDP - value"].copy()
    
    # Sort by country and year
    data = data.sort_values(["country_or_area", "year"])
    
    # Calculate year-over-year percentage change
    data["value"] = data.groupby("country_or_area")["value"].pct_change() * 100
    
    return data
```
""") 