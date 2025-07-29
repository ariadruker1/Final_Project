import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

def get_etf_data(symbols, delay=0.1):
    """
    Get annual growth and standard deviation for multiple time periods for all ETFs
    
    Args:
        symbols (list): List of ETF ticker symbols
        delay (float): Delay between requests to avoid rate limiting
    
    Returns:
        pd.DataFrame: DataFrame with all metrics
    """
    end_date = datetime.now()
    time_periods = [1, 4, 8, 15, 25]  # years
    results = []
    
    print(f"Processing {len(symbols)} ETFs...")
    
    for i, symbol in enumerate(symbols):        
        row = {'Symbol': symbol}
        
        for years in time_periods:
            # Calculate start date
            start_date = end_date - timedelta(days=years * 365 + 30)
            
            try:
                # Fetch data
                ticker = yf.Ticker(symbol)
                data = ticker.history(start=start_date.strftime('%Y-%m-%d'), 
                                    end=end_date.strftime('%Y-%m-%d'))
                
                if len(data) < 50:  # Need minimum data
                    annual_growth, annual_std = None, None
                else:
                    # Calculate daily returns
                    daily_returns = data['Close'].pct_change().dropna()
                    
                    # Annual growth rate (CAGR)
                    start_price = data['Close'].iloc[0]
                    end_price = data['Close'].iloc[-1]
                    actual_years = len(data) / 252
                    annual_growth = ((end_price / start_price) ** (1 / actual_years) - 1) * 100
                    
                    # Annual standard deviation
                    annual_std = daily_returns.std() * np.sqrt(252) * 100
                    
                    annual_growth = round(annual_growth, 2)
                    annual_std = round(annual_std, 2)
                    
            except:
                annual_growth, annual_std = None, None
            
            row[f'Annual_Growth_{years}Y'] = annual_growth
            row[f'Standard_Deviation_{years}Y'] = annual_std
        
        results.append(row)
        time.sleep(delay)
    
    return pd.DataFrame(results)

def export_etf_data(symbols, filename=None):
    """
    Export ETF data to CSV
    
    Args:
        symbols (list): List of ETF symbols
        filename (str): Output filename (auto-generated if None)
    
    Returns:
        str: Filename of exported CSV
    """
    df = get_etf_data(symbols)
    
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'etf_data_{timestamp}.csv'
    
    df.to_csv(filename, index=False)
    print(f"Data exported to: {filename}")
    return filename

# Example usage
if __name__ == "__main__":
    # Sample ETFs for testing
    sample_etfs = ['SPY', 'QQQ', 'IWM', 'VTI', 'BND']
    # ishares_etfs = ['IVV', 'IWM', 'IWF', ...] (We need a complete list of 169 etfs)
    
    # Export data
    filename = export_etf_data(sample_etfs)
