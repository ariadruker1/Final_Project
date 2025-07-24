'''
Asks user to build financial goal profile
'''

def getUserProfile():
    time_horizon_selected = 0
    # uses the average of each range - will be time window for averaging and comparing ETFs
    time_horizon_options = [1, 4, 8, 15, 25]
    user_time_horizon = 0

    desired_growth_selected = 0
    # uses the average % as goal
    desired_growth_options = [2, 4, 6, 8, 11]
    user_desired_growth = 0

    fluctuation_selected = 0
    # uses the maximum acceptable variance (will be compared to daily standard deviation)
    fluctuation_options = [1, 3, 5, 8, 100]
    user_fluctuation = 0

    worst_case_selected = 0
    # uses the maximum for tolerance of drawdown
    worse_case_options = [5, 10, 20, 35, 100]
    user_worst_case = 0

    print("\nHello and welcome to ETF Navigator!\nPlease answer the following questions so we can suggest 5 ETFs we think would fit well with your financial goals.")
    while time_horizon_selected== 0 or desired_growth_selected == 0 or fluctuation_selected== 0 or worst_case_selected== 0:
        try:
            while time_horizon_selected!= 1 and time_horizon_selected!= 2 and time_horizon_selected!= 3 and time_horizon_selected!= 4 and time_horizon_selected!= 5:
                time_horizon_selected= int(input('\n1. What is your time horizon? (longer timespan offers more reliable returns) (1/2/3/4/5):\n\t1) 0-2 years\n\t2) 3-5 years\n\t3) 6-10 years\n\t4) 11-20 years\n\t5) 20+ years\n'))
            user_time_horizon = time_horizon_options[time_horizon_selected - 1]
            while desired_growth_selected != 1 and desired_growth_selected != 2 and desired_growth_selected != 3 and desired_growth_selected != 4 and desired_growth_selected != 5:
                desired_growth_selected = int(input('\n2. What are your annual growth goals? (1/2/3/4/5):\n\t1) Beat inflation (<3%)\n\t2) Modest and reliable (3-5%)\n\t3) Steady longterm (5-7%)\n\t4) Strong returns with moderate risk (7-9%)\n\t5) High growth with greater risk (10%+)\n'))
            user_desired_growth = desired_growth_options[desired_growth_selected - 1]
            while fluctuation_selected != 1 and fluctuation_selected!= 2 and fluctuation_selected!= 3 and fluctuation_selected!= 4 and fluctuation_selected!= 5:
                fluctuation_selected = int(input('\n3. How much daily fluctuation_selectedis okay with you? (1/2/3/4/5):\n\t1) Not much at all (<1%)\n\t2) Small ups and downs are okay (2-3%)\n\t3) Regular market swings (4-5%)\n\t4) I can handle large moves if it promotes growth (6-8%)\n\t5) Volatility doesn\' bother me (>8%)\n'))
            user_fluctuation = fluctuation_options[fluctuation_selected - 1]
            while worst_case_selected!= 1 and worst_case_selected!= 2 and worst_case_selected!= 3 and worst_case_selected!= 4 and worst_case_selected!= 5:
                worst_case_selected= int(input('\n4. In the worst case, what is the greatest loss you could tolerate? (1/2/3/4/5):\n\t1) Very low (<5%)\n\t2) Minor (<10%)\n\t3) Moderate (<20%)\n\t4) High (<35%)\n\t5) Very high (>35%)\n'))
                
            user_worst_case = worse_case_options[worst_case_selected - 1]
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
    return [user_time_horizon, user_desired_growth, user_fluctuation, user_worst_case]

getUserProfile()