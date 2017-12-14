import os
import pandas as pd
import pickle as pickle
import csv
from collections import deque 

def compile_data():

    def get_first_row():
        with open('stock_dfs/SPY.csv') as f:
            reader = csv.reader(f)
            row1 = next(reader)
            row1 = next(reader)
            return row1[0]
    
    def get_last_row(csv_filename):
        with open(csv_filename, 'rt') as f:
            return deque(csv.reader(f), 1)[0]
    start=get_first_row()
    end = get_last_row('stock_dfs/SPY.csv')
    dates = pd.date_range(start,end[0])
    
    df = pd.DataFrame(index=dates)
    with open("sp500tickers.pickle","rb") as f:
            tickers = pickle.load(f)
    for ticker in tickers:
        if(ticker=="BRK.B" or ticker=="BF.B"):
                continue
        else:
            df_temp = pd.read_csv('stock_dfs/{}.csv'.format(ticker), index_col='Date',parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
            #df_temp.fillna(method="ffill",inplace=True)
            #df.fillna(method="bfill",inplace=True)
            df_temp = df_temp.rename(columns={'Adj Close': ticker})
            df = df.join(df_temp)
            df.fillna(method="ffill",inplace=True)
            df.fillna(method="bfill",inplace=True)
            print (ticker)
            if ticker == 'SPY':  # drop dates SPY did not trade
                df = df.dropna(subset=["SPY"])
            df.to_csv("CompiledData.csv")
            

compile_data()
