import pandas as pd
from DataManagement import DataManagement 

import queue

class Logic:
    
    def __init__(self):
        print("Start Logic")


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
                idx = idx+1
                continue


            stock = stock+invest_money/price
            org_money = org_money + invest_money
            ret_money = stock * price

            idx = idx+1

        #print(total_invest_money)
        #print(ret_money)

        ret = 0
        earn_money = 0
        if org_money != 0:
            ret = ret_money/org_money-1
            earn_money = ret_money-org_money



        #print(ret_money, org_money, price)

        return ret, org_money

    def logic_alpha_v4(self,df):
        alpha_df = df['Close']
        idx = 0
        q = queue.Queue()
        start_rate = 0.01
        var_rate = 0.03
        stock = 0
        org_money = 0
        invest_money = 10000
        
        start_flag = False
        continue_flag = False
        end_flag = True
        stop_cnt = 0
        stop_flag = False
        mod_rate = True
        
        ret_money = 0
        s_idx = 10000

        spare_money = 0


        def get_rate(ret,org):
            if org == 0:
                return 0
            else:
                return ret/org-1

        for price in alpha_df:
            invest_money = 0
            q.put(price)
            if idx < 51:
                idx = idx+1
                continue

            max_price = max(list(q.queue))

            if get_rate(price,max_price) < -(start_rate):
                start_flag = True
                continue_flag = True
            else:
                start_flag = False


            if start_flag or continue_flag:
                invest_money = 10000

            if stop_flag:
                continue_flag = False
                invest_money = 0

            
            if not start_flag and not continue_flag and not stop_flag:
                spare_money = spare_money+10000
                stock = stock + invest_money/price
                org_money = org_money + invest_money
            else:
                stock = stock + (spare_money+invest_money)/price
                org_money = org_money + invest_money + spare_money
                spare_money = 0

           
            #stock = stock + invest_money/price
            #org_money = org_money + invest_money

            ret_money = price*stock


            #print(price, max_price, price/max_price-1,invest_money, org_money, stock, ret_money, ret_money/org_money-1, start_rate, start_flag, stop_flag, continue_flag, spare_money )



            if get_rate(ret_money, org_money) > start_rate and not stop_flag:
                if invest_money != 0:
                    stop_flag = True
                    s_idx = idx+1
                    start_rate = start_rate + var_rate
                    continue_flag = False

            if s_idx == idx:
                stop_flag = False


            

            q.get()
            idx = idx+1
           

        ret = 0
        er_m = 0
        if org_money != 0:
            ret = ret_money/org_money-1
            er_m = ret_money-org_money

        return ret, er_m
        


    # 로직 alpha에 대한 수익률
    # alpha:
    # - 매수 : 고점 대비 -기준 수익률도달 시 매수 시작
    # - 현재 수익률이 기준 수익률 초과 시 매수 중지 and 기준 수익률 + n%
    # - 기준 수익률은 max 30%
    def logic_alpha_v3(self,df):
        alpha_df = df['Close']
        idx = 0
        q = queue.Queue()
        #start_rate = 0.25
        #var_rate = 0.05
        start_rate = 0.3
        var_rate = 0.01

        stock = 0
        org_money = 0
        invest_money = 10000
        
        start_flag = False
        continue_flag = False
        end_flag = True
        stop_cnt = 0
        stop_flag = False
        mod_rate = True
        
        ret_money = 0
        s_idx = 10000

        spare_money = 0


        def get_rate(ret,org):
            if org == 0:
                return 0
            else:
                return ret/org-1

        for price in alpha_df:
            invest_money = 0
            print(price)
            q.put(price)
            if idx < 51:
                idx = idx+1
                continue

            max_price = max(list(q.queue))

            if get_rate(price,max_price) < -(start_rate):
                start_flag = True
                continue_flag = True
            else:
                start_flag = False


            if start_flag or continue_flag:
                invest_money = 10000

            if stop_flag:
                continue_flag = False
                invest_money = 0

            """
            if not start_flag and not continue_flag and not stop_flag:
                spare_money = spare_money+10000


            if start_flag and continue_flag:
                spare_money = 0
            """
            stock = stock + invest_money/price
            org_money = org_money + invest_money

            ret_money = price*stock


            #print(price, max_price, price/max_price-1,invest_money, org_money, stock, ret_money, ret_money/org_money-1, start_rate, start_flag, stop_flag, continue_flag, spare_money )



            if get_rate(ret_money, org_money) > start_rate and not stop_flag:
                if invest_money != 0:
                    stop_flag = True
                    s_idx = idx+1
                    start_rate = start_rate + var_rate
                    if start_rate > 0.3:
                        start_rate = 0.3
                    continue_flag = False

            if s_idx == idx:
                stop_flag = False


            

            q.get()
            idx = idx+1
           

        ret = 0
        er_m = 0
        if org_money != 0:
            ret = ret_money/org_money-1
            er_m = ret_money-org_money

        return ret, org_money
        








    # 로직 alpha에 대한 수익률
    # alpha:
    # - 매수 : 고점 대비 -기준 수익률도달 시 매수 시작
    # - 현재 수익률이 기준 수익률 초과 시 매수 중지 and 기준 수익률 + n%
    def logic_alpha(self, df):
        alpha_df = df['Close']
        q = queue.Queue()

        #print(alpha_df)

        idx = 0
        stock = 0
        start_rate = 0.05
        var_rate = 0.01
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
                start_rate = start_rate + var_rate
                #print(price, max_price, price/max_price-1, stock, org_money, ret_money, ret_money/org_money-1, total_invest_money, start_rate)
                #print(ret_money/total_invest_money -1)
                income_rate.append(ret_money/total_invest_money -1)
                
            
            q.get()

            idx = idx+1


        ret = 0
        if len(income_rate) > 0:
            ret = income_rate[-1]

        return ret

    # 로직 alpha 의 변형에 대한 수익률
    # alpha:
    # - 매수 : 매도한 금액 그대로 매수 (기준-수익률도달 시)
    # - 매도 : 기준 수익률 이상 도달 시 매도
    #          매도 후 기준 수익률 +1%
    def logic_alpha_v2(self, df):
        alpha_df = df['Close']
        q = queue.Queue()

        #print(alpha_df)

        idx = 0
        stock = 0
        start_rate = 0.05
        invest_money = 10000
        total_invest_money = 0
        org_money = 10000
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
            
            if (price/max_price-1) < -(start_rate) and investing_flag == False:
                investing_flag = True
                stock = invest_money/price

            ret_price = price*stock


            #print(price,ret_price,invest_money,ret_price/invest_money-1)


            if (ret_price/invest_money-1) > start_rate and investing_flag == True:
                income_rate.append(ret_price/org_money -1)
                investing_flag = False
                invest_money = ret_price
                start_rate = start_rate+0.01
                #start_rate = start_rate+0.05
                stock = 0


            """
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
            """    
            
            q.get()

            idx = idx+1


        
        ret = 0
        if len(income_rate) > 0:
            ret = income_rate[-1]

        print(ret)

        return ret
        

    # 로직 beta에 대한 수익률
    # beta:
    # 1~n년 까지의 수익률의 평균치를 구함
    # 배당 포함
    def logic_beta(self, df):
        period_arr=range(1,6)
        #period_arr=[1,2,3,4,5,6,7,8,9,10]
        #period_arr=[1,2,3,4,5]
        total_avr = []
        year = 51
        stock = 1
        div_queue = queue.Queue()
        for p in period_arr:
            idx = 0
            avr_list = []
            for close in df['Close']:

                div = df['Dividends'][idx]
                if div != 0.0:
                    #div_arr.append(div)
                    #div_st = div/close
                    div_queue.put(div/close)
                    if idx > year and div_queue.empty() == False:
                        div_queue.get()
                        

                """
                if idx%((year) * p) == 0 and idx != 0:
                    #print('clear')
                    #print(p,idx, list(div_queue.queue)) 
                    stock = 1
                    #if div_queue.empty() == False:
                    #    div_queue.get()
                """


                if(idx < (year+1)*p):
                    idx = idx+1
                    continue

                #print(p,idx, list(div_queue.queue)) 
                pre_close = df['Close'][idx-(year*p)]
                #print(close, pre_close, close/pre_close-1)

                #if self.df['Dividends'][idx-(year*p)] != 0.0:
                #    div_arr.append(self.df['Dividends'][idx-(year*p)])


                div_list = list(div_queue.queue)
                for d in div_list:
                    stock = stock + d

                #stock = stock + (self.df['Dividends'][idx]/close)
               
                
                """
                dist = 0
                for i in range(p):
                    dist = dist + self.df['Close'][idx-(year*(i+1))]*self.dist
                """

                #avr_list.append((close + dist)/pre_close-1)
                avr_list.append((close*stock)/pre_close - 1)

                stock = 1

                idx = idx+1

            try:
                average = sum(avr_list) / len(avr_list)
                #print(p,average)
                total_avr.append(average)
            except ZeroDivisionError:
                #print(p,0)
                total_avr.append(0)

            #print(div_queue)
            #print(list(div_queue.queue)) 

        t_avr = sum(total_avr) / len(total_avr)

        """
        j = 0
        for d in total_avr:
            print(j+1, d)
            j = j+1
        """
        #print(self.name, self.ticker ,round(t_avr*100,2), round(min(total_avr)*100,2), round(max(total_avr)*100,2))

        return t_avr

    # 로직 beta의 변형에 대한 수익률
    # beta:
    # 특정 n년의 수익률의 평균치를 구함
    # 배당 포함
    def logic_beta_v2(self, df):
        #total_avr = []
        year = 51
        stock = 1
        div_queue = queue.Queue()
        avr_list = []

        p = 5

        idx = 0
        for close in df['Close']:
            div = df['Dividends'][idx]

            if div != 0.0:
                #div_arr.append(div)
                #div_st = div/close
                div_queue.put(div/close)
                if idx > (year+1)*p and div_queue.empty() == False:
                    div_queue.get()

            if(idx < (year+1)*p):
                idx = idx+1
                continue

            #print(close, div)
            #print(list(div_queue.queue)) 


            pre_close = df['Close'][idx-(year*p)]

            div_list = list(div_queue.queue)
            for d in div_list:
                stock = stock + d

               
            avr_list.append((close*stock)/pre_close - 1)
            stock = 1

            idx = idx+1

        try:
            t_avr = sum(avr_list) / len(avr_list)
        #print(self.name, self.ticker ,round(t_avr*100,2), round(min(avr_list)*100,2), round(max(avr_list)*100,2))
        except ZeroDivisionError:
            t_avr = 0
        #print(self.name, self.ticker ,0, 0,0)

        return t_avr


    # 로직 theta의 수익률
    # theta:
    #  - 이전 3개월 최고가 대비 -n% 이하일 경우 매수
    def logic_theta(self, df):
        theta_df = df['Close']
        q = queue.Queue()

        idx = 0
        ret_money = 0
        stock = 0
        org_money = 0
        target_rate = 0.25

        #period = 37
        #period = 25
        period = -1
        
        for price in theta_df:
            #print(price)
            if idx > period:
                q.put(price)

            if idx < 51:
                idx = idx+1
                continue

                
            max_price = max(list(q.queue))
            #max_price = sum(list(q.queue)) / len(list(q.queue))
        
            if (price/max_price-1) < -(target_rate):
                stock = stock + 10000/price
                org_money = org_money+10000

            ret_money = stock*price    

            #print(price, price/max_price-1, max_price)
            #print(org_money, ret_money)

            q.get()
            idx = idx+1

        
        
        ret = 0
        if org_money != 0:
            ret = ret_money/org_money-1
        #if len(income_rate) > 0:
        #    ret = income_rate[-1]

        #print(ret)

        return ret, org_money

    # 로직 gamma의 수익률
    # gamma:
    #    - 시작 시점에 기준 수익률 미만일 경우계속 매수
    #    - 기준 수익률 도달 후 매수 중지, 현재 수익률을 target 으로 설정
    #    - target 대비 -n% 이면 매수 시작
    #    - target 대비 +n% 이면 매수 종료, 현재 수익률을 target으로 재 설정
    #    - 반복
    def logic_gamma(self,df):
        gamma_df = df['Close']
        idx = 0
        q = queue.Queue()
        start_rate = 0.3
        var_rate = 0.05
        stock = 0
        org_money = 0
        invest_money = 10000
       

        pre_rate = 0
        pre_var_rate = 0
        target_rate = 0
        ret_money = 0
        update_target = True
        first_flag = True
        investing_flag = False


        def get_rate(ret,org):
            if org == 0:
                return 0
            else:
                return ret/org-1

        for price in gamma_df:
            invest_money = 0
            #investing_flag = False
            if idx < 51:
                idx = idx+1
                continue
            
            if pre_var_rate < -(var_rate):
                investing_flag = True

            if pre_rate < start_rate and first_flag:
                invest_money = 10000
            else:
                if update_target:
                    target_rate = pre_rate
                    update_target = False
                    first_flag = False
                    investing_flag = False

            if investing_flag:
                invest_money = 10000

            stock = stock + invest_money/price
            org_money = org_money + invest_money

            ret_money = price*stock

            pre_var_rate = get_rate(ret_money, org_money) - target_rate
            #print(price, invest_money, org_money, stock, ret_money, ret_money/org_money-1, target_rate, pre_var_rate)
            pre_rate = get_rate(ret_money, org_money)


            if pre_var_rate > var_rate and investing_flag and not first_flag:
                investing_flag = False
                target_rate = pre_rate

            idx = idx+1
           

        ret = 0
        er_m = 0
        if org_money != 0:
            ret = ret_money/org_money-1
            er_m = ret_money-org_money

        return ret, org_money


    def logic_delta(self,df):
        delta_df = df['Close']
        idx = 0

        y_rate_list = []
        ret_list = []

        def get_rate(ret,org):
            if org == 0:
                return 0
            else:
                return ret/org-1

        for price in delta_df:
            if idx < 51:
                idx = idx+1
                continue

            cur_price = price
            past_price = delta_df[idx-51]
            
            if idx % 51 == 0 and idx > 51:
                #print(y_rate_list)
                size = len(y_rate_list)
                var = sum(y_rate_list)
                ret_list.append(str(var/size))
                y_rate_list = []
                y_rate_list.append(get_rate(cur_price, past_price))
            else:
                y_rate_list.append(get_rate(cur_price, past_price))

            idx = idx+1
           
        size = len(y_rate_list)
        var = sum(y_rate_list)
        ret_list.append(str(var/size))
        ret = " ".join(ret_list)

        return ret

        """
        ret = 0
        er_m = 0
        if org_money != 0:
            ret = ret_money/org_money-1
            er_m = ret_money-org_money

        return ret, org_money
        """
        
