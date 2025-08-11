def top_recommend(df, column_title, amount):
    """
    Returns top 5 rows with highest scoring etf data.

    Args:
        df (pd.DataFrame): DataFrame containing at least the column `column_title`.
        column_title (str): Column name.

    Returns:
        pd.DataFrame: Top 5 rows sorted by descending.
    """
    if column_title not in df.columns:
        raise ValueError(f"Column '{column_title}' not found in DataFrame.")

    # Drop rows with NaN Sharpe ratios to avoid errors in sorting
    df_clean = df.dropna(subset=[column_title])

    # Sort descending by Sharpe ratio
    df_sorted = df_clean.sort_values(by=column_title, ascending=False)

    result = df_sorted.head(amount)

    return result
