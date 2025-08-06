import pandas as pd
from datetime import datetime
from user_profile import getUserProfile
from max_drawdown import calculate_max_drawdown
from Etf_Data import get_etf_data, filter_etf_data
from visualizing_etf_metrics import plot_risk_return_user
from risk_free_rates import fetch_risk_free_boc
from etf_recommendation_evaluation import top_5_recommend
from custom_score import utility_score
from sharpe_recommendation import sharpe_score

def recommendation_test(
    time_horizon, desired_growth, std_deviation, max_drawdown, 
    minimum_etf_age, risk_preference, valid_tickers, data, test_period
):
    """
    Generate ETF recommendations based on training period,
    then plot ETF performance over training+test with user prefs.

    Args:
        user (list): user profile parameters.
        valid_tickers (list): available ETFs.
        data (pd.DataFrame): price data.
        test_period (int): length of test period in years.
    """
    today = pd.Timestamp(datetime.now())

    # Define date boundaries for training and test periods
    train_end = today - pd.DateOffset(years=test_period)

    # Filter ETFs based on max drawdown and minimum age as of train_end
    md_tolerable_list = calculate_max_drawdown(max_drawdown, minimum_etf_age, valid_tickers, data, train_end)

    # Calculate ETF metrics based on training data only
    etf_metrics = get_etf_data(md_tolerable_list, time_horizon, data, train_end)
    quadrant_ideal_etfs = filter_etf_data(etf_metrics, desired_growth, std_deviation, time_horizon)
    risk_free_data = fetch_risk_free_boc("1995-01-01")

    # Calculate utility scores based on training metrics
    etf_utility_calculation = utility_score(quadrant_ideal_etfs, time_horizon, risk_free_data, risk_preference)
    print("CUSTOM 5 Selected data:")
    print(etf_utility_calculation.head(5))
    # Select top 5 ETFs by Utility_Score
    custom_recommended_list = top_5_recommend(etf_utility_calculation, 'Utility_Score')['Ticker'].tolist()

    # Calculate sharpe scores
    sharpe_scoring_calculation = sharpe_score(etf_metrics, time_horizon,risk_free_data)
    print("\nSHARPE 5 Selected data:")
    print(sharpe_scoring_calculation.head(5))
    # Calculate and recommend 5 ETFs based on Sharpe Ratio
    sharpe_recommended_list = top_5_recommend(sharpe_scoring_calculation, 'Sharpe')['Ticker'].tolist()

    print("CUSTOM Recommended ETFs based on training data:")
    print(custom_recommended_list)
    print("SHARPE Recommended ETFs based on training data:")
    print(sharpe_recommended_list)
    plot_risk_return_user(quadrant_ideal_etfs, desired_growth, std_deviation, time_horizon, f'TRAINING TIME: ETF Risk-Return Space with User Profile (Time Horizon = {time_horizon}Y)')

    return custom_recommended_list, sharpe_recommended_list
