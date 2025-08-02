import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

ETFs = ["SVR.TO", "IBIT.TO", "CGL.TO", "XMV.TO", "XMI.TO", "XML.TO", "XIN.TO", "XMS.TO", "XMY.TO", "XEM.TO", "XMM.TO", "XEC.TO", "XUS.TO", "XEF.TO", "XMH.TO", "XMC.TO", "XDIV.TO", "XMU.TO", "XQQ.TO", "XWD.TO", "XDUH.TO", "XDG.TO", "XSU.TO", "XDU.TO", "XSUS.TO", "XSEA.TO", "XDGH.TO", "XESG.TO", "XGI.TO", "XCD.TO", "XSEM.TO", "XSP.TO", "CWO.TO", "CRQ.TO", "XID.TO", "XCH.TO", "XEMC.TO", "XHC.TO", "XDRV.TO", "CWW.TO", "XCV.TO", "XCG.TO", "XUSR.TO", "XDV.TO", "XDSR.TO", "XEU.TO", "CEW.TO", "XEH.TO", "XUU.TO", "COW.TO", "CIF.TO", "CYH.TO", "XDNA.TO", "XCLN.TO", "XQQU.TO", "XEXP.TO", "XAW.TO", "XHAK.TO", "XETM.TO", "XCHP.TO", "CIE.TO", "XUSF.TO", "XAD.TO", "XEN.TO", "CUD.TO", "CDZ.TO", "XQLT.TO", "XIU.TO", "CJP.TO", "XEG.TO", "XST.TO", "XIC.TO", "CPD.TO", "XSMC.TO",
        "XMA.TO", "XUSC.TO", "XSMH.TO", "XFH.TO", "XIT.TO", "XFN.TO", "XMTM.TO", "XBM.TO", "XEI.TO", "XVLU.TO", "XMD.TO", "XUT.TO", "XCSR.TO", "XPF.TO", "XHU.TO", "XGD.TO", "XSPC.TO", "XUH.TO", "XCS.TO", "XHD.TO", "CLU.TO", "XMW.TO", "XSC.TO", "XSE.TO", "CMR.TO", "CLG.TO", "CBH.TO", "CLF.TO", "CBO.TO", "XGGB.TO", "CVD.TO", "XQB.TO", "XAGG.TO", "XCBG.TO", "XSHG.TO", "XAGH.TO", "XSTB.TO", "XFLB.TO", "XFLI.TO", "XFLX.TO", "XSAB.TO", "XTLH.TO", "XTLT.TO", "XFR.TO", "XGB.TO", "XCB.TO", "XSB.TO", "XSI.TO", "XRB.TO", "XLB.TO", "XHB.TO", "XBB.TO", "XSH.TO", "XSTH.TO", "XSTP.TO", "XCBU.TO", "XIGS.TO", "XSHU.TO", "XEB.TO", "XIG.TO", "XHY.TO", "GCNS.TO", "GGRO.TO", "GEQT.TO", "GBAL.TO", "XGRO.TO", "XBAL.TO", "FIE.TO", "XTR.TO", "XCNS.TO", "XEQT.TO", "XINC.TO", "CGR.TO", "XRE.TO"]


def get_etf_data(symbols, years, tickers, data):
    """
    Get annual growth and standard deviation for multiple time periods for all ETFs

    Args:
        symbols (list): List of ETF ticker symbols
        delay (float): Delay between requests to avoid rate limiting

    Returns:
        pd.DataFrame: DataFrame with all metrics
    """
    end_date = datetime.now()  # years
    start_date = end_date - timedelta(days=365 * years)
    results = []

    print(f"Processing {len(symbols)} ETFs...")

    # for i, symbol in enumerate(symbols):
    #     row = {'Symbol': symbol}

    #     ticker = yf.Ticker(symbol)

        # Calculate start date
    for ticker in tickers:
        row = {'Symbol': ticker}

        try:
            df = data[ticker]
            prices = df['Close'].dropna()
            prices = prices[(prices.index >= start_date) & (prices.index <= end_date)]
    # data = ticker.history(start=start_date.strftime('%Y-%m-%d'),
    #                           end=end_date.strftime('%Y-%m-%d'))

            # calculate annual growth
            start_price = prices.iloc[0]
            end_price = prices.iloc[-1]

            annual_growth = ((end_price / start_price) - 1) * 100 / years
            annual_growth = round(annual_growth, 2)

            # calculate annual standard deviation
            daily_returns = prices.pct_change().dropna()
            annual_std = daily_returns.std() * np.sqrt(252) * 100
            annual_std = round(annual_std, 2)

        except:
            annual_growth, annual_std, start_price = None, None, None

        row[f'Annual_Growth_{years}Y'] = annual_growth
        row[f'Standard_Deviation_{years}Y'] = annual_std

        results.append(row)

    return pd.DataFrame(results)


def export_etf_data(symbols, years, filename=None):
    """
    Export ETF data to CSV

    Args:
        symbols (list): List of ETF symbols
        filename (str): Output filename (auto-generated if None)

    Returns:
        str: Filename of exported CSV
    """
    df = get_etf_data(symbols, years)

    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'etf_data_{timestamp}.csv'

    df.to_csv(filename, index=False)
    print(f"Data exported to: {filename}")
    return filename


# Example usage
if __name__ == "__main__":
    years = 10
    # Export data
    filename = export_etf_data(ETFs, years)
