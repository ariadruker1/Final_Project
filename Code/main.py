'''
Aria Druker and Linghe Zhou

'''
import user_profile as up
import max_drawdown as md
import pandas as pd
from ishares_ETF_list import download_valid_data
from Etf_Data import get_etf_data, filter_etf_data
from datetime import datetime
from kdtree_nearest_5_etfs import kdtree_nearest_5_etfs
from visualizing_results import plot_etfs_with_user

NEAREST_NEIGHBOURS = 500
USER_TIME_HORIZON = 0
USER_DESIRED_GROWTH = 1
USER_FLUCTUATION = 2
USER_WORST_CASE = 3
USER_MINIMUM_ETF_AGE = 4


def main():
    user = up.getUserProfile()
    valid_tickers, data = download_valid_data()
    end_date = pd.Timestamp(datetime.now())
    md_tolerable_list = md.calculate_max_drawdown(
        user[USER_WORST_CASE], user[USER_MINIMUM_ETF_AGE], valid_tickers, data, end_date)
    annual_data = get_etf_data(
        md_tolerable_list, user[USER_TIME_HORIZON], data)
    filtered_data = filter_etf_data(
        annual_data, user[USER_DESIRED_GROWTH], user[USER_FLUCTUATION], user[USER_TIME_HORIZON])
    etf_distances = kdtree_nearest_5_etfs(
        user[USER_DESIRED_GROWTH], user[USER_FLUCTUATION], filtered_data, user[USER_TIME_HORIZON], NEAREST_NEIGHBOURS)
    print(etf_distances.head(NEAREST_NEIGHBOURS))
    print(f'Time_Horizon: {user[USER_TIME_HORIZON]}\nGrowth: {user[USER_DESIRED_GROWTH]}\nSTD: {user[USER_FLUCTUATION]}\nMax_Drawdown: {user[USER_WORST_CASE]}\nMin_ETF_Age: {user[USER_MINIMUM_ETF_AGE]}')
    plot_etfs_with_user(
        etf_distances, user[USER_DESIRED_GROWTH], user[USER_FLUCTUATION], user[USER_TIME_HORIZON])


main()
