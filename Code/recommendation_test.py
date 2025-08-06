import pandas as pd
from datetime import datetime
from risk_free_rates import fetch_risk_free_boc
from Etf_Data import get_etf_data
from etf_recommend import top_5_recommend
from utility_score import utility_score
from max_drawdown import calculate_max_drawdown
from plot_select_performance import plot_etf_performance_with_user_preferences

def recommendation_test(user, valid_tickers, data, test_period):
    """
    Generate ETF recommendations based on training period,
    then plot ETF performance over training+test with user prefs.

    Args:
        user (list): user profile parameters.
        valid_tickers (list): available ETFs.
        data (pd.DataFrame): price data.
        test_period (int): length of test period in years.
    """
    time_horizon = user[0]
    desired_growth = user[1]
    std_deviation = user[2]
    max_drawdown = user[3]
    minimum_etf_age = user[4]
    risk_preference = user[5]

    today = pd.Timestamp(datetime.now())

    # Define date boundaries for training and test periods
    train_start = today - pd.DateOffset(years=time_horizon + test_period)
    train_end = today - pd.DateOffset(years=test_period)
    test_start = train_end
    test_end = today

    # Filter ETFs based on max drawdown and minimum age as of train_end
    md_tolerable_list = calculate_max_drawdown(max_drawdown, minimum_etf_age, valid_tickers, data, train_end)

    # Calculate ETF metrics based on training data only
    etf_metrics = get_etf_data(md_tolerable_list, time_horizon, data, train_end)
    risk_free_data = fetch_risk_free_boc("1995-01-01")

    # Calculate utility scores based on training metrics
    etf_utility_calculation = utility_score(etf_metrics, time_horizon, risk_free_data, risk_preference)

    # Select top 5 ETFs by Utility_Score
    etf_recommended_list = top_5_recommend(etf_utility_calculation, 'Utility_Score')['Ticker'].tolist()

    print("Recommended ETFs based on training data:")
    print(etf_recommended_list)

    # Plot ETF normalized prices over training + test periods with user prefs
    plot_etf_performance_with_user_preferences(
        data, etf_recommended_list, train_start, train_end, test_start, test_end, time_horizon,
        desired_growth, std_deviation, max_drawdown, minimum_etf_age, risk_preference
    )
