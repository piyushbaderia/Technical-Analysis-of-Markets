import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import datetime as dt
import numpy as np
import tkinter
import tkinter as tk
from tkinter import *
##from Histogram import histogram
##from Candlestck import candlestick
##from BollingerBand import bollinger_band
##from DailyReturnPlot import dailyreturnplot
##from CustomStats import custom_stats
import pickle


def dailyreturnplot(ticker):
    df = pd.read_csv("CompiledData.csv",parse_dates=True, na_values=['nan'])
    df.fillna(method="ffill",inplace=True)
    df.fillna(method="bfill",inplace=True)
    dailyreturn=compute_daily_return(df[ticker])
    plot_data(dailyreturn,title="Daily returns")

def histogram(ticker):
    df = pd.read_csv("CompiledData.csv",parse_dates=True, na_values=['nan'])
    df.fillna(method="ffill",inplace=True)
    df.fillna(method="bfill",inplace=True)
    dailyreturn=compute_daily_return(df[ticker])
    #plot_data(dailyreturn,title="Daily returns")
    #print (dailyreturn.head)
    dailyreturn=dailyreturn.values
    plt.hist(dailyreturn, 20)
    plt.show()
def compute_daily_return(df):
    daily_ret=df.copy()
    daily_ret[1:]=(df[1:]/df[:-1].values)-1
    daily_ret.ix[0]=0
    return daily_ret
def plot_data(df, title="Stock prices"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()

    
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

def bollinger_band(ticker):
    
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

def candlestick(ticker):
    #ticker=input()

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
  


def visual():
    app= Tk()

    #comp =[(1,"Mean"),(2,"Standard Deviation"),(3,"Median")]

    button1 = tk.Button(app, text='Histogram',height=2, width=20,fg="white", bg="slate blue", command=lambda: histogram(symbolname.get()))
    button1.grid(column=0, row=0, pady=10, padx=10, sticky=(tkinter.N))

    button2 = tk.Button(app, text='Daily Return Plot',height=2, width=20,fg="white", bg="slate blue", command=lambda: dailyreturnplot(symbolname.get()))
    button2.grid(column=0, row=1, pady=10, padx=10, sticky=(tkinter.N))

    button3 = tk.Button(app, text='Bollinger Band Analysis',height=2, width=20,fg="white", bg="slate blue", command=lambda: bollinger_band(symbolname.get()))
    button3.grid(column=0, row=2, pady=10, padx=10, sticky=(tkinter.N))

    button4 = tk.Button(app, text='Candlestick Analysis',height=2, width=20,fg="white", bg="slate blue", command=lambda: candlestick(symbolname.get()))
    button4.grid(column=0, row=3, pady=10, padx=10, sticky=(tkinter.N))

    label = tk.Label(app, text='Select your Stats', font=("Courier", 20),fg="slate blue")
    label.grid(column=1, row=0, pady=10, padx=50, sticky=(tkinter.E))

    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()

    Checkbutton(app, text="Mean", variable=var1,command =lambda: custom_stats(var1.get(),var2.get(),var3.get(),symbolname.get())).grid(column=1,pady=5, padx=10, row=1,rowspan=1, sticky=(tkinter.N))
    
    Checkbutton(app, text="Standard Deviation", variable=var2,command =lambda: custom_stats(var1.get(),var2.get(),var3.get(),symbolname.get())).grid(column=1, row=2,pady=5, padx=10,rowspan=1, sticky=(tkinter.N))
    
    Checkbutton(app, text="Median", variable=var3,command =lambda: custom_stats(var1.get(),var2.get(),var3.get(),symbolname.get())).grid(column=1, row=3,pady=5, padx=10,rowspan=1, sticky=(tkinter.N))

    #for v,data in comp:
     #   Checkbutton(app, text=data, variable=v).grid(column=1, padx=10, sticky=(tkinter.N+W+E+S))

    label2 = tk.Label(app, text='Enter Stock', font=("Courier", 20),fg="slate blue")
    label2.grid(column=2, row=0, pady=10, padx=20, sticky=(tkinter.E))

    symbolname = Entry(app)
    symbolname.grid(row=1, column=2,padx=15, pady=5)

    button5 = tk.Button(app, text='OK',height=2, width=20,fg="white", bg="slate blue", command=lambda: symbolselected(symbolname.get()))
    button5.grid(column=2, row=2, pady=10, padx=10, sticky=(tkinter.N))

    #scrollbar
    frame=Frame(app,width=50,height=50)
    frame.grid(row=3,column=2,pady=10)
    canvas=Canvas(frame,bg='grey',width=50,height=50)

    f = open('sp500tickers.pickle','rb')
    mydata= pickle.load(f)
    f.close()


    canvas.config(width=50,height=50)
    #canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    canvas.pack(side=LEFT,expand=True,fill=BOTH)

    scrollbar = Scrollbar(canvas)
    scrollbar.pack( side = RIGHT, fill=Y )

    mylist = Listbox(canvas, yscrollcommand = scrollbar.set )
    for line in mydata:
       mylist.insert(END,line)

    mylist.pack( side = LEFT, fill = BOTH )
    scrollbar.config( command = mylist.yview )



   
    

    app.mainloop()


visual()
