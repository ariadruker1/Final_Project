# keep these 3 lines at the top of the file
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.data_processing.ishares_ETF_list import download_valid_data
from core.data_processing.Etf_Data import get_etf_data, filter_etf_data
from core.analysis.max_drawdown import calculate_max_drawdown
from core.scoring.etf_recommendation_evaluation import top_5_recommend
from core.scoring.utility_score import utility_score
from core.scoring.sharpe_recommendation import sharpe_score
from core.data_processing.risk_free_rates import fetch_risk_free_boc
from testing.recommendation_test import recommendation_test
from testing.compare_custom_Sharpe_test_results import quantitative_etf_basket_comparison
from visualization.chart_training_test_performances import plot_etf_performance_with_user_preferences
from config.constants import (
    USER_TIME_HORIZON, USER_DESIRED_GROWTH, USER_FLUCTUATION,
    USER_WORST_CASE, USER_MINIMUM_ETF_AGE, USER_RISK_PREFERENCE,
    TIME_HORIZON_OPTIONS, DESIRED_GROWTH_OPTIONS, FLUCTUATION_OPTIONS,
    WORSE_CASE_OPTIONS, MINIMUM_ETF_AGE_OPTIONS, RISK_PREFERENCE_OPTIONS
)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


def create_etf_performance_chart(etf_recommend_df, data, time_horizon, chart_title):
    """
    Create a simple interactive line chart showing ETF performance over time
    """
    # Get the recommended ETF tickers
    etf_tickers = etf_recommend_df['Ticker'].tolist()

    # Calculate start and end dates
    end_date = pd.Timestamp(datetime.now())
    start_date = end_date - pd.DateOffset(years=time_horizon)

    # Create the plotly figure
    fig = go.Figure()

    for ticker in etf_tickers:
        try:
            # Get price data for this ETF - fix the column access issue
            try:
                price_series = data[(ticker, 'Adj Close')].dropna()
            except (KeyError, TypeError):
                try:
                    price_series = data[ticker].dropna()
                except (KeyError, TypeError):
                    # Skip ETFs with missing price data
                    continue

            # Filter to the time horizon
            period_prices = price_series.loc[start_date:end_date]
            if period_prices.empty:
                continue

            # Normalize to start at 100 for better comparison
            normalized_prices = 100 * period_prices / period_prices.iloc[0]

            # Get metrics for this ETF
            etf_metrics = etf_recommend_df[etf_recommend_df['Ticker']
                                           == ticker].iloc[0]

            # Create hover text with only requested metrics
            growth_col = f'Annual_Growth_{time_horizon}Y'
            std_col = f'Standard_Deviation_{time_horizon}Y'

            hover_text = []
            for date, price in zip(normalized_prices.index, normalized_prices.values):
                hover_text.append(
                    f"<b>{ticker}</b><br>" +
                    f"Date: {date.strftime('%Y-%m-%d')}<br>" +
                    f"Annual Growth: {etf_metrics[growth_col]:.2f}%<br>" +
                    f"Standard Deviation: {etf_metrics[std_col]:.2f}%"
                )

            # Add trace for this ETF
            fig.add_trace(go.Scatter(
                x=normalized_prices.index,
                y=normalized_prices.values,
                mode='lines',
                name=ticker,
                line=dict(width=2),
                hovertemplate='%{text}<extra></extra>',
                text=hover_text
            ))

        except Exception as e:
            # Skip ETFs that can't be processed
            continue

    # Simple layout
    fig.update_layout(
        title=chart_title,
        xaxis_title="Date",
        yaxis_title="Normalized Price",
        hovermode='closest',
        height=400
    )

    return fig


# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = [None] * 6

st.title("ETF Recommendations")
st.write("Answer a few questions to get personalized ETF recommendations.")

# Define options
time_horizon_options = [1, 4, 8, 15, 25]
desired_growth_options = [2, 5, 10, 16, 21]
fluctuation_options = [5, 10, 15, 20, 60]
worse_case_options = [15, 25, 35, 45, 100]
minimum_etf_age = [10, 5, 3, 1, 0]
risk_preference = [[3, 1], [2, 1], [1, 1], [1, 2], [1, 3]]

