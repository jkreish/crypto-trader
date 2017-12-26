#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 16:39:19 2017

@author: JAK
"""

# Plotting of BB and moving averages

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.dates as mdates

# Historic Data
BTCKrakenData = pd.read_csv('HistoricalData/KrakenBTC-USDPriceData.csv')
BTCExchangeData = pd.read_csv('HistoricalData/ExchangesBTC-USDPriceData.csv')

# Date Array
dates = BTCExchangeData.iloc[:,0].values
dates = np.array(dates)
dates = dates.astype(np.str)



dates_dateTime = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]

# Average BTC Price from exchanges
averageBTCPrice = BTCExchangeData.iloc[:,5].values
averageBTCPrice = np.array(averageBTCPrice)
averageBTCPrice = averageBTCPrice.astype(np.float)



start_date = '2017-9-13'


# PLOTTING

start_date_dateTime = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
start_index = dates_dateTime.index(start_date_dateTime )


# Create data
Y = {'average': averageBTCPrice}

# Create dataframe
df = pd.DataFrame(Y)



Y['EMA10'] = df.rolling(10).mean()
Y['EMA20'] = df.rolling(20).mean()
Y['EMA50'] = df.rolling(50).mean()

Y['Bol_upper'] = Y['EMA20'] + 2* df.rolling(20).std()
Y['Bol_lower'] = Y['EMA20'] - 2* df.rolling(20).std()



Y['Bol_BW'] = ((Y['Bol_upper'] - Y['Bol_lower'])/Y['EMA20'])*100
#Y['Bol_BW_200MA'] = Y['Bol_BW'].rolling(50).mean() #cant get the 200 daa
#Y['Bol_BW_200MA'] = temp_data_set['Bol_BW_200MA'].fillna(method='backfill')##?? ,may not be good
#Y['20d_exma'] = pandas.ewma(temp_data_set['Adj Close'], span=20)
#Y['50d_exma'] = pandas.ewma(temp_data_set['Adj Close'], span=50)


#data_ext.all_stock_df = temp_data_set.sort('Date',ascending = False ) #revese back to original


plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#plt.gca().xaxis.set_major_locator(mdates.DayLocator())

plt.plot(dates_dateTime[start_index:len(dates_dateTime)],Y['average'][start_index:len(dates_dateTime)])
plt.plot(dates_dateTime[start_index:len(dates_dateTime)],Y['EMA10'][start_index:len(dates_dateTime)])
plt.plot(dates_dateTime[start_index:len(dates_dateTime)],Y['EMA20'][start_index:len(dates_dateTime)])
plt.plot(dates_dateTime[start_index:len(dates_dateTime)],Y['EMA50'][start_index:len(dates_dateTime)])

plt.plot(dates_dateTime[start_index:len(dates_dateTime)],Y['Bol_upper'][start_index:len(dates_dateTime)], '--')
plt.plot(dates_dateTime[start_index:len(dates_dateTime)],Y['Bol_lower'][start_index:len(dates_dateTime)], '--')
plt.gcf().autofmt_xdate()
plt.show()


