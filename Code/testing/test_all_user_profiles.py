import sys
import os
# Add project root to sys.path for imports to work
# Corrected path to add the 'Code' directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Reverted to absolute imports, which work with the sys.path modification
from testing.compare_custom_Sharpe_test_results import quantitative_etf_basket_comparison
from testing.recommendation_test import recommendation_test

from core.user.user_profile import getUserProfile
from core.data_processing.ishares_ETF_list import download_valid_data
from core.data_processing.risk_free_rates import fetch_risk_free_boc

from datetime import datetime
import itertools
import pandas as pd

# Constants for index access
USER_TIME_HORIZON = 0
USER_DESIRED_GROWTH = 1
USER_FLUCTUATION = 2
USER_WORST_CASE = 3
USER_MINIMUM_ETF_AGE = 4
USER_RISK_PREFERENCE = 5


def generate_all_user_tests():
    valid_tickers, data = download_valid_data()
    end_date = pd.Timestamp(datetime.now())
    test_period = 1
    test_start = end_date - pd.DateOffset(years=test_period)

    time_horizons = [10]
    growths = [2, 21]
    stds = [5, 35]
    max_drawdowns = [15, 35, 100]
    min_etf_ages = [3]
    risk_preferences = [[3, 1], [1, 1], [1, 3]]

    rows = []

    for combo in itertools.product(time_horizons, growths, stds, max_drawdowns, min_etf_ages, risk_preferences):
        user = list(combo)
        print(f"Processing combo: {combo}")

        try:
            # Get recommended tickers
            custom_list, sharpe_list = recommendation_test(
                user[USER_TIME_HORIZON], user[USER_DESIRED_GROWTH], user[USER_FLUCTUATION],
                user[USER_WORST_CASE], user[USER_MINIMUM_ETF_AGE], user[USER_RISK_PREFERENCE],
                valid_tickers, data, test_period
            )

            print(f"Custom recommended ETFs ({len(custom_list)}): {custom_list}")
            print(f"Sharpe recommended ETFs ({len(sharpe_list)}): {sharpe_list}")

            if not custom_list or not sharpe_list:
                print("Skipping due to empty recommendation list")
                continue

            # Get performance metrics
            risk_free_data = fetch_risk_free_boc("1995-01-01")
            result_df = quantitative_etf_basket_comparison(
                data, custom_list, sharpe_list,
                user[USER_DESIRED_GROWTH], user[USER_FLUCTUATION],
                test_start, end_date, risk_free_data['yield_pct'].mean()
            )

            if 'Sharpe' not in result_df.index or 'Custom' not in result_df.index:
                print("Skipping due to missing Sharpe or Custom in results")
                continue

            # Extract overlap info from Custom row (same for both methods)
            overlap_info = {
                "Unique Custom ETFs": ', '.join(map(str, result_df.loc['Custom', 'Unique Custom ETFs'])),
                "Unique Sharpe ETFs": ', '.join(map(str, result_df.loc['Custom', 'Unique Sharpe ETFs'])),
                "Overlapping ETFs": ', '.join(map(str, result_df.loc['Custom', 'Overlapping ETFs'])),
                "Overlap Count": result_df.loc['Custom', 'Overlap Count']
            }

            # Flatten Sharpe & Custom metrics
            sharpe_metrics = {f"Sharpe_{col}": result_df.loc['Sharpe', col] for col in result_df.columns if col not in overlap_info}
            custom_metrics = {f"Custom_{col}": result_df.loc['Custom', col] for col in result_df.columns if col not in overlap_info}

            # Ensure list-like metrics inside Sharpe/Custom are stringified
            for metrics in (sharpe_metrics, custom_metrics):
                for k, v in metrics.items():
                    if isinstance(v, (list, set)):
                        metrics[k] = ', '.join(map(str, v))

            # Combine all into one row
            combined_row = {
                "time_horizon": user[USER_TIME_HORIZON],
                "growth": user[USER_DESIRED_GROWTH],
                "fluctuation": user[USER_FLUCTUATION],
                "max_drawdown": user[USER_WORST_CASE],
                "min_etf_age": user[USER_MINIMUM_ETF_AGE],
                "risk_preference": user[USER_RISK_PREFERENCE],
            }
            combined_row.update(sharpe_metrics)
            combined_row.update(custom_metrics)
            combined_row.update(overlap_info)

            rows.append(combined_row)

        except Exception as e:
            print(f"Failed on combo {combo}: {e}")
            continue

    if not rows:
        print("No valid data rows collected to write to Excel.")
        return None

    df = pd.DataFrame(rows)
    df.to_excel('~/Desktop/all_users_etf_sharpe_custom_compare_full.xlsx', index=False)
    print(f"Saved results with {len(df)} rows to Excel.")
    return df


if __name__ == "__main__":
    generate_all_user_tests()
