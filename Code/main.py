'''
Aria Druker and Linghe Zhou

'''
import ishares_ETF_list as ishares
import user_profile as up
import max_drawdown as md

def main():
    user = up.getUserProfile()
    md_tolerable_list = md.calculate_max_drawdown(user[3])
    print(md_tolerable_list)
main()