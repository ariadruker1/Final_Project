import pandas as pd
from ishares_ETF_list import download_valid_data
from datetime import datetime

def calculate_max_drawdown(user_max_drawdown, user_minimum_efs_age, valid_tickers, data, end_date):
    tickers_within_user_drawdown_tolerance = []

    for ticker in valid_tickers:
        if 'Adj Close' not in data[ticker]:
            continue

        prices = data[ticker]['Adj Close'].dropna()
        past_10_year_date = end_date - pd.DateOffset(years=10)

        prices_origin = prices[prices.index <= end_date]
        prices_10_year = prices[(prices.index >= past_10_year_date) & (prices.index <= end_date)]
        
        if not prices_origin.empty:
            running_max = prices_origin.cummax()
            drawdown = (prices_origin - running_max) / running_max
            max_drawdown_origin = drawdown.min() * 100
        else:
            max_drawdown_origin = None 

        if not prices_10_year.empty:
            running_max_10yr = prices_10_year.cummax()
            drawdown_10yr = (prices_10_year - running_max_10yr) / running_max_10yr
            max_drawdown_10yr = drawdown_10yr.min() * 100
        else:
            max_drawdown_10yr = None 

        if max_drawdown_origin is not None and max_drawdown_10yr is not None:
            max_drawdown = 0.3 * max_drawdown_origin + 0.7 * max_drawdown_10yr
        elif max_drawdown_origin is not None:
            max_drawdown = max_drawdown_origin
        elif max_drawdown_10yr is not None:
            max_drawdown = max_drawdown_10yr
        else:
            continue 

        minimum_age_etf = datetime.now() - pd.DateOffset(years=user_minimum_efs_age)
        if max_drawdown >= -user_max_drawdown and prices.index.min() < minimum_age_etf:
            tickers_within_user_drawdown_tolerance.append(ticker)

    return tickers_within_user_drawdown_tolerance
