import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#ticker = 'GOOG'
#type(ticker)

def get_rolling_mean(values, window):
    return pd.rolling_mean(values, window=window)

def get_rolling_std(values, window):
    return pd.rolling_std(values, window=window)

def get_rolling_median(values, window):
    return pd.rolling_median(values, window=window)

def custom_stats(var1,var2,var3,ticker):
    
    df = pd.read_csv("CompiledData.csv",parse_dates=True, na_values=['nan'])
    df.fillna(method="ffill",inplace=True)
    df.fillna(method="bfill",inplace=True)
    ax = df[ticker].plot(title="Custom Stats", label=ticker)
    
    def plot_mean():
        RollingMean = get_rolling_mean(df[ticker], window=20)
        RollingMean.plot(label='Rolling mean', ax=ax)

    def plot_std():
        RollingStd = get_rolling_std(df[ticker], window=20)
        RollingStd.plot(label='Rolling Standard', ax=ax)

    def plot_median():
        RollingMedian = get_rolling_median(df[ticker],window=20)
        RollingMedian.plot(label='Rolling Median',ax=ax)
    if(var1==1):
        plot_mean()
        if(var2==1):
            plot_std()
            if(var3==1):
                plot_median()
        else:
            if(var3==1):
                plot_median()
    else:
        if(var2==1):
            plot_std()
            if(var3==1):
                plot_median()
        else:
            if(var3==1):
                plot_median()
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.show()

#custom_stats()
