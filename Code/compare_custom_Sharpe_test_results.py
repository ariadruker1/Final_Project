import pandas as pd
import numpy as np

def quantitative_etf_basket_comparison(
    df,
    custom_tickers,
    sharpe_tickers,
    user_growth,
    user_std,
    user_risk_preference, #[risk_weight, return_weight]
    test_start,
    test_end=None
):
    if test_end is None:
        test_end = pd.Timestamp.today()

    df = df[(df.index >= test_start) & (df.index <= test_end)].copy()

    results = []

    for label, tickers in [('Custom', custom_tickers), ('Sharpe', sharpe_tickers)]:
        combined_returns = []

        for ticker in tickers:
            try:
                prices = df[(ticker, 'Adj Close')].dropna()
                if len(prices) < 2:
                    continue

                prices = prices / prices.iloc[0] * 100  # Normalize to 100
                daily_returns = prices.pct_change().dropna()
                if daily_returns.empty:
                    continue

                mean_daily_return = daily_returns.mean()
                annual_return = (1 + mean_daily_return) ** 252 - 1
                combined_returns.append(daily_returns)

            except Exception:
                continue

        if not combined_returns:
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
            # Custom weighted score
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

    return pd.DataFrame(results, columns=['Set', 'mean_annual_return_pct', 'mean_shortfall', 'reward_to_shortfall'])
