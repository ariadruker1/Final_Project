import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd

def plot_etf_performance_with_user_preferences(
    data, tickers, train_start, train_end, test_start, test_end,
    user_time_horizon, user_growth_pct, user_std_pct, user_max_drawdown, user_etf_age, user_risk_pref):
    """
    Plot ETF prices over training and test periods, normalized, with user desired cumulative growth
    and linear risk bands, plus a user profile summary and legend below.
    """
    plt.figure(figsize=(12, 8))
    colors = list(mcolors.TABLEAU_COLORS.values())

    # Full date range for user bands (training + test)
    full_start = train_start
    full_end = test_end
    dates = pd.date_range(start=full_start, end=full_end, freq='B')
    years_elapsed = (dates - full_start).days / 365.25
    baseline = 100  # normalized base price

    # Compound user growth line
    user_growth_line = baseline * (1 + user_growth_pct / 100) ** years_elapsed

    # Linear risk band around that line
    risk_range = baseline * (user_std_pct / 100) * years_elapsed
    upper_band = user_growth_line + risk_range
    lower_band = user_growth_line - risk_range

    # Plot ETFs
    for i, ticker in enumerate(tickers):
        color = colors[i % len(colors)]

        try:
            price_series = data[(ticker, 'Adj Close')].dropna()
        except Exception:
            # fallback if structure is different
            try:
                price_series = data[ticker].dropna()
            except Exception:
                print(f"[⚠] Missing price data for {ticker}, skipping.")
                continue

        # Training normalized
        train_prices = price_series.loc[train_start:train_end]
        if train_prices.empty:
            continue
        train_norm = 100 * train_prices / train_prices.iloc[0]

        # Test normalized (same base)
        test_prices = price_series.loc[test_start:test_end]
        if test_prices.empty:
            continue
        test_norm = 100 * test_prices / train_prices.iloc[0]

        plt.plot(train_norm.index, train_norm.values, label=f'{ticker} Training', color=color, linewidth=2)
        plt.plot(test_norm.index, test_norm.values, label=f'{ticker} Test', color=color, linestyle='--', alpha=0.6, linewidth=1)

    # Plot user desired growth and linear risk band once
    plt.plot(dates, user_growth_line, color='green', linestyle='-', linewidth=2, label='User Desired Growth')
    plt.fill_between(dates, lower_band, upper_band, color='green', alpha=0.15, label='User Risk Band (± std dev)')

    # Profile summary (top-left inside plot)
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

    # Legend below plot
    plt.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.15),
        ncol=3,
        frameon=False,
        fontsize=9
    )
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)  # ensure space for legend
    plt.show()
