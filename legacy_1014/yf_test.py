import os
import pandas as pd
import yfinance as yf

code = "012450.KS"

data = yf.Ticker(code)
df = data.history(start="2023-01-01")

df["weekday"] = df.index.weekday

fri_df = df[df["weekday"] == 4]


print(fri_df)

