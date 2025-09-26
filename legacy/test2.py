import yfinance as yf
import sys
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


ticker = 'mo'
data = yf.Ticker(ticker)

df = data.history(period="6y")


idx = 0
year = 252
stock = 1
avr_list = []

pa = range(1,10)

for idx in pa:
    print(idx)

"""
for close in df['Close']:

    if(idx < year+1):
        idx = idx+1
        continue


    pre_close = df['Close'][idx-252]
    #print(close, pre_close, df['Dividends'][idx])
    stock = stock + (df['Dividends'][idx]/close)
    #print((close*stock)/pre_close - 1)
    avr_list.append((close*stock)/pre_close - 1)

    
    idx = idx+1


#print(sum(avr_list)/len(avr_list))

print(df)
"""