def back_test_dca(file_name):
    obj = Logic()
    obj_dm = DataManagement()

    df = obj_dm.load_data_market_cap(file_name)

    for name, code in zip(df['종목명'],df['Code']):
        tmp_df = obj_dm.load_data_from_yf(code)

        dca, dca_m = obj.logic_dca(tmp_df)

        print(name, dca)


        

def back_test_alpha(file_name):
    obj = Logic()
    obj_dm = DataManagement()

    df = obj_dm.load_data_market_cap(file_name)

    for name, code in zip(df['종목명'],df['Code']):
        tmp_df = obj_dm.load_data_from_yf(code)

        dca, dca_m = obj.logic_dca(tmp_df)
        alpha, alpha_m = obj.logic_alpha_v3(tmp_df)

        #print(alpha/dca - 1)
    
        
        
        if alpha_m/dca_m < 0.3:
            print(0)
        else:
            print(alpha/dca-1)
        

    """
    obj = Logic()
    obj_dm = DataManagement()

    df = obj_dm.load_data_market_cap(file_name)

    for name, code in zip(df['종목명'],df['Code']):
        tmp_df = obj_dm.load_data_from_yf(code)

        dca, dca_m = obj.logic_dca(tmp_df)
        alpha, alpha_m = obj.logic_alpha_v3(tmp_df)

        #print(name, dca, alpha, dca_er_m, alpha_er_m, alpha_er_m/dca_er_m -1 )
        if alpha_m/dca_m < 0.2:
            print(0)
        else:
            print(alpha/dca-1)
    """

