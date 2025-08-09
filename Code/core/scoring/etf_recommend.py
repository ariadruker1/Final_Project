def top_5_recommend(df, sharpe_col='Sharpe_Ratio'):
    """
    Returns top 5 rows with highest Sharpe ratios and prints elapsed time.

    Args:
        df (pd.DataFrame): DataFrame containing at least the column `sharpe_col`.
        sharpe_col (str): Column name for Sharpe ratio (default 'Sharpe_Ratio').

    Returns:
        pd.DataFrame: Top 5 rows sorted by Sharpe ratio descending.
    """
    if sharpe_col not in df.columns:
        raise ValueError(f"Column '{sharpe_col}' not found in DataFrame.")

    # Drop rows with NaN Sharpe ratios to avoid errors in sorting
    df_clean = df.dropna(subset=[sharpe_col])

    # Sort descending by Sharpe ratio
    df_sorted = df_clean.sort_values(by=sharpe_col, ascending=False)

    result = df_sorted.head(5)

    return result
