import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle as pickle

#Function to fetch stock data of S&P 500 stocks(names stored in the pickle)

todaydate=dt.datetime.now()

def get_data_from_yahoo(reload_sp500=False):
    
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle","rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(todaydate.year,todaydate.month, (todaydate.day-1))
    
    for ticker in tickers:
        #print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            if(ticker=="BRK.B" or ticker=="BF.B"):
                continue
            df = web.DataReader(ticker, "yahoo", start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
            continue
        
get_data_from_yahoo()
