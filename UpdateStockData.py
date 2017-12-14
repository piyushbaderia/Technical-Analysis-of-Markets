import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle as pickle
from collections import deque
import csv



#Function to update CSV files

todaydate=dt.datetime.now()

def get_last_row(csv_filename):
    with open(csv_filename, 'rt') as f:
        return deque(csv.reader(f), 1)[0]



def update_data(reload_sp500=False):
            lastline = get_last_row('stock_dfs/MMM.csv')
            values=lastline
            lastdate=values[0]
            print (values[0])
            append_data(lastdate)

            
def append_data(lastdate):
    tickers=pickle.load(open("sp500tickers.pickle","rb"))
    for ticker in tickers:
        if(ticker=="BRK.B" or ticker=="BF.B"):
                continue

        else:
            start=lastdate
            end = dt.datetime(todaydate.year,todaydate.month, (todaydate.day-1))
            df = web.DataReader(ticker, "yahoo", start, end)
            #df_append = pd.read_csv('stock_dfs/{}.csv'.format(ticker),parse_dates=True,index_col=0)
            print ("Appending Data")
            #df_append.append(df)
            with open('stock_dfs/{}.csv'.format(ticker),'a') as f:
                df.to_csv(f,header=False)

update_data()
