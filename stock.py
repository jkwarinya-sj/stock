import pandas as pd
import FinanceDataReader as fdr

df2 = pd.read_csv("investment.csv")
#print(df2)


#print(df2.sort_values('투자금'))

#print(df2.loc[2,'투자금'])

for idx in range(0,len(df2)):
    code = df2.loc[idx,'종목코드']
    name = df2.loc[idx,'종목명']
    percent = df2.loc[idx, '보유량']
    #print(name)
    price_df = fdr.DataReader(code.replace('C',''))
    #print(price_df)
    today = price_df.iloc[-1]['Close']
    yesterday = price_df.iloc[-2]['Close']
    
    #ret = today-yesterday
    #print(ret, round(ret*percent,0))
    
    ret = today * percent
    #print(ret, round(ret,0))
    #print(name, round(ret,0))
    
    inv = df2.loc[idx, '투자금']
    #df2.loc[idx, '투자금'] = inv + round(ret*percent,0)
    df2.loc[idx, '투자금'] = round(ret,0)
    
    
  
#print(df2)

df2.to_csv('investment.csv',encoding = 'utf-8-sig',index = False)
print(df2.sort_values('투자금').iloc[:5]['종목명'])
    


#for data in df2.iloc:
#    print(data['종목명'])
#    data['투자금'] = 100

"""
class stock_datas:
    def __init__(self, n, p, name, price):
        #print('stock_datas')
        self.number = n
        self.percent = p
        self.name = name
        self.price = price

print('test')

stock_list  = [
stock_datas('071670', 0.38505, 'SK텔레콤', 19984),
stock_datas('029780', 0.512457, '삼성카드', 19832),
stock_datas('381970', 1.491752, '케이카', 19646)
]

print(stock_list)


for d in stock_list:
    print(d.name)

#price_df = fdr.DataReader('069500, 229200')
price_df = fdr.DataReader('017670')

print(price_df.iloc[-2]['Close'])
print(price_df.iloc[-1]['Close'])
print(price_df  )

#sns.set_style('whitegrid')
#price_df.plot()
#plt.show()
"""
