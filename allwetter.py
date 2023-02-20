import pandas as pd
from pandas.tseries.offsets import BQuarterEnd,BMonthEnd
import datetime
from datetime import date
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
#%matplotlib inline

#** GLOBALS
ASSETS = ['SPY','IEF','TLT','DBC','GLD']
WEIGHTS = [0.3,0.15,0.4,0.075,0.075]

data = yf.download("SPY DBC TLT IEF GLD",start="2010-01-01",end="2022-01-01")
df = pd.DataFrame(data['Adj Close'])

# Quartalsenden für Rebalancing hinzufügen
rebals = []
for idx in df[df.index.month == 5].index.date:
    rebals.append(BMonthEnd().rollforward(idx))

for idx in df[df.index.month == 11].index.date:
    rebals.append(BMonthEnd().rollforward(idx))

df['Rebalancing_Days'] = np.where(df.index.isin(np.unique(rebals)),1,0)

# Log-Renditen berechnen
for asset in ASSETS:
    df[asset+'_ret'] = np.log(df[asset]) / np.log(df[asset].shift(1))