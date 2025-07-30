import yfinance as yf
import ishares_ETF_list as ishares

print("Script started")

def calculate_max_drawdown(ticker):
    data = yf.Ticker(ticker).history(period="1d", interval="1m")
    if data.empty:
        return None
    return data["Close"][-1]

for i in ishares.ETFs:
    print(i, calculate_max_drawdown(i))

