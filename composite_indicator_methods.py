import pandas as pd

def calculate_banking_sector_development_index(df, country_col='country_or_area', year_col='year'):
    """
    Calculate the Banking Sector Development Index for each country-year.

    Methodology:
    The index is a weighted sum of three indicators:
      - Bank capital to assets ratio (%) [weight: 40%]
      - Bank liquid reserves to bank assets ratio (%) [weight: 30%]
      - Domestic credit provided by financial sector (% of GDP) [weight: 30%]
    
    If any of the three indicators is missing for a country-year, the index is not calculated for that country-year.

    Weights:
      - Bank capital to assets ratio: 40%
      - Bank liquid reserves to bank assets ratio: 30%
      - Domestic credit provided by financial sector: 30%

    Rationale:
    This weighting balances financial stability (capital and liquidity) with economic growth (credit provision),
    aligning with Basel III and empirical research (see references).

    References:
    1. Jordà, Ò., Schularick, M., & Taylor, A. M. (2017). Macrofinancial History and the New Business Cycle Facts. NBER.
    2. Berger, A. N., & Bouwman, C. H. (2013). How Does Capital Affect Bank Performance During Financial Crises? JFE.
    3. Diamond, D. W., & Dybvig, P. H. (1983). Bank Runs, Deposit Insurance, and Liquidity. JPE.
    4. Brunnermeier, M. K., & Pedersen, L. H. (2009). Market Liquidity and Funding Liquidity. RFS.
    5. Schularick, M., & Taylor, A. M. (2012). Credit Booms Gone Bust. AER.
    6. Gambacorta, L., & Shin, H. S. (2018). Why Bank Capital Matters for Monetary Policy. JFI.

    Parameters:
        df (pd.DataFrame): DataFrame with columns: country_col, year_col, indicator_label, value
        country_col (str): Name of the country column
        year_col (str): Name of the year column

    Returns:
        pd.DataFrame: DataFrame with columns [country_col, year_col, 'Banking Sector Development Index']
    """
    # Define indicator labels (must match your data exactly)
    indicators = {
        'Bank capital to assets ratio (%)': 0.4,
        'Bank liquid reserves to bank assets ratio (%)': 0.3,
        'Domestic credit provided by financial sector (% of GDP)': 0.3
    }
    # Pivot to wide format: one row per country-year, columns for each indicator
    df_pivot = df[df['indicator_label'].isin(indicators.keys())].pivot_table(
        index=[country_col, year_col],
        columns='indicator_label',
        values='value'
    )
    # Only keep rows where all three indicators are present
    df_pivot = df_pivot.dropna(subset=indicators.keys())
    # Calculate weighted sum
    df_pivot['Banking Sector Development Index'] = sum(
        df_pivot[ind] * weight for ind, weight in indicators.items()
    )
    # Reset index for output
    result = df_pivot[['Banking Sector Development Index']].reset_index()
    return result 

def calculate_stock_market_cap_to_gdp(df, country_col='country_or_area', year_col='year'):
    """
    Calculate Stock Market Capitalization to GDP (%) for each country-year.
    Formula: (Market capitalization of listed domestic companies (current US$) / GDP (current US$)) * 100
    If either value is missing for a country-year, the result is missing for that country-year.
    Returns a DataFrame with columns: country, year, Stock Market Cap to GDP (%)
    Handles both wide and long formats.
    """
    market_cap_col = 'Market capitalization of listed domestic companies (current US$)'
    gdp_col = 'GDP (current US$)'
    indicators = [market_cap_col, gdp_col]
    # If wide format, melt to long
    if all(col in df.columns for col in [country_col, year_col, market_cap_col, gdp_col]):
        df_long = df.melt(
            id_vars=[country_col, year_col],
            value_vars=indicators,
            var_name='indicator_label',
            value_name='value'
        )
    elif all(col in df.columns for col in [country_col, year_col, 'indicator_label', 'value']):
        df_long = df.copy()
    else:
        return pd.DataFrame(columns=[country_col, year_col, 'Stock Market Cap to GDP (%)'])
    df_pivot = df_long[df_long['indicator_label'].isin(indicators)].pivot_table(
        index=[country_col, year_col],
        columns='indicator_label',
        values='value'
    )
    if not set(indicators).issubset(df_pivot.columns):
        return pd.DataFrame(columns=[country_col, year_col, 'Stock Market Cap to GDP (%)'])
    df_pivot = df_pivot.dropna(subset=indicators)
    df_pivot['Stock Market Cap to GDP (%)'] = (df_pivot[market_cap_col] / df_pivot[gdp_col]) * 100
    result = df_pivot[['Stock Market Cap to GDP (%)']].reset_index()
    return result

def calculate_adequacy_of_international_reserves(df, country_col='country_or_area', year_col='year'):
    """
    Calculate Adequacy of International Reserves for each country-year.
    Formula: (Reserves and related items (BoP, current US$)) / (External debt stocks, short-term (DOD, current US$))
    If either value is missing for a country-year, the result is missing for that country-year.
    Returns a DataFrame with columns: country, year, Adequacy of International Reserves
    """
    reserves_label = 'Reserves and related items (BoP, current US$)'
    debt_label = 'External debt stocks, short-term (DOD, current US$)'
    indicators = [reserves_label, debt_label]
    df_pivot = df[df['indicator_label'].isin(indicators)].pivot_table(
        index=[country_col, year_col],
        columns='indicator_label',
        values='value'
    )
    if not set(indicators).issubset(df_pivot.columns):
        return pd.DataFrame(columns=[country_col, year_col, 'Adequacy of International Reserves'])
    df_pivot = df_pivot.dropna(subset=indicators)
    df_pivot['Adequacy of International Reserves'] = df_pivot[reserves_label] / df_pivot[debt_label]
    result = df_pivot[['Adequacy of International Reserves']].reset_index()
    return result 

def calculate_indicator_with_gap(df, required_labels, calculation_func, country_col='country_or_area', year_col='year'):
    """
    Generalized function to calculate an indicator and identify data gaps.

    Parameters:
        df (pd.DataFrame): DataFrame with columns: country_col, year_col, indicator_label, value
        required_labels (list): List of required indicator labels
        calculation_func (function): Function to calculate the indicator from a DataFrame
        country_col (str): Name of the country column
        year_col (str): Name of the year column

    Returns:
        result (pd.DataFrame): DataFrame with calculated indicator
        missing (pd.DataFrame): DataFrame with missing country-year pairs
    """
    df_required = df[df['indicator_label'].isin(required_labels)]
    df_pivot = df_required.pivot_table(index=[country_col, year_col], columns='indicator_label', values='value')
    missing_mask = df_pivot.isnull().any(axis=1)
    missing = df_pivot[missing_mask].reset_index()[[country_col, year_col]]
    df_pivot = df_pivot.dropna()
    result = calculation_func(df_pivot)
    return result, missing 