# Progress bar (only show for questions 1-6)
if st.session_state.step <= 6:
    progress = (st.session_state.step - 1) / 6
    st.progress(progress)
    st.write(f"Question {st.session_state.step} of 6")

if st.session_state.step == 1:
    st.subheader("Time Horizon")
    choice = st.selectbox(
        "What is your investment time horizon?",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {
            1: "0-2 years",
            2: "3-5 years",
            3: "6-10 years",
            4: "11-20 years",
            5: "20+ years"
        }[x],
        key="q1"
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:  # Center column for single button
        if st.button("Next", key="next1"):
            st.session_state.user_profile[USER_TIME_HORIZON] = time_horizon_options[choice - 1]
            st.session_state.step = 2
            st.rerun()

elif st.session_state.step == 2:
    st.subheader("Growth Goals")
    choice = st.selectbox(
        "What are your annual growth goals?",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {
            1: "Beat inflation (<3%)",
            2: "Modest and reliable (3-7%)",
            3: "Steady longterm (8-12%)",
            4: "Strong returns with moderate risk (13-20%)",
            5: "High growth with greater risk (>20%+)"
        }[x],
        key="q2"
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Back", key="back2"):
            st.session_state.step = 1
            st.rerun()
    with col3:
        if st.button("Next", key="next2"):
            st.session_state.user_profile[USER_DESIRED_GROWTH] = desired_growth_options[choice - 1]
            st.session_state.step = 3
            st.rerun()

elif st.session_state.step == 3:
    st.subheader("Risk Tolerance")
    choice = st.selectbox(
        "How much annual fluctuation can you tolerate?",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {
            1: "Not much at all (<5%)",
            2: "Small ups and downs are okay (<10%)",
            3: "Regular market swings (<15%)",
            4: "I can handle large moves if it promotes growth (<20%)",
            5: "Volatility doesn't bother me (>20%)"
        }[x],
        key="q3"
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Back", key="back3"):
            st.session_state.step = 2
            st.rerun()
    with col3:
        if st.button("Next", key="next3"):
            st.session_state.user_profile[USER_FLUCTUATION] = fluctuation_options[choice - 1]
            st.session_state.step = 4
            st.rerun()

elif st.session_state.step == 4:
    st.subheader("Maximum Loss Tolerance")
    choice = st.selectbox(
        "In the worst case, what is the greatest loss you could tolerate?",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {
            1: "Low (<15%)",
            2: "Minor (<25%)",
            3: "Moderate (<35%)",
            4: "High (<45%)",
            5: "Very high (>45%)"
        }[x],
        key="q4"
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Back", key="back4"):
            st.session_state.step = 3
            st.rerun()
    with col3:
        if st.button("Next", key="next4"):
            st.session_state.user_profile[USER_WORST_CASE] = worse_case_options[choice - 1]
            st.session_state.step = 5
            st.rerun()

elif st.session_state.step == 5:
    st.subheader("ETF Track Record")
    choice = st.selectbox(
        "What is the minimum time you'd like the ETF to have existed?",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {
            1: "Very Established (>10 years)",
            2: "Experienced some variation (>5 years)",
            3: "Newer is okay (>3 years)",
            4: "I don't mind less data (>1 year)",
            5: "I want all options (up to present)"
        }[x],
        key="q5"
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Back", key="back5"):
            st.session_state.step = 4
            st.rerun()
    with col3:
        if st.button("Next", key="next5"):
            st.session_state.user_profile[USER_MINIMUM_ETF_AGE] = minimum_etf_age[choice - 1]
            st.session_state.step = 6
            st.rerun()

elif st.session_state.step == 6:
    st.subheader("Risk vs Return Preference")
    choice = st.selectbox(
        "How would you rate your preference for risk vs return?",
        options=[1, 2, 3, 4, 5],
        format_func=lambda x: {
            1: "Risk Averse (3:1)",
            2: "Risk Conscious (2:1)",
            3: "Balanced (1:1)",
            4: "Returns Prioritized (1:2)",
            5: "Return Focused (1:3)"
        }[x],
        key="q6"
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Back", key="back6"):
            st.session_state.step = 5
            st.rerun()
    with col3:
        if st.button("Get My Recommendations", key="final", type="primary"):
            st.session_state.user_profile[USER_RISK_PREFERENCE] = risk_preference[choice - 1]
            st.session_state.step = 7
            st.rerun()

elif st.session_state.step == 7:
    st.subheader("🎯 Your Personalized ETF Recommendations")

    with st.spinner("Generating your recommendations..."):
        try:
            user = st.session_state.user_profile

            valid_tickers, data = download_valid_data()
            end_date = pd.Timestamp(datetime.now())
            md_tolerable_list = calculate_max_drawdown(
                user[USER_WORST_CASE],
                user[USER_MINIMUM_ETF_AGE],
                valid_tickers,
                data,
                end_date
            )
            etf_metrics = get_etf_data(
                md_tolerable_list, user[USER_TIME_HORIZON], data, end_date)
            risk_free_data = fetch_risk_free_boc("1995-01-01")

            # Calculate both Sharpe and Utility recommendations
            etf_sharpe_calculation = sharpe_score(
                etf_metrics, user[USER_TIME_HORIZON], risk_free_data)
            etf_sharpe_recommend = top_5_recommend(
                etf_sharpe_calculation, 'Sharpe')

            etf_utility_calculation = utility_score(
                etf_metrics, user[USER_TIME_HORIZON], risk_free_data, user[USER_RISK_PREFERENCE])
            etf_utility_recommend = top_5_recommend(
                etf_utility_calculation, 'Utility_Score')

            st.success("✅ Analysis complete!")

            # Create two columns for side-by-side charts
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📈 Sharpe Ratio Based")
                if not etf_sharpe_recommend.empty:
                    sharpe_chart = create_etf_performance_chart(
                        etf_sharpe_recommend,
                        data,
                        user[USER_TIME_HORIZON],
                        f"Top 5 ETFs by Sharpe Ratio ({user[USER_TIME_HORIZON]} Years)"
                    )
                    st.plotly_chart(sharpe_chart, use_container_width=True)
                else:
                    st.warning("No Sharpe-based ETFs found.")

            with col2:
                st.subheader("⚖️ Utility Score Based")
                if not etf_utility_recommend.empty:
                    utility_chart = create_etf_performance_chart(
                        etf_utility_recommend,
                        data,
                        user[USER_TIME_HORIZON],
                        f"Top 5 ETFs by Utility Score ({user[USER_TIME_HORIZON]} Years)"
                    )
                    st.plotly_chart(utility_chart, use_container_width=True)
                else:
                    st.warning("No Utility-based ETFs found.")

            # Show simplified metrics tables below
            st.subheader("📊 Detailed Metrics Comparison")

            # Create simplified dataframes with only requested columns
            growth_col = f'Annual_Growth_{user[USER_TIME_HORIZON]}Y'
            std_col = f'Standard_Deviation_{user[USER_TIME_HORIZON]}Y'

            col1, col2 = st.columns(2)
            with col1:
                st.write("**Sharpe Ratio Recommendations:**")
                if not etf_sharpe_recommend.empty:
                    sharpe_simple = etf_sharpe_recommend[[
                        'Ticker', growth_col, std_col]].reset_index(drop=True)
                    sharpe_simple.columns = [
                        'Ticker', 'Annual Growth (%)', 'Standard Deviation (%)']
                    st.dataframe(
                        sharpe_simple, use_container_width=True, hide_index=True)
                else:
                    st.write("No data available")

            with col2:
                st.write("**Utility Score Recommendations:**")
                if not etf_utility_recommend.empty:
                    utility_simple = etf_utility_recommend[[
                        'Ticker', growth_col, std_col]].reset_index(drop=True)
                    utility_simple.columns = [
                        'Ticker', 'Annual Growth (%)', 'Standard Deviation (%)']
                    st.dataframe(utility_simple,
                                 use_container_width=True, hide_index=True)
                else:
                    st.write("No data available")

            if st.button("Start Over", key="restart"):
                st.session_state.step = 1
                st.session_state.user_profile = [None] * 6
                st.rerun()

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            if st.button("Try Again", key="retry"):
                st.session_state.step = 1
                st.rerun()
