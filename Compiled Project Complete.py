import mysql.connector
import sys
from tkinter import *
from tkinter import messagebox
import pickle
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle as pickle
from collections import deque
import csv
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


#database connection
conn=mysql.connector.connect(host='localhost',user='root',passwd='piyush123') #connection
cursor = conn.cursor()
cursor.execute('use stockprediction;')


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



#Function to fetch stock data of S&P 500 stocks(names stored in the pickle)

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
    #print('Data spread:',Counter(str_vals))

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
    #print('accuracy:',confidence)
    predictions = clf.predict(X_test)
    c=Counter(predictions)
    #print('predicted class counts:',c)
    li=list(c.items())
    li=sorted(li,key=lambda l:l[1], reverse=True)
    #print (li)
    #print (li[0][0])
    if(li[0][0]==0):
        print("HOLD "+ticker)
    if(li[0][0]==1):
        print("BUY "+ticker)
    if(li[0][0]==-1):
        print("SELL "+ticker)
    return li[0][0]
    print()
    print()
    print()
    return li[0][0]

##with open("sp500tickers.pickle","rb") as f:
##            tickers = pickle.load(f)
##
##for ticker in tickers:
##    if(ticker=="BRK.B" or ticker=="BF.B"):
##                continue
##    else:
##        counter=counter+1
##        print (ticker)
##        a=do_ml(ticker)
##        if(a==0):
##            count_0=count_0+1
##        if(a==1):
##            count_1=count_1+1
##        if(a==-1):
##            count__1=count__1+1
##
##print (count_0)
##print (count_1)
##print (count__1)
##print (counter)


def dailyreturnplot(ticker):
    df = pd.read_csv("CompiledData1.csv",parse_dates=True, na_values=['nan'])
    df.fillna(method="ffill",inplace=True)
    df.fillna(method="bfill",inplace=True)
    dailyreturn=compute_daily_return(df[ticker])
    plot_data(dailyreturn,title="Daily returns")

def histogram(ticker):
    df = pd.read_csv("CompiledData1.csv",parse_dates=True, na_values=['nan'])
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
    
    df = pd.read_csv("CompiledData1.csv",parse_dates=True, na_values=['nan'])
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
    
    df = pd.read_csv("CompiledData1.csv",parse_dates=True, na_values=['nan'])
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


#visual()






def CheckLogin(luname,lpass):
    
    cursor.execute("SELECT name FROM login_tb where uname=%s and password=%s",(luname,lpass))

    
    row = cursor.fetchone()

    if(row):
          after_login=Tk()
          after_login.title('Welcome')
          name=Label(after_login, text="Hello!  "+row[0],fg="slate blue",font="Helvetica 12 bold")
          name.grid(row=1, sticky=W, column=1,pady=10,padx=15)
          row = cursor.fetchone()
          updateButton = Button(after_login, text='UPDATE DATA',fg="white",bg="slate blue",font="Helvetica 10",pady=5, command=lambda:update_data())
          updateButton.grid(row=2, sticky=W, column=1,pady=10,padx=15)

          fetchButton = Button(after_login, text='FETCH DATA',fg="white",bg="slate blue",font="Helvetica 10",pady=5,command=lambda:get_data_from_yahoo() )
          fetchButton.grid(row=3, sticky=W, column=1,pady=10,padx=15)

          visualButton = Button(after_login, text='VISUALIZATION',fg="white",bg="slate blue",font="Helvetica 10",pady=5,command=lambda:visual() )
          visualButton.grid(row=4, sticky=W, column=1,pady=10,padx=15)


          name=Label(after_login, text="Select Symbol",fg="slate blue",font="Helvetica 12 ")
          name.grid(row=2, sticky=W, column=2,padx=15)

          symname = Entry(after_login)
          symname.grid(row=3, column=2,padx=15, pady=5)
          
          paButton = Button(after_login, text='Predefined Analysis',fg="white",bg="slate blue",font="Helvetica 10",pady=5,command=lambda:do_ml(symname.get()) )
          paButton.grid(row=4, column=2,padx=15, pady=5)

          #scrollbar
          frame=Frame(after_login,width=50,height=50)
          frame.grid(row=5,column=2,pady=10)
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

          
          
    else:
          messagebox.showinfo(title="login",message="Incorrect login credentials")




