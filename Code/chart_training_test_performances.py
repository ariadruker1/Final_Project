import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from matplotlib.lines import Line2D

def plot_etf_performance_with_user_preferences(
    data, custom_tickers, sharpe_tickers, test_period,
    user_time_horizon, user_growth_pct, user_std_pct, user_max_drawdown, user_etf_age, user_risk_pref
):
    """
    Plot ETF prices over training and test periods, normalized, with user desired cumulative growth
    and linear risk bands per ETF starting at that ETF's end of training normalized price,
    plus a user profile summary and legend below.
    """
    today = pd.Timestamp(datetime.now())
    train_start = today - pd.DateOffset(years=user_time_horizon + test_period)
    train_end = today - pd.DateOffset(years=test_period)
    test_start = train_end
    test_end = today

    plt.figure(figsize=(12, 8))

    # Colors assigned per your legend request with purple for overlap
    color_custom = "#ff7f0e"   # orange
    color_sharpe = "#1f77b4"   # blue
    color_both = "#9467bd"     # purple (overlap)

    set_custom = set(custom_tickers)
    set_sharpe = set(sharpe_tickers)
    all_tickers = set_custom.union(set_sharpe)

    # Dates for test period
    dates_test = pd.date_range(start=test_start, end=test_end, freq='B')
    years_elapsed_test = (dates_test - test_start).days / 365.25

    # Plot ETFs
    for ticker in sorted(all_tickers):
        in_custom = ticker in set_custom
        in_sharpe = ticker in set_sharpe

        if in_custom and in_sharpe:
            color = color_both
        elif in_custom:
            color = color_custom
        else:
            color = color_sharpe

        # Get price series
        try:
            price_series = data[(ticker, 'Adj Close')].dropna()
        except Exception:
            try:
                price_series = data[ticker].dropna()
            except Exception:
                print(f"[⚠] Missing price data for {ticker}, skipping.")
                continue

        # Training normalization (start at 100)
        train_prices = price_series.loc[train_start:train_end]
        if train_prices.empty:
            continue
        train_norm = 100 * train_prices / train_prices.iloc[0]

        # Test normalization (continuity from training)
        test_prices = price_series.loc[test_start:test_end]
        if test_prices.empty:
            continue
        test_norm = 100 * test_prices / train_prices.iloc[0]
        scale_factor = train_norm.iloc[-1] / test_norm.iloc[0]
        test_norm *= scale_factor

        # Plot training (solid)
        plt.plot(train_norm.index, train_norm.values, label=f'{ticker} Training', color=color, linewidth=2)
        # Plot test (dashed)
        plt.plot(test_norm.index, test_norm.values, label=f'{ticker} Test', color=color,
                 linestyle='--', alpha=0.7, linewidth=1.5)

        # User desired growth & risk bands start at ETF training end normalized price
        baseline = train_norm.iloc[-1]
        user_growth_line = baseline * (1 + user_growth_pct / 100) ** years_elapsed_test
        risk_range = baseline * (user_std_pct / 100) * years_elapsed_test
        upper_band = user_growth_line + risk_range
        lower_band = user_growth_line - risk_range

        # Plot user growth line (lighter green for each ETF)
        plt.plot(dates_test, user_growth_line, color='green', linestyle='-', alpha=0.3, linewidth=1)
        # Plot risk band fill (lighter green, low alpha)
        plt.fill_between(dates_test, lower_band, upper_band, color='green', alpha=0.05)

    # Profile summary text (top-left)
    profile_text = (
        f"User Profile:\n"
        f"• Horizon: {user_time_horizon}y  "
        f"• Growth Goal: {user_growth_pct}%  "
        f"• Std Dev Tolerance: ±{user_std_pct}%\n"
        f"• Max Drawdown: {user_max_drawdown}%  "
        f"• Min ETF Age: {user_etf_age}y  "
        f"• Risk (Return:Risk): {user_risk_pref[1]}:{user_risk_pref[0]}"
    )
    plt.text(
        0.01, 0.98, profile_text,
        transform=plt.gca().transAxes,
        fontsize=9, va='top', ha='left',
        bbox=dict(boxstyle="round,pad=0.4", facecolor="whitesmoke", edgecolor="gray")
    )

    plt.title('ETF Performance (Training and Test Periods)')
    plt.xlabel('Date')
    plt.ylabel('Normalized Adjusted Close Price')
    plt.grid(True)

    # Custom legend for sets + user band
    legend_elements = [
        Line2D([0], [0], color=color_custom, lw=3, label='Custom-only ETFs (orange)'),
        Line2D([0], [0], color=color_sharpe, lw=3, label='Sharpe-only ETFs (blue)'),
        Line2D([0], [0], color=color_both, lw=3, label='ETFs in both sets (purple)'),
        Line2D([0], [0], color='green', lw=3, label='User Desired Growth & Risk Band'),
    ]

    plt.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False, fontsize=9)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)
    plt.show()
