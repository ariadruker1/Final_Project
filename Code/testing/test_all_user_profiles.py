from testing.compare_custom_Sharpe_test_results import quantitative_etf_basket_comparison
from testing.recommendation_test import recommendation_test
# if needed, override this with manual profiles
from core.user.user_profile import getUserProfile
from core.data_processing.ishares_ETF_list import download_valid_data
from datetime import datetime
import itertools
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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

    time_horizons = [15]
    growths = [2, 10, 21]
    stds = [5, 15, 60]
    max_drawdowns = [15, 35, 100]
    min_etf_ages = [3]
    risk_preferences = [[3, 1], [1, 1], [1, 3]]

    rows = []

    for combo in itertools.product(time_horizons, growths, stds, max_drawdowns, min_etf_ages, risk_preferences):
        user = list(combo)
        print(f"Processing combo: {combo}")

        try:
            custom_list, sharpe_list = recommendation_test(
                user[USER_TIME_HORIZON], user[USER_DESIRED_GROWTH], user[USER_FLUCTUATION],
                user[USER_WORST_CASE], user[USER_MINIMUM_ETF_AGE], user[USER_RISK_PREFERENCE],
                valid_tickers, data, test_period
            )

            print(
                f"Custom recommended ETFs (count {len(custom_list)}): {custom_list}")
            print(
                f"Sharpe recommended ETFs (count {len(sharpe_list)}): {sharpe_list}")

            if not custom_list or not sharpe_list:
                print("Skipping due to empty recommendation list")
                continue

            result_df = quantitative_etf_basket_comparison(
                data, custom_list, sharpe_list,
                user[USER_DESIRED_GROWTH], user[USER_FLUCTUATION], user[USER_RISK_PREFERENCE],
                test_start, end_date
            )

            print(f"Result DataFrame index labels: {result_df.index.tolist()}")

            # Ensure required rows exist
            if 'Sharpe' not in result_df.index or 'Custom' not in result_df.index:
                print("Skipping due to missing 'Sharpe' or 'Custom' in results")
                continue

            rows.append({
                "time_horizon": user[USER_TIME_HORIZON],
                "growth": user[USER_DESIRED_GROWTH],
                "fluctuation": user[USER_FLUCTUATION],
                "max_drawdown": user[USER_WORST_CASE],
                "min_etf_age": user[USER_MINIMUM_ETF_AGE],
                "risk_preference": user[USER_RISK_PREFERENCE],
                "sharpe_return": result_df.loc['Sharpe', 'Annual Return (%)'],
                "sharpe_reward_to_shortfall": result_df.loc['Sharpe', 'Reward to Shortfall'],
                "custom_return": result_df.loc['Custom', 'Annual Return (%)'],
                "custom_reward_to_shortfall": result_df.loc['Custom', 'Reward to Shortfall'],
            })

        except Exception as e:
            print(f"Failed on combo {combo}: {e}")
            continue

    if not rows:
        print("No valid data rows collected to write to Excel.")
    else:
        df = pd.DataFrame(rows)
        df.to_excel(
            '~/Desktop/all_users_etf_sharpe_custom_compare.xlsx', index=False)
        print(f"Saved results with {len(df)} rows to Excel.")

    return rows if rows else None


generate_all_user_tests()
