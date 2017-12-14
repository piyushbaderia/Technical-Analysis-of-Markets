import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
#import pickle


ticker=input()

style.use('ggplot')
df = pd.read_csv('stock_dfs/{}.csv'.format(ticker), parse_dates=True, index_col=0)
df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_ohlc.fillna(method="ffill",inplace=True)
df_ohlc.fillna(method="bfill",inplace=True)
df_volume = df['Volume'].resample('10D').sum()
df_volume.fillna(method="ffill",inplace=True)
df_volume.fillna(method="bfill",inplace=True)
df_ohlc.reset_index(inplace=True)
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()
candlestick_ohlc(ax1, df_ohlc.values, width=5, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()
