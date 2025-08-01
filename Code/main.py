'''
Aria Druker and Linghe Zhou

'''
import user_profile as up
import max_drawdown as md
from ishares_ETF_list import download_valid_data
from Etf_Data import get_etf_data

def main():
    user = up.getUserProfile()
    valid_tickers, data = download_valid_data()
    md_tolerable_list = md.calculate_max_drawdown(user[3], valid_tickers, data)
    for ticker in md_tolerable_list:
        print(ticker, data[ticker]['Close'].dropna().tail())
    annual_data = get_etf_data(valid_tickers, user[0], md_tolerable_list, data)
    print(annual_data)
main()