def back_test_theta(file_name):
    obj = Logic()
    obj_dm = DataManagement()

    df = obj_dm.load_data_market_cap(file_name)

    for name, code in zip(df['종목명'],df['Code']):
        tmp_df = obj_dm.load_data_from_yf(code)

        dca, dca_m = obj.logic_dca(tmp_df)
        theta, theta_m = obj.logic_theta(tmp_df)

        #print(name, dca, alpha, dca_er_m, alpha_er_m, alpha_er_m/dca_er_m -1 )
        if theta_m/dca_m < 0.3:
            print(0)
        else:
            print(theta/dca-1)

def back_test_gamma(file_name):
    obj = Logic()
    obj_dm = DataManagement()

    df = obj_dm.load_data_market_cap(file_name)

    for name, code in zip(df['종목명'],df['Code']):
        tmp_df = obj_dm.load_data_from_yf(code)

        dca, dca_m = obj.logic_dca(tmp_df)
        gamma, gamma_m = obj.logic_gamma(tmp_df)

        #print(name, dca, alpha, dca_er_m, alpha_er_m, alpha_er_m/dca_er_m -1 )
        if gamma_m/dca_m < 0.3:
            print(0)
        else:
            print(gamma/dca-1)

def back_test_delta(file_name):
    obj = Logic()
    obj_dm = DataManagement()

    df = obj_dm.load_data_market_cap(file_name)

    for name, code in zip(df['종목명'],df['Code']):
        tmp_df = obj_dm.load_data_from_yf(code)

        delta = obj.logic_delta(tmp_df)
        print(name, delta)



