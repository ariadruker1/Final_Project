import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.constants import (
    TESTING_PERIOD, RECOMMENDATION_COUNT
)
from core.analysis.max_drawdown import calculate_max_drawdown
from core.data_processing.Etf_Data import get_etf_data
from core.data_processing.risk_free_rates import fetch_risk_free_boc
from core.scoring.etf_recommendation_evaluation import top_recommend
from core.scoring.custom_score import utility_score
from core.scoring.sharpe_recommendation import sharpe_score


def recommendation_test(
    time_horizon, growth, fluctuation, worst_case, min_age, risk_preference, valid_tickers, data, test_period
):
    """
    Generate ETF recommendations based on a training period and return lists of top ETFs
    and their performance metrics.

    Args:
        time_horizon (int): time horizon in years
        growth (float): user desired growth rate
        fluctuation (float): user allowed std deviation
        worst_case (float): maximum drawdown allowed
        min_age (int): minimum ETF age in years
        risk_preference (list): risk preference weights [reward_weight, risk_weight]
        valid_tickers (list): available ETFs
        data (pd.DataFrame): price data
        test_period (int): length of test period in years

    Returns:
        tuple: (custom_recommended_list, sharpe_recommended_list, custom_metrics, sharpe_metrics)
        custom_metrics and sharpe_metrics are dictionaries containing
        'Annual Return (%)' and 'Volatility (%)'.
    """
    today = pd.Timestamp(datetime.now())
    train_end = today - pd.DateOffset(years=test_period)
    
    md_tolerable_list = calculate_max_drawdown(worst_case, min_age, valid_tickers, data, train_end)
    etf_metrics = get_etf_data(md_tolerable_list, time_horizon, data, train_end)
    risk_free_data = fetch_risk_free_boc("1995-01-01")

    if etf_metrics.empty:
        return [], [], {'Annual Return (%)': None, 'Volatility (%)': None}, {'Annual Return (%)': None, 'Volatility (%)': None}

    etf_utility_calculation = utility_score(etf_metrics, time_horizon, risk_free_data, risk_preference)
    sharpe_scoring_calculation = sharpe_score(etf_metrics, time_horizon, risk_free_data)

    custom_clean = etf_utility_calculation.dropna(subset=['Utility_Score'])
    sharpe_clean = sharpe_scoring_calculation.dropna(subset=['Sharpe'])
    
    custom_recommended_df = top_recommend(custom_clean, 'Utility_Score', RECOMMENDATION_COUNT)
    sharpe_recommended_df = top_recommend(sharpe_clean, 'Sharpe', RECOMMENDATION_COUNT)

    custom_recommended_list = custom_recommended_df['Ticker'].tolist() if not custom_recommended_df.empty else []
    sharpe_recommended_list = sharpe_recommended_df['Ticker'].tolist() if not sharpe_recommended_df.empty else []
    
    # Dynamically construct column names based on the time_horizon
    annual_growth_col = f"Annual_Growth_{time_horizon}Y"
    std_dev_col = f"Standard_Deviation_{time_horizon}Y"

    custom_metrics = {
        'Annual Return (%)': custom_recommended_df[annual_growth_col].mean() if not custom_recommended_df.empty else None,
        'Volatility (%)': custom_recommended_df[std_dev_col].mean() if not custom_recommended_df.empty else None
    }
    sharpe_metrics = {
        'Annual Return (%)': sharpe_recommended_df[annual_growth_col].mean() if not sharpe_recommended_df.empty else None,
        'Volatility (%)': sharpe_recommended_df[std_dev_col].mean() if not sharpe_recommended_df.empty else None
    }

    return custom_recommended_list, sharpe_recommended_list, custom_metrics, sharpe_metrics