import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def get_etf_data(tickers, years, all_data):
    """
    Get annual growth and standard deviation for multiple time periods for all ETFs
    Args:
    tickers (list): List of ETF tickers to analyze
    years (int): Number of years ago to calculate metrics
    all_data (pd.DataFrame): DataFrame containing all-time data for all ETFs
    Returns:
    pd.DataFrame: DataFrame with annual growth and standard deviation for each ETF
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * years)
    results = []
    print(f"Processing {len(tickers)} ETFs...")

    # Filter time period
    period_data = all_data[all_data.index >= start_date]

    for i, ticker in enumerate(tickers):
        row = {'Ticker': ticker}
        try:
            # Check if ticker exists in the data
            if ticker not in all_data.columns.get_level_values(0):
                annual_growth, annual_std = None, None
            else:
                # Get data for this specific ticker
                ticker_data = period_data[(ticker, 'Close')].dropna()

                if len(ticker_data) < 2:
                    annual_growth, annual_std = None, None
                else:
                    # Find the price closest to start_date (N years ago)
                    start_idx = ticker_data.index.get_indexer(
                        [start_date], method='nearest')[0]
                    start_price = ticker_data.iloc[start_idx]
                    end_price = ticker_data.iloc[-1]

                    annual_growth = (
                        (end_price / start_price) - 1) * 100 / years
                    annual_growth = round(annual_growth, 2)

                    # calculate annual standard deviation
                    daily_returns = ticker_data.pct_change().dropna()
                    annual_std = daily_returns.std() * np.sqrt(252) * 100
                    annual_std = round(annual_std, 2)
        except:
            annual_growth, annual_std = None, None

        row[f'Annual_Growth_{years}Y'] = annual_growth
        row[f'Standard_Deviation_{years}Y'] = annual_std
        results.append(row)

    return pd.DataFrame(results)
