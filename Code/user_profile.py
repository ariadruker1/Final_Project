'''
Asks user to build financial goal profile
'''

def getUserProfile():
    time_horizon = 0
    desired_growth = 0
    fluctuation = 0
    worst_case = 0
    print("\nHello and welcome to ETF Navigator!\nPlease answer the following questions so we can suggest 5 ETFs we think would fit well with your financial goals.")
    while time_horizon == 0 or desired_growth == 0 or fluctuation == 0 or worst_case == 0:
        try:
            while time_horizon != 1 and time_horizon != 2 and time_horizon != 3 and time_horizon != 4 and time_horizon != 5:
                time_horizon = int(input('\n1. What is your time horizon? (1/2/3/4/5):\n\t1) 0-2 years\n\t2) 3-5 years\n\t3) 6-10 years\n\t4) 11-20 years\n\t5) 20+ years\n'))
            while desired_growth != 1 and desired_growth != 2 and desired_growth != 3 and desired_growth != 4 and desired_growth != 5:
                desired_growth = int(input('\n2. What are your growth goals? (a/b/c/d/5):\n\t1) Beat inflation (<3%)\n\t2) Modest and reliable (3-5%)\n\t3) Steady longterm (5-7%)\n\t4) Strong returns even with some bumps (7-9%)\n\t5) High growth with greater risk (10%+)\n'))
            while fluctuation != 1 and fluctuation != 2 and fluctuation != 3 and fluctuation != 4 and fluctuation != 5:
                fluctuation = int(input('\n3. How much daily fluctuation is okay with you? (a/b/c/d/5):\n\t1) Not much at all (<3%)\n\t2) Small ups and downs are okay (3-6%)\n\t3) Regular market swings (6-10%)\n\t4) I can handle large moves if it helps grow (10-15%)\n\t5) Volatility doesn\' bother me (15%+)\n'))
            while worst_case != 1 and worst_case != 2 and worst_case != 3 and worst_case != 4 and worst_case != 5:
                worst_case = int(input('\n4. In the worst case, what is the greatest loss you could tolerate? (a/b/c/d/5):\n\t1) Very low (<5%)\n\t2) Minor (<10%)\n\t3) Moderate (<20%)\n\t4) High (<35%)\n\t5) Very high (35%+)\n'))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

getUserProfile()