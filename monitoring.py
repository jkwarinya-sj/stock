import pandas as pd
import FinanceDataReader as fdr

name_list = ['EM']
code_list = ['091120']
price_list = [36350]
stock_cnt_list = [100]


for code, price, stock_cnt, name in zip(code_list, price_list, stock_cnt_list, name_list):
    price_df = fdr.DataReader(code)
    #print(price_df)

    today = price_df.iloc[-1]['Close']
    #print(today*stock_cnt)
    curr_price = today*stock_cnt
    buy_price = price*stock_cnt
    print("{0}: {1}, {2}, {3}, {4}%".format(name, curr_price, buy_price, curr_price-buy_price, round(((curr_price / buy_price)-1)*100,2)))
