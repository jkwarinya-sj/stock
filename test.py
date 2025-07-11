
import yfinance as yf
import sys
import pandas as pd

# 가져올 주식 티커 (예: Apple)
ticker = 'schd'
dist = '0.0783'
year = 252
period = 10

if len(sys.argv)>1:
    ticker = sys.argv[1]
    dist = sys.argv[2]


dist_rate_f = float(dist)
# yfinance 객체 생성
data = yf.Ticker(ticker)

# 최근 1년 데이터 가져오기
df = data.history(period="11y")


# 데이터 출력
#print(df.head())
#print(df['Close'])



"""
idx = 0
avr_list = []
for close in df['Close']:
    idx = idx+1
    if(idx < (year+1)*period):
        continue

    pre_close = df['Close'][idx-(year*period)]
    print(close, pre_close, close/pre_close-1)

    dist = 0
    for i in range(period):
        dist = dist + df['Close'][idx-(year*(i+1))]*dist_rate_f



    #avr_list.append((close + pre_close*dist_rate_f)/pre_close-1)
    avr_list.append((close + dist)/pre_close-1)

    
average = sum(avr_list) / len(avr_list)
print(average)
"""


period_arr=[1,2,3,4,5,6,7,8,9,10]
total_avr = []
for p in period_arr:
    idx = 0
    avr_list = []
    for close in df['Close']:
        idx = idx+1
        if(idx < (year+1)*p):
            continue

        pre_close = df['Close'][idx-(year*p)]
        #print(close, pre_close, close/pre_close-1)

        dist = 0
        for i in range(p):
            dist = dist + df['Close'][idx-(year*(i+1))]*dist_rate_f



        #avr_list.append((close + pre_close*dist_rate_f)/pre_close-1)
        avr_list.append((close + dist)/pre_close-1)


    try:
        average = sum(avr_list) / len(avr_list)
        print(p,average)
        total_avr.append(average)
    except ZeroDivisionError:
        print(p,0)
        total_avr.append(0)

t_avr = sum(total_avr) / len(total_avr)
print("total:",t_avr)



"""
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(df)
"""

