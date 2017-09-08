# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 14:41:37 2017

@author: Chad
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 15:51:45 2017

@author: Chad
"""

from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import time
from datetime import datetime, timedelta

# Define the instruments to download. We would like to see Apple, Microsoft and the S&P500 index.
tickers = ['EFX','TRU','EXPN']

# Define which online source one should use
data_source = 'google'

# We would like all available data from 30 days until current system date.
end = time.strftime("%Y-%m-%d")
end = datetime.strptime(end, "%Y-%m-%d") #string to date
start = end - timedelta(days=30) 
start_date = start.strftime("%Y-%m-%d")
end_date = end.strftime("%Y-%m-%d")

# User pandas_reader.data.DataReader to load the desired data. As simple as that.
panel_data = data.DataReader(tickers, data_source, start_date, end_date)

# Getting just the adjusted closing prices. This will return a Pandas DataFrame
# The index in this DataFrame is the major index of the panel_data.
prices = panel_data.ix['Close']
adj_close = prices
adj_close = adj_close.pct_change()
adj_close = adj_close.fillna(0)


# Getting all weekdays between 01/01/2000 and 2017/09/08.
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')

# How do we align the existing prices in adj_close with our new set of dates?
# All we need to do is reindex adj_close using all_weekdays as the new index
adj_close = adj_close.reindex(all_weekdays)

# Reindexing will insert missing values (NaN) for the dates that were not present
# in the original set. To cope with this, we can fill the missing by replacing them
# with the latest available price for each instrument.
adj_close = adj_close.fillna(method='ffill')

# Get the EFX timeseries. This now returns a Pandas Series object indexed by date.
EFX = adj_close.ix[:, 'EFX']
TRU = adj_close.ix[:, 'TRU']
EXPN = adj_close.ix[:, 'EXPN']





# Plot everything by leveraging the very powerful matplotlib package
fig = plt.figure()
plt.xticks(rotation=70)
ax = fig.add_subplot(1,1,1)
ax.plot(EFX.index, EFX, label='Equifax')
ax.plot(TRU.index, TRU, label='Transunion')
ax.plot(EXPN.index, EXPN, label='Experian')
ax.set_title("Stock Prices Percent Change for Credit Agenencies")
ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price change (%)')
ax.legend()
