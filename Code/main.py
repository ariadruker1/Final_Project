'''
Aria Druker and Linghe Zhou

'''
import user_profile as up
import max_drawdown as md
import pandas as pd
from ishares_ETF_list import download_valid_data
from Etf_Data import get_etf_data
from datetime import datetime
from kdtree_nearest_5_etfs import kdtree_nearest_5_etfs

NEAREST_NEIGHBOURS = 5


def main(): 
    user = up.getUserProfile()
    valid_tickers, data = download_valid_data()
    end_date = pd.Timestamp(datetime.now())
    md_tolerable_list = md.calculate_max_drawdown(user[3], user[4], valid_tickers, data, end_date)
    annual_data = get_etf_data(md_tolerable_list, user[0], data)
    etf_distances = kdtree_nearest_5_etfs(user[1], user[2], annual_data, user[0], NEAREST_NEIGHBOURS)
    print(etf_distances.head(5))
    print(f'Time_Horizon: {user[0]}\nGrowth: {user[1]}\nSTD: {user[2]}\nMax_Drawdown: {user[3]}\nMin_ETF_Age: {user[4]}')
main()