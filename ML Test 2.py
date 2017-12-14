import bs4 as bs
from collections import Counter
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
from sklearn import svm, cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
import csv
from collections import deque 

style.use('ggplot')

counter=0
count_0=0
count_1=0
count__1=0

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
##            df.fillna(method="ffill",inplace=True)
##            df.fillna(method="bfill",inplace=True)
            print (ticker)
            if ticker == 'SPY':  # drop dates SPY did not trade
                df = df.dropna(subset=["SPY"])
            df.to_csv("CompiledData1.csv")
            

#compile_data()

def process_data_for_labels(ticker):
    hm_days = 7
    df = pd.read_csv('CompiledData1.csv', index_col=0)
    tickers = df.columns.values.tolist()
    #df.fillna(0, inplace=True)
    for i in range(1,hm_days+1):
        df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
        
    #df.fillna(0, inplace=True)
    return tickers, df

def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.02
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0


def extract_featuresets(ticker):
    tickers, df = process_data_for_labels(ticker)

    df['{}_target'.format(ticker)] = list(map( buy_sell_hold,
                                               df['{}_1d'.format(ticker)],
                                               df['{}_2d'.format(ticker)],
                                               df['{}_3d'.format(ticker)],
                                               df['{}_4d'.format(ticker)],
                                               df['{}_5d'.format(ticker)],
                                               df['{}_6d'.format(ticker)],
                                               df['{}_7d'.format(ticker)] ))


    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread:',Counter(str_vals))

    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)

    X = df_vals.values
    y = df['{}_target'.format(ticker)].values
    
    return X,y,df


def do_ml(ticker):
    X, y, df = extract_featuresets(ticker)

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,
                                                        y,
                                                        test_size=0.15)


    #clf = neighbors.KNeighborsClassifier()

    clf = VotingClassifier([('lsvc',svm.LinearSVC()),
                            ('knn',neighbors.KNeighborsClassifier()),
                            ('rfor',RandomForestClassifier())])


    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('accuracy:',confidence)
    predictions = clf.predict(X_test)
    c=Counter(predictions)
    print('predicted class counts:',c)
    li=list(c.items())
    li=sorted(li,key=lambda l:l[1], reverse=True)
    print (li)
    print (li[0][0])
    print()
    print()
    print()
    return li[0][0]

with open("sp500tickers.pickle","rb") as f:
            tickers = pickle.load(f)

for ticker in tickers:
    if(ticker=="BRK.B" or ticker=="BF.B"):
                continue
    else:
        counter=counter+1
        print (ticker)
        a=do_ml(ticker)
        if(a==0):
            count_0=count_0+1
        if(a==1):
            count_1=count_1+1
        if(a==-1):
            count__1=count__1+1

print (count_0)
print (count_1)
print (count__1)
print (counter)

