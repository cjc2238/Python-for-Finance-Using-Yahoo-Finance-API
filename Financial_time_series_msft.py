# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 15:51:45 2017

@author: Chad
"""

from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd

# Define the instruments to download. We would like to see Apple, Microsoft and the S&P500 index.
tickers = ['AAPL', 'MSFT', 'NEM']

# Define which online source one should use
data_source = 'yahoo'

# We would like all available data from 01/01/2000 until 2017-04-05.
start_date = '2016-01-01'
end_date = '2017-04-05'

# User pandas_reader.data.DataReader to load the desired data. As simple as that.
panel_data = data.DataReader(tickers, data_source, start_date, end_date)

# Getting just the adjusted closing prices. This will return a Pandas DataFrame
# The index in this DataFrame is the major index of the panel_data.
adj_close = panel_data.ix['Adj Close']

# Getting all weekdays between 01/01/2000 and 2017/04/05.
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')

# How do we align the existing prices in adj_close with our new set of dates?
# All we need to do is reindex adj_close using all_weekdays as the new index
adj_close = adj_close.reindex(all_weekdays)

# Reindexing will insert missing values (NaN) for the dates that were not present
# in the original set. To cope with this, we can fill the missing by replacing them
# with the latest available price for each instrument.
adj_close = adj_close.fillna(method='ffill')

# Get the MSFT timeseries. This now returns a Pandas Series object indexed by date.
msft = adj_close.ix[:, 'MSFT']
aapl = adj_close.ix[:, 'AAPL']
nem = adj_close.ix[:, 'NEM']

# Calculate the 20 and 100 days moving averages of the closing prices
short_rolling_msft = msft.rolling(window=20).mean()
long_rolling_msft = msft.rolling(window=100).mean()

short_rolling_aapl = aapl.rolling(window=20).mean()
long_rolling_aapl = aapl.rolling(window=100).mean()


# Plot everything by leveraging the very powerful matplotlib package
fig = plt.figure()
plt.xticks(rotation=70)
ax = fig.add_subplot(1,1,1)
ax.plot(aapl.index, aapl, label='AAPL')
ax.plot(short_rolling_aapl.index, short_rolling_aapl, label='20 days rolling')
ax.plot(long_rolling_aapl.index, long_rolling_aapl, label='100 days rolling')
ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price ($)')
ax.legend()

# Plot everything by leveraging the very powerful matplotlib package
fig = plt.figure()
plt.xticks(rotation=70)
ax = fig.add_subplot(1,1,1)
ax.plot(msft.index, msft, label='MSFT')
ax.plot(short_rolling_msft.index, short_rolling_msft, label='20 days rolling')
ax.plot(long_rolling_msft.index, long_rolling_msft, label='100 days rolling')
ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price ($)')
ax.legend()


# Plot everything by leveraging the very powerful matplotlib package
fig = plt.figure()
plt.xticks(rotation=70)
ax = fig.add_subplot(1,1,1)
ax.plot(nem.index, nem, label='NEM')
ax.plot(short_rolling_nem.index, short_rolling_nem, label='20 days rolling')
ax.plot(long_rolling_nem.index, long_rolling_nem, label='100 days rolling')
ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price ($)')
ax.legend()