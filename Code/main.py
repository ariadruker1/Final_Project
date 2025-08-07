'''
Aria Druker and Linghe Zhou
'''
import pandas as pd
from datetime import datetime
from ishares_ETF_list import download_valid_data
from user_profile import getUserProfile
from max_drawdown import calculate_max_drawdown
from Etf_Data import get_etf_data, filter_etf_data
from visualizing_etf_metrics import plot_risk_return_user
from risk_free_rates import fetch_risk_free_boc
from etf_recommendation_evaluation import top_5_recommend
from custom_score import utility_score
from recommendation_test import recommendation_test
from graph_performance import plot_annual_growth_rate
from compare_custom_Sharpe_test_results import quantitative_etf_basket_comparison
from sharpe_recommendation import sharpe_score

USER_TIME_HORIZON = 0
USER_DESIRED_GROWTH = 1
USER_FLUCTUATION = 2
USER_WORST_CASE = 3
USER_MINIMUM_ETF_AGE = 4
USER_RISK_PREFERENCE = 5

def main(): 
    valid_tickers, data = download_valid_data()
    user = getUserProfile()
    end_date = pd.Timestamp(datetime.now())
    # md_tolerable_list = calculate_max_drawdown(user[USER_WORST_CASE], user[USER_MINIMUM_ETF_AGE], valid_tickers, data, end_date)
    # etf_metrics = get_etf_data(md_tolerable_list, user[USER_TIME_HORIZON], data, end_date)
    # quadrant_ideal_etfs = filter_etf_data(etf_metrics, user[USER_DESIRED_GROWTH], user[USER_FLUCTUATION], user[USER_TIME_HORIZON])
    # risk_free_data = fetch_risk_free_boc("1995-01-01")
    # etf_utility_calculation = utility_score(quadrant_ideal_etfs, user[USER_TIME_HORIZON], risk_free_data, user[USER_RISK_PREFERENCE])
    # etf_utility_recommend = top_5_recommend(etf_utility_calculation, 'Utility_Score')
    # print(etf_utility_recommend)
    # plot_risk_return_user(quadrant_ideal_etfs, user[USER_DESIRED_GROWTH], user[USER_FLUCTUATION], user[USER_TIME_HORIZON], f'FULL DATA: ETF Risk-Return Space with User Profile (Time Horizon = {user[USER_TIME_HORIZON]}Y)')
    test_period = 2
    custom_recommended_list, sharpe_recommended_list = recommendation_test(
        user[USER_TIME_HORIZON], user[USER_DESIRED_GROWTH], user[USER_FLUCTUATION], 
        user[USER_WORST_CASE], user[USER_MINIMUM_ETF_AGE], user[USER_RISK_PREFERENCE], 
        valid_tickers, data, test_period
    )
    train_start = end_date - pd.DateOffset(years=test_period) - pd.DateOffset(years=user[USER_TIME_HORIZON])
    test_start = end_date - pd.DateOffset(years=test_period)
    results = quantitative_etf_basket_comparison(
        data, custom_recommended_list, sharpe_recommended_list, user[USER_DESIRED_GROWTH], 
        user[USER_FLUCTUATION], user[USER_RISK_PREFERENCE], test_start, end_date)
    print("COMPARISON:")
    print(results)
    (
        data, custom_recommended_list, sharpe_recommended_list, test_period, 
        user[USER_TIME_HORIZON], user[USER_DESIRED_GROWTH], user[USER_FLUCTUATION], 
        user[USER_WORST_CASE], user[USER_MINIMUM_ETF_AGE], user[USER_RISK_PREFERENCE]
    )
    plot_annual_growth_rate(
        data, 
        custom_recommended_list, 
        sharpe_recommended_list,
        test_period,
        user[USER_TIME_HORIZON],
        user[USER_DESIRED_GROWTH],
        user[USER_FLUCTUATION],
        user[USER_WORST_CASE],      # max drawdown
        user[USER_MINIMUM_ETF_AGE],
        user[USER_RISK_PREFERENCE]
    )

    print(f'Time_Horizon: {user[USER_TIME_HORIZON]}\nGrowth: {user[USER_DESIRED_GROWTH]}\nSTD: {user[USER_FLUCTUATION]}\nMax_Drawdown:'
          + f'{user[USER_WORST_CASE]}\nMin_ETF_Age: {user[USER_MINIMUM_ETF_AGE]}\nRisk_Return_Ratio: {user[USER_RISK_PREFERENCE]}\n')

main()