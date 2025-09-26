
import pandas as pd
import queue

import yfinance as yf

class Invest_logic:
    def __init__(self):
        print("invest logic")


    def load_data_from_excel(self, file_name):
        print(file_name)
        self.df = pd.read_excel(file_name)
        #print(self.df)

    def load_data_from_yf(self, code):
        code = code + '.KS'
        #print(code)
        data = yf.Ticker(code)
        self.df = data.history(interval="1wk", start="2018-01-01")
        #price_df = fdr.DataReader('069500, 229200')
        #print(self.df['Close'])



    def logic_dca(self):
        dca_df = self.df['Close']

        invest_money = 10000
        stock = 0
        idx = 0
        org_money = 0
        ret_money = 0

        for price in dca_df:
            if idx < 51:
                idx = idx+1
                continue


            stock = stock+invest_money/price
            org_money = org_money + invest_money
            ret_money = stock * price

            idx = idx+1

        #print(total_invest_money)
        #print(ret_money)

        return ret_money/org_money-1





    def logic_alpha(self):
        alpha_df = self.df['Close']
        q = queue.Queue()

        #print(alpha_df)

        idx = 0
        stock = 0
        start_rate = 0.05
        invest_money = 10000
        total_invest_money = 0
        org_money = 0
        ret_money = 0
        sell_money = 0
        investing_flag = False
        income_rate = []
        for price in alpha_df:
            #print(price)
            q.put(price)
            if idx < 51:
                idx = idx+1
                continue

                
            max_price = max(list(q.queue))
            
            if (price/max_price-1) < -(start_rate):
                investing_flag = True


            if investing_flag:
                if sell_money == 0:
                    stock = stock+invest_money/price
                    org_money = org_money + invest_money
                    total_invest_money = total_invest_money + invest_money
                else:
                    stock = (sell_money)/price
                    org_money = sell_money
                    sell_money = 0

                ret_money = stock * price
            #max_price = max(tmp_list)

            if(org_money == 0):
                q.get()
                idx = idx+1
                continue

            #print(ret_money, org_money)
            if ret_money/org_money-1 > start_rate and investing_flag:
                investing_flag = False
                sell_money = ret_money
                start_rate = start_rate + 0.01
                #print(price, max_price, price/max_price-1, stock, org_money, ret_money, ret_money/org_money-1, total_invest_money, start_rate)
                #print(ret_money/total_invest_money -1)
                income_rate.append(ret_money/total_invest_money -1)
                
            
            q.get()

            idx = idx+1


        ret = 0
        if len(income_rate) > 0:
            ret = income_rate[-1]

        return ret
        

if __name__ == '__main__':
    obj = Invest_logic()
    #obj.load_data_from_excel('samsung_week.xlsx')
    #print(obj.logic_alpha())
    #print(obj.logic_dca())

    
    f = open('market_cap_kospi.txt','r')

    f_list = [s.replace("'","") for s in f.readlines()]
    idx = 0
    for line in f_list:
        obj.load_data_from_yf(line.split(',')[0])
        #ret = obj.logic_alpha()

        print(line.split(',')[1].split('\n')[0], obj.logic_alpha(), obj.logic_dca())

        #if idx == 10:
        #    break

        idx = idx+1
    
        




 
