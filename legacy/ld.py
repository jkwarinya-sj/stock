import pandas as pd

import yfinance as yf


ticker = '069500.KS' 

data = yf.Ticker(ticker)
df = data.history(interval="1wk", start="2019-01-01")
#price_df = fdr.DataReader('069500, 229200')

print(df['Close'])

