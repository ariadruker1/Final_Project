'''
Aria Druker and Linghe Zhou

'''
import ishares_ETF_list as ishares
import user_profile as up
import max_drawdown as md

def main():
    # user = up.getUserProfile()
    md.calculate_max_drawdown("XIT", 1, 4)
    # for i in ishares.ETFs:
    #     md.calculate_max_drawdown(i, user[0], user[3])

main()