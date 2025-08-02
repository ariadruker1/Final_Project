'''
Aria Druker and Linghe Zhou

'''
import user_profile as up
import max_drawdown as md
import pandas as pd
from ishares_ETF_list import download_valid_data
from Etf_Data import get_etf_data
from datetime import datetime

def main():
    user = up.getUserProfile()
    valid_tickers, data = download_valid_data()
    end_date = pd.Timestamp(datetime.now())
    md_tolerable_list = md.calculate_max_drawdown(user[3], user[4], valid_tickers, data, end_date)
    annual_data = get_etf_data(valid_tickers, user[0], md_tolerable_list, data)
    print(annual_data)
main()