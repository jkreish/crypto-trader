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
BTCKrakenDaily = pd.read_csv('HistoricalData/KrakenBTC-USDPriceData.csv')
BTCExchangeDaily = pd.read_csv('HistoricalData/ExchangesBTC-USDPriceData.csv')
BTCGDAXHourly = pd.read_csv('HistoricalData/GDAX_BTC_Hourly_Aug-Dec17.csv')

# Date Array
dates_daily = BTCExchangeDaily.iloc[:,0].values
dates_daily = np.array(dates_daily)
dates_daily = dates_daily.astype(np.str)
dates_daily_dateTime = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates_daily]

# Time Array
time_hourly = BTCGDAXHourly.iloc[:,0].values
time_hourly = np.array(time_hourly)
time_hourly = time_hourly.astype(np.str)
time_hourly_dateTime = [dt.datetime.strptime(d, '%Y-%m-%d %H:%M:%S') for d in time_hourly]

# Average BTC Price from exchanges
averageBTCPrice = BTCExchangeDaily.iloc[:,5].values
averageBTCPrice = np.array(averageBTCPrice)
averageBTCPrice = averageBTCPrice.astype(np.float)

# Hourly Close BTC Price
hourlyCloseBTCPrice = BTCGDAXHourly.iloc[:,4].values
length = hourlyCloseBTCPrice.shape[0]-1
for i in range(0,length):
    if hourlyCloseBTCPrice[i] == '—':
        hourlyCloseBTCPrice[i] = hourlyCloseBTCPrice[i-1]
        
hourlyCloseBTCPrice = np.array(hourlyCloseBTCPrice)
hourlyCloseBTCPrice = hourlyCloseBTCPrice.astype(np.float)


start_date = '2017-11-1'
start_time = start_date + ' 0:00:00'

# PLOTTING
start_date_dateTime = dt.datetime.strptime(start_date, '%Y-%m-%d').date()
start_daily_index = dates_daily_dateTime.index(start_date_dateTime )

start_hour_dateTime = dt.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
start_hour_index = time_hourly_dateTime.index(start_hour_dateTime )


# Create DAILY data
DAILY = {'average': averageBTCPrice}

# Create dataframe
df = pd.DataFrame(DAILY)

DAILY['EMA10'] = df.rolling(10).mean()
DAILY['EMA20'] = df.rolling(20).mean()
DAILY['EMA50'] = df.rolling(50).mean()

DAILY['Bol_upper'] = DAILY['EMA20'] + 2* df.rolling(20).std()
DAILY['Bol_lower'] = DAILY['EMA20'] - 2* df.rolling(20).std()

DAILY['Bol_BW'] = ((DAILY['Bol_upper'] - DAILY['Bol_lower'])/DAILY['EMA20'])*100
#Y['Bol_BW_200MA'] = Y['Bol_BW'].rolling(50).mean() #cant get the 200 daa
#Y['Bol_BW_200MA'] = temp_data_set['Bol_BW_200MA'].fillna(method='backfill')##?? ,may not be good
#Y['20d_exma'] = pandas.ewma(temp_data_set['Adj Close'], span=20)
#Y['50d_exma'] = pandas.ewma(temp_data_set['Adj Close'], span=50)

# Create HOURLY data
tel = {'jack': 4098, 'sape': 4139}


hourly_data = {'close': hourlyCloseBTCPrice}

# Create dataframe
df2 = pd.DataFrame(hourly_data)

hourly_data['EMA10-4'] = df2.rolling(10*4).mean()
hourly_data['EMA20-4'] = df2.rolling(20*4).mean()
hourly_data['EMA99-4'] = df2.rolling(99*4).mean()
hourly_data['Bol_upper-4'] = hourly_data['EMA20-4'] + 2* df2.rolling(20*4).std()
hourly_data['Bol_lower-4'] = hourly_data['EMA20-4'] - 2* df2.rolling(20*4).std()
hourly_data['Bol_BW-4'] = ((hourly_data['Bol_upper-4'] - hourly_data['Bol_lower-4'])/hourly_data['EMA20-4'])*100



hourly_data['EMA10-2'] = df2.rolling(10*2).mean()
hourly_data['EMA20-2'] = df2.rolling(20*2).mean()
hourly_data['EMA99-2'] = df2.rolling(99*2).mean()
hourly_data['Bol_upper-2'] = hourly_data['EMA20-2'] + 2* df2.rolling(20*2).std()
hourly_data['Bol_lower-2'] = hourly_data['EMA20-2'] - 2* df2.rolling(20*2).std()
hourly_data['Bol_BW-2'] = ((hourly_data['Bol_upper-2'] - hourly_data['Bol_lower-2'])/hourly_data['EMA20-2'])*100

