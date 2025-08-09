import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scoring.sharpe_recommendation import sharpe_score
from core.scoring.custom_score import utility_score
from core.scoring.etf_recommendation_evaluation import top_5_recommend
from core.data_processing.risk_free_rates import fetch_risk_free_boc
from visualization.visualizing_etf_metrics import plot_risk_return_user
from core.data_processing.Etf_Data import get_etf_data, filter_etf_data
from core.analysis.max_drawdown import calculate_max_drawdown
from datetime import datetime
import pandas as pd


def recommendation_test(
    time_horizon, desired_growth, std_deviation, max_drawdown,
    minimum_etf_age, risk_preference, valid_tickers, data, test_period
):
    """
    Generate ETF recommendations based on training period,
    then return lists of top ETFs by custom utility score and Sharpe ratio.

    Args:
        time_horizon (int): time horizon in years
        desired_growth (float): user desired growth rate
        std_deviation (float): user allowed std deviation
        max_drawdown (float): maximum drawdown allowed
        minimum_etf_age (int): minimum ETF age in years
        risk_preference (list): risk preference weights [reward_weight, risk_weight]
        valid_tickers (list): available ETFs
        data (pd.DataFrame): price data
        test_period (int): length of test period in years

    Returns:
        tuple: (custom_recommended_list, sharpe_recommended_list)
    """
    today = pd.Timestamp(datetime.now())
    train_end = today - pd.DateOffset(years=test_period)

    md_tolerable_list = calculate_max_drawdown(
        max_drawdown, minimum_etf_age, valid_tickers, data, train_end)
    etf_metrics = get_etf_data(
        md_tolerable_list, time_horizon, data, train_end)
    risk_free_data = fetch_risk_free_boc("1995-01-01")

    etf_utility_calculation = utility_score(
        etf_metrics, time_horizon, risk_free_data, risk_preference)

    if 'Utility_Score' in etf_utility_calculation.columns:
        custom_clean = etf_utility_calculation.dropna(subset=['Utility_Score'])
        custom_recommended_list = top_5_recommend(custom_clean, 'Utility_Score')[
            'Ticker'].tolist() if not custom_clean.empty else []
    else:
        custom_recommended_list = []

    sharpe_scoring_calculation = sharpe_score(
        etf_metrics, time_horizon, risk_free_data)

    if 'Sharpe' in sharpe_scoring_calculation.columns:
        sharpe_clean = sharpe_scoring_calculation.dropna(subset=['Sharpe'])
        sharpe_recommended_list = top_5_recommend(sharpe_clean, 'Sharpe')[
            'Ticker'].tolist() if not sharpe_clean.empty else []
    else:
        sharpe_recommended_list = []

    return custom_recommended_list, sharpe_recommended_list
