import pandas as pd
import numpy as np
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
    test_end=None,
    risk_free_rate=0.02,
):
    if test_end is None:
        test_end = pd.Timestamp.today()

    df = df.loc[test_start:test_end, :]  # slice the testing period

    results = []

    for label, tickers in [('Custom', custom_tickers), ('Sharpe', sharpe_tickers)]:
        combined_returns = []

        for ticker in tickers:
            if (ticker, 'Adj Close') not in df.columns:
                print(f"{ticker} not found in test data.")
                continue

            prices = df[(ticker, 'Adj Close')].dropna()
            if len(prices) < 2:
                continue

            returns = prices.pct_change().dropna()
            combined_returns.append(returns)

        if not combined_returns:
            print(f"No valid returns for {label}")
            results.append([
                label, None, None, None, None, None, None
            ])
            continue

        test_returns = pd.concat(combined_returns, axis=1).mean(axis=1)

        # Calculate metrics
        ann_return = (1 + test_returns.mean()) ** 252 - 1
        ann_std = test_returns.std() * np.sqrt(252)
        sharpe = (ann_return - risk_free_rate) / ann_std if ann_std else np.nan

        downside = test_returns[test_returns < 0]
        sortino = (ann_return - risk_free_rate) / (downside.std() * np.sqrt(252)) if not downside.empty else np.nan

        cum_returns = (1 + test_returns).cumprod()
        peak = cum_returns.cummax()
        drawdown = (cum_returns - peak) / peak
        max_dd = drawdown.min()

        if user_growth is not None and user_std is not None:
            threshold = (user_growth - user_std) / 100 / 252
            shortfalls = np.where(test_returns < threshold, threshold - test_returns, 0)
            mean_shortfall = np.mean(shortfalls)
            reward_to_shortfall = ann_return * 100 - mean_shortfall * 100
        else:
            mean_shortfall = np.nan
            reward_to_shortfall = np.nan

        results.append([
            label,
            round(ann_return * 100, 2),
            round(ann_std * 100, 2),
            round(sharpe, 2),
            round(sortino, 2) if not np.isnan(sortino) else None,
            round(max_dd * 100, 2),
            round(reward_to_shortfall, 2)
        ])

    return pd.DataFrame(results, columns=[
        'method', 'Annual Return (%)', 'Volatility (%)', 'Sharpe', 'Sortino',
        'Max Drawdown (%)', 'Reward to Shortfall'
    ]).set_index('method')
