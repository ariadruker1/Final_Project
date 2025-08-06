import pandas as pd

def utility_score(etf_df, time_horizon, risk_free_df, risk_pref):
    growth_col = f'Annual_Growth_{time_horizon}Y'
    std_col = f'Standard_Deviation_{time_horizon}Y'
    risk_w, return_w = risk_pref
    W_return = return_w / (return_w + risk_w)
    W_risk = risk_w / (return_w + risk_w)

    # compute avg risk-free
    end = risk_free_df.index.max()
    start = end - pd.DateOffset(years=time_horizon)
    rf_period = risk_free_df.loc[start:end]
    avg_rf = rf_period['yield_pct'].mean()

    df = etf_df.dropna(subset=[growth_col, std_col]).copy()
    df['ExcessReturn'] = df[growth_col] - avg_rf  # in percent

    # z-score normalize
    df['z_excess'] = (df['ExcessReturn'] - df['ExcessReturn'].mean()) / df['ExcessReturn'].std(ddof=1)
    df['z_std'] = (df[std_col] - df[std_col].mean()) / df[std_col].std(ddof=1)

    # utility: want high excess return, low std
    df['Utility_Score'] = W_return * df['z_excess'] - W_risk * df['z_std']

    return df.sort_values('Utility_Score', ascending=False)
