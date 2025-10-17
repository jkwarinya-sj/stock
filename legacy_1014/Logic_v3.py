import pandas as pd
from DataManagement import DataManagement 
import logging
import queue
from Log import Log


log = Log(logging.DEBUG).get_logger()

class Logic:
    
    def __init__(self):
        log.info("Start Logic")

    # DCA 방식으로 투자 시 수익률
    def logic_dca(self, df):
        dca_df = df['Close']

        invest_money = 10000
        stock = 0
        idx = 0
        org_money = 0
        ret_money = 0

        for price in dca_df:
            if idx < 51:
                #print(price)
                idx = idx+1
                continue


            stock = stock+invest_money/price
            org_money = org_money + invest_money
            ret_money = stock * price

            idx = idx+1

            #print(price, org_money, ret_money, self.get_rate(ret_money, org_money))

        #print(total_invest_money)
        #print(ret_money)

        ret = 0
        earn_money = 0
        if org_money != 0:
            ret = ret_money/org_money-1
            earn_money = ret_money-org_money



        #print(ret_money, org_money, price)

        #return ret, org_money
        return ret



if __name__ == '__main__':
    obj = Logic()




