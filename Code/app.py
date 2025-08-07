import streamlit as st
import pandas as pd
from datetime import datetime
from ishares_ETF_list import download_valid_data
from max_drawdown import calculate_max_drawdown
from Etf_Data import get_etf_data, filter_etf_data
from visualizing_etf_metrics import plot_risk_return_user
from risk_free_rates import fetch_risk_free_boc
from etf_recommendation_evaluation import top_5_recommend
from custom_score import utility_score
from sharpe_recommendation import sharpe_score
from recommendation_test import recommendation_test
from chart_training_test_performances import plot_etf_performance_with_user_preferences
from compare_custom_Sharpe_test_results import quantitative_etf_basket_comparison

USER_TIME_HORIZON = 0
USER_DESIRED_GROWTH = 1
USER_FLUCTUATION = 2
USER_WORST_CASE = 3
USER_MINIMUM_ETF_AGE = 4
USER_RISK_PREFERENCE = 5

# # Set page config for dark theme
# st.set_page_config(
#     page_title="ETF Navigator",
#     page_icon="📈",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# # Custom CSS for financial dark theme
# st.markdown("""
# <style>
#     .stApp {
#         background-color: #0e1117;
#         color: #ffffff;
#     }

#     .main-header {
#         text-align: center;
#         color: #00d4aa;
#         font-size: 2.5rem;
#         font-weight: 700;
#         margin-bottom: 10px;
#         text-shadow: 0 0 10px rgba(0, 212, 170, 0.3);
#     }

#     .sub-text {
#         text-align: center;
#         color: #b8bcc8;
#         font-size: 1.1rem;
#         margin-bottom: 30px;
#     }

#     .question-container {
#         background: linear-gradient(135deg, #1e2329 0%, #2b2f36 100%);
#         padding: 30px;
#         border-radius: 15px;
#         border: 1px solid #00d4aa;
#         box-shadow: 0 8px 32px rgba(0, 212, 170, 0.1);
#         margin: 20px 0;
#     }

#     .question-title {
#         color: #00d4aa;
#         font-size: 1.4rem;
#         font-weight: 600;
#         margin-bottom: 15px;
#     }

#     .question-text {
#         color: #ffffff;
#         font-size: 1.2rem;
#         font-weight: 500;
#         margin-bottom: 20px;
#     }

#     .progress-text {
#         color: #b8bcc8;
#         text-align: center;
#         margin-bottom: 15px;
#         font-weight: 500;
#     }

#     .results-container {
#         background: linear-gradient(135deg, #1a1d29 0%, #2d3748 100%);
#         padding: 30px;
#         border-radius: 15px;
#         border: 2px solid #00d4aa;
#         box-shadow: 0 12px 48px rgba(0, 212, 170, 0.2);
#         margin: 20px 0;
#     }

#     .success-title {
#         color: #00d4aa;
#         font-size: 1.8rem;
#         font-weight: 700;
#         text-align: center;
#         margin-bottom: 20px;
#     }

#     /* Style the selectbox */
#     .stSelectbox > div > div {
#         background-color: #2b2f36;
#         border: 1px solid #00d4aa;
#         border-radius: 8px;
#         color: #ffffff;
#         font-size: 1.1rem;
#     }

#     .stSelectbox label {
#         color: #ffffff !important;
#         font-size: 1.2rem !important;
#         font-weight: 500 !important;
#     }

#     /* Style buttons */
#     .stButton > button {
#         background: linear-gradient(45deg, #00d4aa, #00a88f);
#         color: #ffffff;
#         border: none;
#         border-radius: 8px;
#         font-weight: 600;
#         padding: 10px 24px;
#         transition: all 0.3s ease;
#         font-size: 1rem;
#     }

#     .stButton > button:hover {
#         background: linear-gradient(45deg, #00a88f, #008f7a);
#         box-shadow: 0 4px 12px rgba(0, 212, 170, 0.3);
#         transform: translateY(-2px);
#     }

#     /* Progress bar styling */
#     .stProgress > div > div {
#         background: linear-gradient(90deg, #00d4aa, #00a88f);
#     }

#     /* DataFrames */
#     .stDataFrame {
#         background-color: #1e2329;
#         border: 1px solid #00d4aa;
#         border-radius: 8px;
#     }

#     /* Hide empty containers */
#     .element-container:has(.stProgress) + .element-container:empty {
#         display: none;
#     }
# </style>
# """, unsafe_allow_html=True)

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

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back", key="back2"):
            st.session_state.step = 1
            st.rerun()
    with col2:
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

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back", key="back3"):
            st.session_state.step = 2
            st.rerun()
    with col2:
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

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back", key="back4"):
            st.session_state.step = 3
            st.rerun()
    with col2:
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

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back", key="back5"):
            st.session_state.step = 4
            st.rerun()
    with col2:
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

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back", key="back6"):
            st.session_state.step = 5
            st.rerun()
    with col2:
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
            quadrant_ideal_etfs = filter_etf_data(
                etf_metrics, user[USER_DESIRED_GROWTH], user[USER_FLUCTUATION], user[USER_TIME_HORIZON])
            risk_free_data = fetch_risk_free_boc("1995-01-01")
            # etf_utility_calculation = utility_score(
            #     quadrant_ideal_etfs, user[USER_TIME_HORIZON], risk_free_data, user[USER_RISK_PREFERENCE])
            # etf_utility_recommend = top_5_recommend(
            #     etf_utility_calculation, 'Utility_Score')
            etf_sharpe_calculation = sharpe_score(
                quadrant_ideal_etfs, user[USER_TIME_HORIZON], risk_free_data)
            etf_sharpe_recommend = top_5_recommend(
                etf_sharpe_calculation, 'Sharpe')

            st.success("✅ Analysis complete!")
            st.dataframe(etf_sharpe_recommend, use_container_width=True)

            if st.button("Start Over", key="restart"):
                # Reset session state
                st.session_state.step = 1
                st.session_state.user_profile = [None] * 6
                st.rerun()

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            if st.button("Try Again", key="retry"):
                st.session_state.step = 1
                st.rerun()