def back_test_one(name):
    code = obj_dm.name_to_code(name)
    #code = 'msft'
    df = obj_dm.load_data_from_yf(code)
 
    ret = obj.logic_alpha(df)
    print(ret)

    #ret = obj.logic_alpha_v3(df)
    #ret = obj.logic_dca(df)
    
    #ret = obj.logic_delta(df)

    #print(ret)




if __name__ == '__main__':
    obj = Logic()
    
    obj_dm = DataManagement()
    
    df = obj_dm.load_data_market_cap('market_cap_kosdaq.csv')


    #back_test_dca('back_test.csv')

    #back_test_alpha('back_test.csv')

    #back_test_theta('back_test.csv')
    #back_test_gamma('back_test.csv')
    #back_test_delta('back_test.csv')
    """
    back_test_alpha('market_cap_kospi2.csv')
    """

    """
    back_test_theta('market_cap_kosdaq.csv')
    back_test_theta('market_cap_kospi2.csv')
    """


    #back_test_one('한화에어로스페이스')
    back_test_one('삼성전자')



    
    
    
    
    """
    
    code = obj_dm.name_to_code('삼성전자')
    #code = 'msft'
    df = obj_dm.load_data_from_yf(code)
 
    #ret = obj.logic_alpha(df)
    #print(ret)

    ret = obj.logic_alpha_v3(df)
    print(ret)
    
    
    
    #ret = obj.logic_dca(df)
    #print(ret)
    """
    """

    ret = obj.logic_alpha(df)
    print(ret)

    ret = obj.logic_beta_v2(df)
    print(ret)
    """


    """
    ret = obj.logic_alpha(df)
    print(ret)

    ret = obj.logic_beta(df)
    print(ret)

    ret = obj.logic_beta_v2(df)
    print(ret)
    obj.logic_alpha_v2(df)
    #print(ret)
    """


