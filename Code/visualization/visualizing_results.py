import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import pandas as pd

def plot_etfs_with_user(df, user_growth, user_std, time_horizon):
    std_col = f'Standard_Deviation_{time_horizon}Y'
    growth_col = f'Annual_Growth_{time_horizon}Y'

    df_clean = df.dropna(subset=[std_col, growth_col]).copy()

    # Plot raw values directly (no scaling)
    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(df_clean[std_col], df_clean[growth_col], alpha=0.5, label='ETFs')

    # Plot user profile point
    plt.scatter(user_std, user_growth, color='red', s=100, label='User Profile')

    plt.xlabel('Standard Deviation (Risk %)')  # raw units
    plt.ylabel('Annual Growth (%)')             # raw units
    plt.title(f'ETF Risk-Return Space with User Profile (Time Horizon = {time_horizon}Y)')
    plt.legend()
    plt.grid(True)

    # Add hover tooltips with mplcursors showing ticker and raw values
    cursor = mplcursors.cursor(scatter, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        idx = sel.index
        ticker = df_clean.iloc[idx]['Ticker']
        growth = df_clean.iloc[idx][growth_col]
        stddev = df_clean.iloc[idx][std_col]
        sel.annotation.set(text=f"{ticker}\nGrowth: {growth:.2f}%\nStd Dev: {stddev:.2f}%")

    plt.show()
