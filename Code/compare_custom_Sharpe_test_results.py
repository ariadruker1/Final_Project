import pandas as pd
import numpy as np

def quantitative_etf_basket_comparison(
    df,
    custom_tickers,
    sharpe_tickers,
    user_growth,
    user_std,
    user_risk_preference,  # [risk_weight, return_weight]
    test_start,
    test_end=None
):
    if test_end is None:
        test_end = pd.Timestamp.today()

    print(f"Test period: {test_start.date()} to {test_end.date()}")
    print(f"Data date range: {df.index.min().date()} to {df.index.max().date()}")
    
    # Use .loc to slice rows by date, keep all columns
    df = df.loc[test_start:test_end, :]
    print(f"Data shape after date filtering: {df.shape}")

    results = []

    for label, tickers in [('Custom', custom_tickers), ('Sharpe', sharpe_tickers)]:
        combined_returns = []
        print(f"\nProcessing {label} tickers: {tickers}")

        for ticker in tickers:
            # Check ticker columns existence
            if (ticker, 'Adj Close') not in df.columns:
                print(f"{ticker} not found in price data columns")
                continue

            prices = df[(ticker, 'Adj Close')].dropna()
            print(f"{ticker} prices count: {len(prices)}")

            if len(prices) < 2:
                print(f"Skipping {ticker} due to insufficient price data in test period")
                continue

            # Normalize prices and compute returns
            prices = prices / prices.iloc[0] * 100
            daily_returns = prices.pct_change().dropna()

            if daily_returns.empty:
                print(f"No returns data for {ticker}")
                continue

            combined_returns.append(daily_returns)

        if not combined_returns:
            print(f"No valid returns for {label}")
            mean_annual_return = 0
            mean_shortfall = np.nan
            reward_to_shortfall = np.nan
        else:
            daily_matrix = pd.concat(combined_returns, axis=1)
            mean_daily_return = daily_matrix.mean().mean()
            mean_annual_return = (1 + mean_daily_return) ** 252 - 1

            shortfall_threshold = (user_growth - user_std) / 100 / 252
            shortfalls = np.where(daily_matrix < shortfall_threshold,
                                  shortfall_threshold - daily_matrix, 0)
            mean_shortfall = np.mean(shortfalls)

            risk_weight, return_weight = user_risk_preference
            reward_to_shortfall = (
                return_weight * mean_annual_return * 100
                - risk_weight * mean_shortfall * 100
            )

        results.append([
            label,
            round(mean_annual_return * 100, 2),
            round(mean_shortfall, 4) if not np.isnan(mean_shortfall) else None,
            round(reward_to_shortfall, 2) if not np.isnan(reward_to_shortfall) else None
        ])

    df_results = pd.DataFrame(
        results,
        columns=['method', 'mean_annual_return_pct', 'mean_shortfall', 'reward_to_shortfall']
    ).set_index('method')

    print(f"\nResult DataFrame index labels: {df_results.index.tolist()}")

    return df_results
