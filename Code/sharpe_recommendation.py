import pandas as pd

def sharpe_score(etf_df, time_horizon, risk_free_df):
    """
    Compute Sharpe Ratios and return ETFs sorted by Sharpe Ratio.

    Args:
        etf_df (pd.DataFrame): DataFrame with annual growth and std deviation columns.
        time_horizon (int): Time period in years.
        risk_free_df (pd.DataFrame): DataFrame with 'yield_pct' column indexed by date.

    Returns:
        pd.DataFrame: ETFs sorted by Sharpe Ratio (descending).
    """
    growth_col = f'Annual_Growth_{time_horizon}Y'
    std_col = f'Standard_Deviation_{time_horizon}Y'

    df = etf_df.dropna(subset=[growth_col, std_col]).copy()

    end = risk_free_df.index.max()
    start = end - pd.DateOffset(years=time_horizon)
    rf_period = risk_free_df.loc[start:end]
    avg_rf = rf_period['yield_pct'].mean()

    df['ExcessReturn'] = df[growth_col] - avg_rf
    df['Sharpe'] = df['ExcessReturn'] / df[std_col]

    return df.sort_values('Sharpe', ascending=False)