def FSSignup(suname,spass,sname):
    
    try:
   # Execute the SQL command
     cursor.execute("""INSERT INTO login_tb (uname,password,name) VALUES(%s,%s,%s)""",(suname,spass,sname))
   # Commit your changes in the database
     conn.commit()
     messagebox.showinfo(title="Signup",message="signup successful!")
    except:
     # Rollback in case there is any error
     conn.rollback
    


def quit():
    mexit = messagebox.askyesno(title="Quit", message="Are you sure?")
    if mexit > 0:
       root.destroy()
       return

def login():
        llabel=Label(root, text='LOGIN',fg="slate blue",font="Helvetica 12 bold")
        llabel.grid(row=2,column=64)

        nameL = Label(root, text='Username: ',fg="slate blue",font="Helvetica 10") # More labels
        pwordL = Label(root, text='Password: ',fg="slate blue",font="Helvetica 10") # ^
        nameL.grid(row=6, sticky=W, column=63,pady=10,padx=15)
        pwordL.grid(row=7, sticky=W, column=63,pady=10,padx=15)
     
        nameEL = Entry(root) # The entry input
        pwordEL = Entry(root, show='*')
        nameEL.grid(row=6, column=65,padx=15)
        pwordEL.grid(row=7, column=65,padx=15)
     
        loginB = Button(root, text='Submit',fg="white", bg="slate blue", command=lambda: CheckLogin(nameEL.get(), pwordEL.get())) # This makes the login button, which will go to the CheckLogin def.
        loginB.grid(row=9,column=64, sticky=W,pady=10,padx=15)

          

         

def signup():

    
       Sroot=Tk()
       Sroot.title('New User Signup')
       slabel=Label(Sroot, text='New User!',fg="slate blue",font="Helvetica 12 bold")
       slabel.grid(row=1,column=1,pady=20)
       unameL = Label(Sroot, text='New Email: ',fg="slate blue",font="Helvetica 10") # This just does the same as above, instead with the text new username.
       pwordL = Label(Sroot, text='New Password: ',fg="slate blue",font="Helvetica 10") # ^^
       nameL = Label(Sroot, text='Name : ',fg="slate blue",font="Helvetica 10")
       unameL.grid(row=2, column=0, sticky=W,padx=15,pady=10) # Same thing as the instruction var just on different rows. :) Tkinter is like that.
       pwordL.grid(row=3, column=0, sticky=W,padx=15,pady=10) # ^^
       nameL.grid(row=4, column=0, sticky=W,padx=15,pady=10) # ^^

       unameE = Entry(Sroot,textvariable=uname) # This now puts a text box waiting for input.
       pwordE = Entry(Sroot, show='*',textvariable=passw) # Same as above, yet 'show="*"' What this does is replace the text with *, like a password box :D
       nameE = Entry(Sroot,textvariable=name)
       unameE.grid(row=2, column=2,padx=15) # You know what this does now :D
       pwordE.grid(row=3, column=2,padx=15) # ^^
       nameE.grid(row=4, column=2,padx=15)
     
       signupButton = Button(Sroot, text='Submit',fg="white",bg="slate blue",font="Helvetica 10", command=lambda: FSSignup(unameE.get(), pwordE.get(),nameE.get())) # This creates the button with the text 'signup', when you click it, the command 'fssignup' will run. which is the def
       signupButton.grid(row=6,column=1, sticky=W,padx=15,pady=10)
       Sroot.mainloop()


    

#main page    
root=Tk()
#signup variables
uname=StringVar()
passw=StringVar()
name=StringVar()

root.title('Prediction of stock')


#menu
menubar=Menu(root)
menubar.add_cascade(label='Login', command= login)
menubar.add_cascade(label='Signup', command= signup)
menubar.add_cascade(label='Close', command= quit)

root.config(menu=menubar)


root.mainloop()


