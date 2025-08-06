import pandas as pd

def sharpe_top_5(etf_df, time_horizon, risk_free_df):
    """
    Compute Sharpe Ratios and return top 5 ETFs by Sharpe Ratio.

    Args:
        etf_df (pd.DataFrame): DataFrame with annual growth and std deviation columns.
        time_horizon (int): Time period in years.
        risk_free_df (pd.DataFrame): DataFrame with 'yield_pct' column indexed by date.

    Returns:
        pd.DataFrame: Top 5 ETFs with highest Sharpe Ratios.
    """
    growth_col = f'Annual_Growth_{time_horizon}Y'
    std_col = f'Standard_Deviation_{time_horizon}Y'

    # Drop rows missing required data
    df = etf_df.dropna(subset=[growth_col, std_col]).copy()

    # Calculate average risk-free rate over time horizon
    end = risk_free_df.index.max()
    start = end - pd.DateOffset(years=time_horizon)
    rf_period = risk_free_df.loc[start:end]
    avg_rf = rf_period['yield_pct'].mean()

    # Calculate excess return
    df['ExcessReturn'] = df[growth_col] - avg_rf  # in percent

    # Compute Sharpe Ratio: Excess Return / Std Deviation
    df['Sharpe'] = df['ExcessReturn'] / df[std_col]

    # Return top 5
    top_5 = df.sort_values('Sharpe', ascending=False).head(5)
    return top_5['Ticker'].tolist()
