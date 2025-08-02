'''
Asks user to build financial goal profile
'''

def get_choice(prompt, options):
    while True:
        try:
            choice = int(input(prompt))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def getUserProfile():
    time_horizon_options = [1, 4, 8, 15, 25]
    desired_growth_options = [2, 4, 6, 8, 11]
    fluctuation_options = [1, 3, 5, 8, 100]
    worse_case_options = [15, 25, 35, 45, 100]
    minimum_etf_age = [10, 5, 3, 1, 0]

    print("\nHello and welcome to ETF Navigator!\nPlease answer the following questions...")

    user_time_horizon = get_choice(
        '\n1. What is your time horizon? (1/2/3/4/5):\n'
        '\t1) 0-2 years\n\t2) 3-5 years\n\t3) 6-10 years\n\t4) 11-20 years\n\t5) 20+ years\n',
        time_horizon_options)

    user_desired_growth = get_choice(
        '\n2. What are your annual growth goals? (1/2/3/4/5):\n'
        '\t1) Beat inflation (<3%)\n\t2) Modest and reliable (3-5%)\n\t3) Steady longterm (5-7%)\n'
        '\t4) Strong returns with moderate risk (7-9%)\n\t5) High growth with greater risk (10%+)\n',
        desired_growth_options)

    user_fluctuation = get_choice(
        '\n3. How much daily fluctuation is okay with you? (1/2/3/4/5):\n'
        '\t1) Not much at all (<1%)\n\t2) Small ups and downs are okay (2-3%)\n'
        '\t3) Regular market swings (4-5%)\n\t4) I can handle large moves if it promotes growth (6-8%)\n'
        '\t5) Volatility doesn\'t bother me (>8%)\n',
        fluctuation_options)

    user_worst_case = get_choice(
        '\n4. In the worst case, what is the greatest loss you could tolerate? (1/2/3/4/5):\n'
        '\t1) Low (<15%)\n\t2) Minor (<25%)\n\t3) Moderate (<35%)\n\t4) High (<45%)\n\t5) Very high (>45%)\n',
        worse_case_options)
    
    user_minimum_efs_age = get_choice(
        '\n5. What is the minimum amount of time you would like the ETF to have existed for? (The older the ETF the more reliable the range of data) (1/2/3/4/5):\n'
        '\t1) Very Established (>10 years)\n\t2) Experienced some variation (>5 years)\n\t3) Newer is okay (>3 years)\n\t4) I don\'t mind less data (>1 year)\n\t5) I want all options (up to present)\n',
        minimum_etf_age)
    

    return [user_time_horizon, user_desired_growth, user_fluctuation, user_worst_case, user_minimum_efs_age]
