
import pandas as pd
import queue


class Invest_logic:
    def __init__(self):
        print("invest logic")


    def load_data_from_excel(self, file_name):
        print(file_name)
        self.df = pd.read_excel(file_name)
        #print(self.df)

    def logic_alpha(self):
        alpha_df = self.df['Close']
        tmp_cnt = 52
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

            if ret_money/org_money-1 > start_rate and investing_flag:
                investing_flag = False
                sell_money = ret_money
                start_rate = start_rate + 0.01
                #print(price, max_price, price/max_price-1, stock, org_money, ret_money, ret_money/org_money-1, total_invest_money, start_rate)
                #print(ret_money/total_invest_money -1)
                income_rate.append(ret_money/total_invest_money -1)
                
            
            q.get()

            idx = idx+1

        print(income_rate[-1])

if __name__ == '__main__':
    obj = Invest_logic()
    obj.load_data_from_excel('tqqq_week.xlsx')
    obj.logic_alpha()


 
