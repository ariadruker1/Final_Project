'''
Aria Druker and Linghe Zhou

'''

import user_profile as up
import max_drawdown as md
import pandas as pd
from ishares_ETF_list import download_valid_data
from Etf_Data import get_etf_data, filter_etf_data

from datetime import datetime
import pandas as pd
from kdtree_nearest_5_etfs import kdtree_nearest_5_etfs
from visualizing_results import plot_etfs_with_user
from risk_free_rates import fetch_risk_free_boc
from ishares_ETF_list import download_valid_data
from Etf_Data import get_etf_data
from etf_recommend import top_5_recommend
from utility_score import utility_score
from recommendation_test import plot_etf_performance_with_user_preferences
from recommendation_test import recommendation_test
from user_profile import getUserProfile
from max_drawdown import calculate_max_drawdown

NEAREST_NEIGHBOURS = 500
USER_TIME_HORIZON = 0
USER_DESIRED_GROWTH = 1
USER_FLUCTUATION = 2
USER_WORST_CASE = 3
USER_MINIMUM_ETF_AGE = 4


def main(): 
    user = getUserProfile()
    time_horizon = user[0]
    desired_growth = user[1]
    std_deviation = user[2]
    max_drawdown = user[3]
    minimum_etf_age = user[4]
    risk_preference = user[5]

    valid_tickers, data = download_valid_data()
    end_date = pd.Timestamp(datetime.now())
    md_tolerable_list = calculate_max_drawdown(max_drawdown, minimum_etf_age, valid_tickers, data, end_date)
    etf_metrics = get_etf_data(md_tolerable_list, time_horizon, data, end_date)
    risk_free_data = fetch_risk_free_boc("1995-01-01")
    etf_utility_calculation = utility_score(etf_metrics, time_horizon, risk_free_data, risk_preference)
    etf_utility_recommend = top_5_recommend(etf_utility_calculation, 'Utility_Score')
    print(etf_utility_recommend)
    nearest = kdtree_nearest_5_etfs(user[1], user[2], etf_metrics, user[0], NEAREST_NEIGHBOURS)
    plot_etfs_with_user(etf_metrics, user[1], user[2], user[0])
    test_period = 3
    train_start = end_date - pd.DateOffset(years=time_horizon) - pd.DateOffset(years=test_period)
    train_end = end_date - pd.DateOffset(years=time_horizon)
    test_start = train_end
    test_end = end_date
    plot_etf_performance_with_user_preferences(
        data, nearest.head(5)["Ticker"].tolist(), train_start, train_end, test_start, test_end, time_horizon,
        desired_growth, std_deviation, max_drawdown, minimum_etf_age, risk_preference
    )
    recommendation_test(user, valid_tickers, data, test_period)
    # plot_etf_performance_with_user_preferences(data, valid_tickers, train_start, train_end, test_start, test_end, desired_growth, std_deviation)
    print(f'Time_Horizon: {user[0]}\nGrowth: {user[1]}\nSTD: {user[2]}\nMax_Drawdown: {user[3]}\nMin_ETF_Age: {user[4]}')
    plot_etfs_with_user(
        etf_distances, user[USER_DESIRED_GROWTH], user[USER_FLUCTUATION], user[USER_TIME_HORIZON])

main()