#HOURLY['Bol_BW'] = ((HOURLY['Bol_upper'] - HOURLY['Bol_lower'])/HOURLY['EMA20'])*100



#data_ext.all_stock_df = temp_data_set.sort('Date',ascending = False ) #revese back to original


fig, axarr = plt.subplots(2,2)

#ax1.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#plt.gca().xaxis.set_major_locator(mdates.DayLocator())

axarr[0,0].plot(dates_daily_dateTime[start_daily_index:len(dates_daily_dateTime)],DAILY['average'][start_daily_index:len(dates_daily_dateTime)])
axarr[0,0].plot(dates_daily_dateTime[start_daily_index:len(dates_daily_dateTime)],DAILY['EMA10'][start_daily_index:len(dates_daily_dateTime)])
axarr[0,0].plot(dates_daily_dateTime[start_daily_index:len(dates_daily_dateTime)],DAILY['EMA20'][start_daily_index:len(dates_daily_dateTime)])
axarr[0,0].plot(dates_daily_dateTime[start_daily_index:len(dates_daily_dateTime)],DAILY['EMA50'][start_daily_index:len(dates_daily_dateTime)])
axarr[0,0].plot(dates_daily_dateTime[start_daily_index:len(dates_daily_dateTime)],DAILY['Bol_upper'][start_daily_index:len(dates_daily_dateTime)], '--')
axarr[0,0].plot(dates_daily_dateTime[start_daily_index:len(dates_daily_dateTime)],DAILY['Bol_lower'][start_daily_index:len(dates_daily_dateTime)], '--')
axarr[0,0].set_title('Daily Moving Averages')
#ax1.gcf().autofmt_xdate()


#ax1.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#plt.gca().xaxis.set_major_locator(mdates.DayLocator())

#axarr[1,0].plot(dates_daily_dateTime[start_daily_index:len(dates_daily_dateTime)],DAILY['average'][start_daily_index:len(dates_daily_dateTime)])
axarr[1,0].plot(time_hourly_dateTime[start_hour_index:len(time_hourly_dateTime)],hourly_data['close'][start_hour_index:len(time_hourly_dateTime)])
axarr[1,0].plot(time_hourly_dateTime[start_hour_index:len(time_hourly_dateTime)],hourly_data['EMA10-4'][start_hour_index:len(time_hourly_dateTime)])
axarr[1,0].plot(time_hourly_dateTime[start_hour_index:len(time_hourly_dateTime)],hourly_data['EMA20-4'][start_hour_index:len(time_hourly_dateTime)])
axarr[1,0].plot(time_hourly_dateTime[start_hour_index:len(time_hourly_dateTime)],hourly_data['EMA99-4'][start_hour_index:len(time_hourly_dateTime)])
axarr[1,0].plot(time_hourly_dateTime[start_hour_index:len(time_hourly_dateTime)],hourly_data['Bol_upper-4'][start_hour_index:len(time_hourly_dateTime)], '--')
axarr[1,0].plot(time_hourly_dateTime[start_hour_index:len(time_hourly_dateTime)],hourly_data['Bol_lower-4'][start_hour_index:len(time_hourly_dateTime)], '--')
axarr[1,0].set_title('4 Hour Moving Averages')



#axarr[1,1].plot(time_hourly_dateTime[start_hour_index:len(time_hourly_dateTime)],HOURLY['close'][start_hour_index:len(time_hourly_dateTime)])
axarr[1,1].plot(time_hourly_dateTime[start_hour_index:len(time_hourly_dateTime)],hourly_data['EMA10-2'][start_hour_index:len(time_hourly_dateTime)])
axarr[1,1].plot(time_hourly_dateTime[start_hour_index:len(time_hourly_dateTime)],hourly_data['EMA20-2'][start_hour_index:len(time_hourly_dateTime)])
axarr[1,1].plot(time_hourly_dateTime[start_hour_index:len(time_hourly_dateTime)],hourly_data['EMA99-2'][start_hour_index:len(time_hourly_dateTime)])
axarr[1,1].plot(time_hourly_dateTime[start_hour_index:len(time_hourly_dateTime)],hourly_data['Bol_upper-2'][start_hour_index:len(time_hourly_dateTime)], '--')
axarr[1,1].plot(time_hourly_dateTime[start_hour_index:len(time_hourly_dateTime)],hourly_data['Bol_lower-2'][start_hour_index:len(time_hourly_dateTime)], '--')
axarr[1,1].set_title('2 Hour Moving Averages')



plt.show()


