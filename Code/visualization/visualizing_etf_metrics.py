import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

def plot_risk_return_user(
    etf_metrics_df,
    user_growth,
    user_std,
    time_horizon,
    title,
    sharpe_list,
    utility_list,
    user_risk_ratio,
    user_min_etf_age,
    user_max_drawdown
):
    std_col = f'Standard_Deviation_{time_horizon}Y'
    growth_col = f'Annual_Growth_{time_horizon}Y'

    df_clean = etf_metrics_df.dropna(subset=[std_col, growth_col]).copy()
    
    labels_for_legend = {
        'Sharpe Only': 'blue',
        'Utility Only': 'orange',
        'Both': 'purple',
        'Not Selected': 'grey'
    }

    colors = []
    for ticker in df_clean['Ticker']:
        in_sharpe = ticker in sharpe_list
        in_util = ticker in utility_list

        if in_sharpe and in_util:
            colors.append('purple')
        elif in_util:
            colors.append('orange')
        elif in_sharpe:
            colors.append('blue')
        else:
            colors.append('grey')

    plt.figure(figsize=(14, 8))  # wide for space on right

    scatter = plt.scatter(df_clean[std_col], df_clean[growth_col], c=colors, alpha=0.7)

    plt.xlabel('Standard Deviation (Risk %)')
    plt.ylabel('Annual Growth (%)')
    plt.title(title)
    plt.grid(True)

    # Plot user profile point
    plt.scatter(user_std, user_growth, color='red', s=100, edgecolor='black', label='User Profile')

    # Create legend handles
    patches = [mpatches.Patch(color=color, label=label) for label, color in labels_for_legend.items()]
    user_patch = plt.Line2D([0], [0], marker='o', color='w', label='User Profile',
                           markerfacecolor='red', markersize=10, markeredgecolor='black')
    patches.append(user_patch)

    # Put legend on the right (leave enough room)
    plt.legend(handles=patches, loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize=10)

    # Label selected ETFs (Sharpe, Utility, or Both)
    selected_mask = df_clean['Ticker'].isin(set(sharpe_list) | set(utility_list))
    selected_df = df_clean[selected_mask].sort_values(by=std_col).reset_index()

    # Smaller vertical offsets, or no offsets
    y_offsets = np.linspace(-0.15, 0.15, len(selected_df))  # tighter offsets for clarity

    for i, row in selected_df.iterrows():
        x = row[std_col]
        y = row[growth_col]
        ticker = row['Ticker']
        plt.text(x, y + y_offsets[i], ticker, fontsize=8, ha='left', va='center')

    # Create an inset axes below the plot for user profile
    # Move it closer by shifting bottom position up and reducing height
    inset_ax = plt.axes([0.1, 0.12, 0.75, 0.1])  # closer to plot, smaller height
    inset_ax.axis('off')  # hide axes

    profile_text = (
        f"User Profile:    Horizon: {time_horizon}y    Growth Goal: {user_growth}%    Std Dev: ±{user_std}%    "
        f"Max Drawdown: {user_max_drawdown}%    Min ETF Age: {user_min_etf_age}y    "
        f"Risk (Return:Risk): {user_risk_ratio[1]}:{user_risk_ratio[0]}"
    )
    inset_ax.text(0.01, 0.5, profile_text, fontsize=10, va='center', ha='left',
              bbox=dict(boxstyle="round,pad=0.5", facecolor="whitesmoke", edgecolor="gray", alpha=0.9))

    # Adjust layout to fit legend on right and user profile below
    plt.tight_layout(rect=[0, 0.15, 0.85, 1])  # less bottom padding for profile box, right for legend
    plt.savefig('etf_risk_return.png')
    plt.close() 
