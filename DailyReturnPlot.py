import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pandas as pd

ticker=input()

def compute_daily_return(df):
    daily_ret=df.copy()
    daily_ret[1:]=(df[1:]/df[:-1].values)-1
    daily_ret.ix[0]=0
    return daily_ret
def plot_data(df, title="Stock prices"):
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

def dailyreturnplot():
    df = pd.read_csv("CompiledData.csv",parse_dates=True, na_values=['nan'])
    df.fillna(method="ffill",inplace=True)
    df.fillna(method="bfill",inplace=True)
    dailyreturn=compute_daily_return(df[ticker])
    plot_data(dailyreturn,title="Daily returns")
    
dailyreturnplot()
