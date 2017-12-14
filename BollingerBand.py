import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pandas as pd

ticker = input()
#type(ticker)

def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    return pd.rolling_mean(values, window=window)

def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    return pd.rolling_std(values, window=window)

def get_bollinger_bands(rm,rstd):
    upper_band=rm+rstd*2
    lower_band=rm-rstd*2
    return upper_band,lower_band

def bollinger_band():
    
    df = pd.read_csv("CompiledData.csv",parse_dates=True, na_values=['nan'])
    df.fillna(method="ffill",inplace=True)
    df.fillna(method="bfill",inplace=True)
    RollingMean = get_rolling_mean(df[ticker], window=20)
    RollingStd = get_rolling_std(df[ticker], window=20)
    upper_band, lower_band = get_bollinger_bands(RollingMean, RollingStd)
    
    ax = df[ticker].plot(title="Bollinger Bands", label=ticker)
    RollingMean.plot(label='Rolling mean', ax=ax)
    upper_band.plot(label='upper band', ax=ax)
    lower_band.plot(label='lower band', ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.show()

bollinger_band()
