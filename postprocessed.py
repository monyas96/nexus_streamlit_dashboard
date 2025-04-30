import pandas as pd
import numpy as np
from typing import Optional, List, Dict
import altair as alt
from universal_viz import generate_placeholder_data, visualize_indicator

# Data processing functions
def calculate_expenditure_outturn(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate expenditure outturn comparing intended vs actual expenditure.
    
    Args:
        df: Main dataset containing PEFA indicators
    
    Returns:
        DataFrame with expenditure outturn data
    """
    expenditure_data = df[df["indicator_label"].str.contains(
        "PEFA: Aggregate expenditure out-turn", 
        case=False, 
        na=False
    )].copy()
    
    if len(expenditure_data) == 0:
        # Generate placeholder data
        countries = df["iso3"].dropna().unique()[:5] if "iso3" in df.columns and len(df) > 0 else ["USA", "GBR", "FRA", "DEU", "JPN"]
        years = list(range(2015, 2021))
        return generate_placeholder_data(
            countries=countries,
            years=years,
            base_value=25.0,
            indicator_types=["Intended", "Actual"]
        )
    
    return expenditure_data

def calculate_tax_revenue_gdp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate tax revenue as percentage of GDP.
    
    Args:
        df: Main dataset containing tax revenue indicators
    
    Returns:
        DataFrame with tax revenue data containing year, country, ISO3 code, value, and region
    """
    tax_data = df[df["indicator_label"] == "Tax Revenue - % of GDP - value"].copy()
    
    if len(tax_data) == 0:
        # Generate placeholder data for empty result
        countries = df["iso3"].dropna().unique()[:5] if "iso3" in df.columns and len(df) > 0 else ["USA", "GBR", "FRA", "DEU", "JPN"]
        years = list(range(2015, 2021))
        placeholder_data = generate_placeholder_data(
            countries=countries,
            years=years,
            base_value=15.0,
            trend=0.05
        )
        # Add required columns
        placeholder_data["region_name"] = "Unknown"
        placeholder_data["indicator_label"] = "Tax Revenue - % of GDP - value"
        
        # Add country_or_area if not present
        if "country_or_area" not in placeholder_data.columns:
            country_names = {
                "USA": "United States", 
                "GBR": "United Kingdom",
                "FRA": "France",
                "DEU": "Germany",
                "JPN": "Japan"
            }
            placeholder_data["country_or_area"] = placeholder_data["iso3"].map(
                lambda x: country_names.get(x, x)
            )
        
        return placeholder_data
    
    return tax_data

def calculate_tax_effort_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate tax effort ratio (actual/potential tax revenue).
    
    Args:
        df: Main dataset containing tax indicators
    
    Returns:
        DataFrame with tax effort data
    """
    actual_tax = df[df["indicator_label"] == "Tax Revenue - % of GDP - value"].copy()
    potential_tax = df[df["indicator_label"] == "Tax Revenue - % of GDP - Capacity"].copy()
    
    if len(actual_tax) > 0 and len(potential_tax) > 0:
        merged = pd.merge(
            actual_tax[["year", "country_or_area", "iso3", "value", "region_name"]],
            potential_tax[["year", "country_or_area", "iso3", "value"]],
            on=["year", "country_or_area", "iso3"],
            suffixes=("_actual", "_potential")
        )
        
        merged["value"] = np.where(
            merged["value_potential"] > 0,
            merged["value_actual"] / merged["value_potential"],
            np.nan
        )
        
        return merged
    
    # Generate placeholder data
    countries = df["iso3"].dropna().unique()[:5] if "iso3" in df.columns and len(df) > 0 else ["USA", "GBR", "FRA", "DEU", "JPN"]
    years = list(range(2015, 2021))
    return generate_placeholder_data(
        countries=countries,
        years=years,
        base_value=0.8,
        variation=0.1
    )

def calculate_taxpayer_composition(
    df: pd.DataFrame,
    country: Optional[str] = None,
    year: Optional[int] = None
) -> pd.DataFrame:
    """
    Calculate taxpayer composition by type.
    
    Args:
        df: Main dataset
        country: ISO3 country code
        year: Year for analysis
    
    Returns:
        DataFrame with taxpayer composition data
    """
    taxpayer_types = [
        "Number of corporate income taxpayers",
        "Number of VAT taxpayers",
        "Number of personal income taxpayers",
        "Number of wage/salary taxpayers (employers)",
        "Number of wage/salary taxpayers (employees)",
        "Number of trust taxpayers"
    ]
    
    taxpayer_data = df[df["indicator_label"].isin(taxpayer_types)].copy()
    
    if country:
        taxpayer_data = taxpayer_data[taxpayer_data["iso3"] == country]
    if year:
        taxpayer_data = taxpayer_data[taxpayer_data["year"] == year]
    
    if len(taxpayer_data) == 0:
        if not country or not year:
            raise ValueError("Both country and year must be provided for placeholder data")
            
        # Get country metadata from the main dataset if available
        country_metadata = {}
        if "iso3" in df.columns and len(df) > 0:
            country_info = df[df["iso3"] == country].iloc[0] if any(df["iso3"] == country) else None
            if country_info is not None:
                country_metadata = {
                    "country_or_area": country_info.get("country_or_area", country),
                    "region_name": country_info.get("region_name", "Unknown")
                }
        
        # Use default mapping if metadata not found
        if not country_metadata:
            country_names = {
                "USA": "United States", 
                "GBR": "United Kingdom",
                "FRA": "France",
                "DEU": "Germany",
                "JPN": "Japan"
            }
            regions = {
                "USA": "North America",
                "GBR": "Europe",
                "FRA": "Europe",
                "DEU": "Europe",
                "JPN": "Asia"
            }
            country_metadata = {
                "country_or_area": country_names.get(country, country),
                "region_name": regions.get(country, "Unknown")
            }
            
        data = []
        for taxpayer_type in taxpayer_types:
            value = np.random.randint(10000, 1000000)
            data.append({
                "year": year,
                "value": value,
                "iso3": country,
                "indicator_label": taxpayer_type,
                "country_or_area": country_metadata["country_or_area"],
                "region_name": country_metadata["region_name"]
            })
        
        return pd.DataFrame(data)
    
    return taxpayer_data

# Legacy function for backward compatibility
def plot_indicator(
    df: pd.DataFrame,
    indicator_label: str,
    countries: Optional[List[str]] = None,
    chart_type: str = "bar",
    y_title: str = "Value",
    show_chart: bool = True
) -> alt.Chart:
    """
    Legacy function maintained for backward compatibility.
    Please use visualize_indicator() for new code.
    """
    return visualize_indicator(
        df=df,
        indicator_label=indicator_label,
        countries=countries,
        chart_type=chart_type,
        y_title=y_title,
        show_chart=show_chart
    )

def visualize_expenditure_outturn(
    df: pd.DataFrame,
    selected_iso3: List[str],
    year_range: Optional[List[int]] = None
) -> Dict:
    """
    Create visualization for expenditure outturn (Topic 4.1.1).
    
    Args:
        df: Main dataset
        selected_iso3: List of selected ISO3 country codes
        year_range: Optional [start_year, end_year] for filtering
        
    Returns:
        Dict containing chart object and calculated metrics
    """
    def get_filtered_data():
        data = calculate_expenditure_outturn(df)
        filtered = data[data["iso3"].isin(selected_iso3)]
        if year_range:
            filtered = filtered[(filtered["year"] >= year_range[0]) & 
                              (filtered["year"] <= year_range[1])]
        return filtered
    
    # Create visualization
    chart = visualize_indicator(
        df=df,
        calculation_function=get_filtered_data,
        chart_type="stacked_bar",
        y_title="Percentage (%)",
        title="Aggregate Expenditure Outturn",
        color_by="indicator_type",
        stack=True,
        color_scale={"Intended": "#EC2E07", "Actual": "#072D92"},
        domain=["Intended", "Actual"]
    )
    
    # Calculate metrics
    metrics = {}
    data = get_filtered_data()
    if len(data) > 0:
        latest_year = data["year"].max()
        latest_data = data[data["year"] == latest_year]
        
        actual_data = latest_data[latest_data["indicator_type"] == "Actual"]
        intended_data = latest_data[latest_data["indicator_type"] == "Intended"]
        
        avg_actual = actual_data["value"].mean()
        avg_intended = intended_data["value"].mean()
        efficiency = (avg_actual / avg_intended * 100) if avg_intended > 0 else 0
        
        metrics = {
            "avg_actual": avg_actual,
            "avg_intended": avg_intended,
            "efficiency": efficiency
        }
    
    return {
        "chart": chart,
        "metrics": metrics
    }

def calculate_expenditure_quality(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate expenditure quality indicators data."""
    quality_indicators = [
        "PEFA: Expenditure composition outturn by function",
        "PEFA: Expenditure composition outturn by economic type",
        "PEFA: Expenditure from contingency reserves"
    ]
    
    quality_data = df[df["indicator_label"].isin(quality_indicators)].copy()
    
    if len(quality_data) == 0:
        countries = df["iso3"].dropna().unique()[:5] if "iso3" in df.columns and len(df) > 0 else ["USA", "GBR", "FRA", "DEU", "JPN"]
        years = list(range(2015, 2021))
        placeholder = generate_placeholder_data(
            countries=countries,
            years=years,
            base_value=3.0,  # PEFA scores typically range from 1-4
            variation=0.5
        )
        # Add indicator types
        placeholder_data = []
        for indicator in quality_indicators:
            temp = placeholder.copy()
            temp["indicator_label"] = indicator
            placeholder_data.append(temp)
        return pd.concat(placeholder_data, ignore_index=True)
    
    return quality_data

def visualize_expenditure_quality(
    df: pd.DataFrame,
    selected_iso3: List[str],
    year_range: Optional[List[int]] = None
) -> Dict:
    """
    Create visualization for expenditure quality (Topic 4.1.2).
    
    Args:
        df: Main dataset
        selected_iso3: List of selected ISO3 country codes
        year_range: Optional [start_year, end_year] for filtering
        
    Returns:
        Dict containing chart object
    """
    def get_filtered_data():
        data = calculate_expenditure_quality(df)
        filtered = data[data["iso3"].isin(selected_iso3)]
        if year_range:
            filtered = filtered[(filtered["year"] >= year_range[0]) & 
                              (filtered["year"] <= year_range[1])]
        return filtered
    
    # Create visualization
    chart = visualize_indicator(
        df=df,
        calculation_function=get_filtered_data,
        chart_type="bar",
        y_title="Score",
        title="Expenditure Quality Indicators",
        color_by="indicator_label",
        facet_by="indicator_label",
        facet_cols=1,
        height=200
    )
    
    return {"chart": chart}
