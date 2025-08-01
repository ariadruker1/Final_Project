import yfinance as yf
import ishares_ETF_list as ishares
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def get_etf_data(symbols, years):
    """
    Get annual growth and standard deviation for multiple time periods for all ETFs

    Args:
        symbols (list): List of ETF ticker symbols
        delay (float): Delay between requests to avoid rate limiting

    Returns:
        pd.DataFrame: DataFrame with all metrics
    """
    end_date = datetime.now()  # years
    results = []

    print(f"Processing {len(symbols)} ETFs...")

    for i, symbol in enumerate(symbols):
        row = {'Symbol': symbol}

        ticker = yf.Ticker(symbol)

        # Calculate start date
        start_date = end_date - timedelta(days=365 * years)
        data = ticker.history(start=start_date.strftime('%Y-%m-%d'),
                              end=end_date.strftime('%Y-%m-%d'))

        try:
            # calculate annual growth
            start_price = data['Close'].iloc[0]
            end_price = data['Close'].iloc[-1]

            annual_growth = ((end_price / start_price) - 1) * 100 / years
            annual_growth = round(annual_growth, 2)

            # calculate annual standard deviation
            daily_returns = data['Close'].pct_change().dropna()
            annual_std = daily_returns.std() * np.sqrt(252) * 100
            annual_std = round(annual_std, 2)

        except:
            annual_growth, annual_std, start_price = None, None, None

        row[f'Annual_Growth_{years}Y'] = annual_growth
        row[f'Standard_Deviation_{years}Y'] = annual_std

        results.append(row)

    return pd.DataFrame(results)


def export_etf_data(symbols, years, filename=None):
    """
    Export ETF data to CSV

    Args:
        symbols (list): List of ETF symbols
        filename (str): Output filename (auto-generated if None)

    Returns:
        str: Filename of exported CSV
    """
    df = get_etf_data(symbols, years)

    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'etf_data_{timestamp}.csv'

    df.to_csv(filename, index=False)
    print(f"Data exported to: {filename}")
    return filename


# Example usage
if __name__ == "__main__":
    years = 10
    etfs = ishares.ETFs
    # Export data
    filename = export_etf_data(etfs, years)
