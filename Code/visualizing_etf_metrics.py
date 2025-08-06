import matplotlib.pyplot as plt
import mplcursors

def plot_risk_return_user(etf_metrics_df, user_growth, user_std, time_horizon, title):
    std_col = f'Standard_Deviation_{time_horizon}Y'
    growth_col = f'Annual_Growth_{time_horizon}Y'

    # Drop rows missing growth or std dev
    df_clean = etf_metrics_df.dropna(subset=[std_col, growth_col]).copy()

    plt.figure(figsize=(10, 7))

    scatter = plt.scatter(df_clean[std_col], df_clean[growth_col], alpha=0.5, label='ETFs')

    # Plot user profile as a big red dot
    plt.scatter(user_std, user_growth, color='red', s=100, label='User Profile')

    plt.xlabel('Standard Deviation (Risk %)')
    plt.ylabel('Annual Growth (%)')
    plt.title(title)
    plt.legend()
    plt.grid(True)

    # Add interactive hover annotations with ticker and values
    cursor = mplcursors.cursor(scatter, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        idx = sel.index
        ticker = df_clean.iloc[idx]['Ticker']
        growth = df_clean.iloc[idx][growth_col]
        stddev = df_clean.iloc[idx][std_col]
        sel.annotation.set(text=f"{ticker}\nGrowth: {growth:.2f}%\nStd Dev: {stddev:.2f}%")

    plt.show()
