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
                print(price)
                idx = idx+1
                continue


            stock = stock+invest_money/price
            org_money = org_money + invest_money
            ret_money = stock * price

            idx = idx+1

            print(price, org_money, ret_money, self.get_rate(ret_money, org_money))

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

    def get_rate(self, ret, org):
        if org == 0:
            return 0
        else:
            return ret/org-1

    # 로직 alpha에 매수 여부
    def logic_alpha_check_buy(self,df):
        #print('logic alpha check buy run')
        alpha_df = df['Close']
        idx = 0
        q = queue.Queue()

        start_rate = 0.05
        buy = False

        for price in alpha_df:
            q.put(price)
            if idx < 51:
                #print(price)
                idx = idx+1
                continue

            max_price = max(list(q.queue))
            cpm = self.get_rate(price, max_price)

            if cpm < -(start_rate):
                buy = True
            else:
                buy = False

            #print(price, investing)

            q.get()
            idx = idx+1

        if buy:
            return 'buy'
        else:
            return '-'



    # 로직 alpha에 매도 여부
    def logic_alpha_check_sell(self, df, org_m, stock):
        #print('logic alpha check sell run')
        alpha_df = df['Close']
        q = queue.Queue()
        idx = 0

        stock = stock
        org_m = org_m
        sell = False

        end_rate = 0.15
        for price in alpha_df:
            q.put(price)
            #print(price)
            if idx < 51:
                idx = idx+1
                continue

            ret_m = price*stock
            ret_rate = self.get_rate(ret_m, org_m)

            if ret_rate > end_rate:
                sell = True
            else:
                sell = False

            #print(price, stock, ret_m, org_m, ret_rate, sell)
            
            q.get()
            idx = idx+1

        if sell:
            return 'sell'
        else:
            return '-'



    
    # 로직 alpha에 대한 수익률
    # alpha:
    # - 매수 : 52주 고점 대비 -start_rate 충족 시 매수
    # - 매도 : 매수가 대비 +end_rate 충족 시 매도
    def logic_alpha(self,df):
        #print('logic alpha run')
        alpha_df = df['Close']
        idx = 0
        q = queue.Queue()

        org_m = 1000000
        ret_m = 0
        tmp_m = 0
        stock = 0
        invest_m = 0

        start_rate = 0.05
        end_rate = 0.15
        var_rate = 0.00
        investing = False
        wait_idx = 0
        first_flag = True


        for price in alpha_df:
            q.put(price)
            if idx < 51:
                print(price)
                idx = idx+1
                continue

            max_price = max(list(q.queue))
            cpm = self.get_rate(price, max_price)

            """
            if first_flag and cpm < -(start_rate):
                investing = True
                invest_m = org_m
                stock = invest_m/price
                first_flag = False
            """

            #if cpm < -(start_rate) and not investing and wait_idx==0 and not first_flag:
            if cpm < -(start_rate) and not investing and wait_idx==0:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price


            ret_m = price*stock
            ret_rate = self.get_rate(ret_m, invest_m)
                            

            print(price, max_price, cpm, invest_m, stock,ret_m, ret_rate, investing)

            if ret_rate > end_rate:
                investing = False
                wait_idx = 2
                invest_m = 0
                stock = 0
                tmp_m = ret_m
                #start_rate = start_rate + 0.01
                end_rate = end_rate + var_rate


            if wait_idx > 0:
                wait_idx = wait_idx-1
            
            q.get()
            idx = idx+1


        if ret_m == 0:
            ret_m = tmp_m

        #print(org_m, ret_m, self.get_rate(ret_m, org_m))


        ret = self.get_rate(ret_m, org_m)
        return ret


    # 로직 gamma의 매수 여부
    def logic_gamma_check_buy(self, df):
        #print('logic gamma check buy run')
        gamma_df = df['Close']
        q = queue.Queue()

        idx = 0
        target_rate = 0.15

        buy = False
        
        for price in gamma_df:
            q.put(price)
            if idx < 51:
                idx = idx+1
                #print(price)
                continue

            max_price = max(list(q.queue))
            cpm = self.get_rate(price, max_price)
        
            if cpm <= -(target_rate):
                buy = True
            else:
                buy = False

            #print(price, buy)
            
            q.get()
            idx = idx+1

        if buy:
            return 'buy'
        else:
            return '-'



    # 로직 gamma의 매도 여부
    def logic_gamma_check_sell(self, df, org_m, stock):
        #print('logic gamma check sell run')
        gamma_df = df['Close']
        q = queue.Queue()
        idx = 0
        
        sell = False
        
        for price in gamma_df:
            q.put(price)
            if idx < 51:
                idx = idx+1
                continue
                
            max_price = max(list(q.queue))
            cpm = self.get_rate(price, max_price)
        
            if cpm >= 0:
                sell = True
            else:
                sell = False
            
            #print(price, sell, cpm)

            q.get()
            idx = idx+1

        if sell:
            return 'sell'
        else:
            return '-'


    # 로직 gamma의 수익률
    # gamma:
    #  - 매수: 이전 12개월 최고가 대비 -n% 이하일 경우 매수
    #   - 매도: 이전 12개월 최고가 대비 + 이면 매도
    def logic_gamma(self, df):
        print('logic gamma run')
        gamma_df = df['Close']
        q = queue.Queue()

        idx = 0
        ret_money = 0
        stock = 0
        org_m = 1000000
        invest_m = 0
        tmp_m = 0
        target_rate = 0.15

        wait_idx = 0
        investing = False

        #period = 37
        #period = 25
        period = -1
        
        for price in gamma_df:
            #print(price)
            if idx > period:
                q.put(price)

            if idx < 51:
                idx = idx+1
                continue

                
            max_price = max(list(q.queue))
            #max_price = sum(list(q.queue)) / len(list(q.queue))
            cpm = self.get_rate(price, max_price)
        
            if cpm <= -(target_rate) and not investing and wait_idx==0:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = self.get_rate(ret_m, invest_m)

            #print(price, max_price, cpm, invest_m, stock,ret_m, ret_rate, investing)

            if cpm >= 0 and investing:
                investing = False
                wait_idx = 2
                invest_m = 0
                stock = 0
                tmp_m = ret_m


            if wait_idx > 0:
                wait_idx = wait_idx-1


            #print(price, price/max_price-1, max_price)
            #print(org_money, ret_money)

            q.get()
            idx = idx+1

        if ret_m == 0:
            ret_m = tmp_m

        ret = self.get_rate(ret_m, org_m)
        return ret

    # 로직 delta의 매수 여부
    def logic_delta_check_buy(self, df):
        #print('logic delta check buy run')
        delta_df = df['Close']

        idx = 0
        buy = False
 
        for price in delta_df:
            if idx < 51:
                idx = idx+1
                continue

            avr_price = (price+delta_df[idx-1])/2
            cpm = self.get_rate(price, avr_price)


            if cpm < 0:
                buy = True
            else:
                buy = False

            #print(price, avr_price, buy)

            idx = idx+1

        if buy:
            return 'buy'
        else:
            return '-'



    # 로직 delta의 매도 여부
    def logic_delta_check_sell(self, df, org_m, stock):
        #print('logic delta check sell run')
        delta_df = df['Close']

        idx = 0
        sell = False

        target_rate = 0.15
        stock = stock
        org_m = org_m
 
        for price in delta_df:
            if idx < 51:
                idx = idx+1
                continue

            avr_price = (price+delta_df[idx-1])/2
            cpm = self.get_rate(price, avr_price)

            ret_m = price*stock
            ret_rate = self.get_rate(ret_m, org_m)


            if ret_rate > target_rate:
                sell = True
            else:
                sell = False

            #print(price, org_m, ret_m, stock, ret_rate, sell)

            #print(price, sell)

            idx = idx+1

        if sell:
            return 'sell'
        else:
            return '-'





    # 로직 delta의 수익률
    # delta:
    #  - 매수: 10일 평균 -% 이하일 경우 매수
    #  - 매도: target_rate + 이면 매도
    def logic_delta(self, df):
        print('logic delta run')
        delta_df = df['Close']

        idx = 0
        investing = False

        org_m = 1000000
        invest_m = 0
        target_rate = 0.15
 

        wait_idx = 0

        ret_money = 0
        stock = 0
        tmp_m = 0

        
        for price in delta_df:

            if idx < 51:
                idx = idx+1
                continue

            avr_price = (price+delta_df[idx-1])/2
            cpm = self.get_rate(price, avr_price)

            if cpm < 0 and not investing and wait_idx==0:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = self.get_rate(ret_m, invest_m)


            #print(price, avr_price, cpm, invest_m, stock, ret_m, ret_rate, investing)

            if ret_rate > target_rate:
                investing = False
                stock = 0
                tmp_m = ret_m
                wait_idx = 2

            if wait_idx > 0:
                wait_idx = wait_idx-1


            idx = idx+1


        if ret_m == 0:
            ret_m = tmp_m

        ret = self.get_rate(ret_m, org_m)
        return ret


    # 로직 epsilon의 매수 여부
    def logic_epsilon_check_buy(self, df):
        #print('logic epsilon check buy run')
        epsilon_df = df['Close']

        idx = 0
        sum_cpm=0
        buy = False

        
        for price in epsilon_df:

            if idx < 51:
                idx = idx+1
                continue

            cpm = self.get_rate(price,epsilon_df[idx-1])
            sum_cpm = sum_cpm+cpm
            
            if sum_cpm < 0:
                buy = True
            else:
                buy = False

            if sum_cpm > 0.3:
                sum_cpm = 0

            #print(price,cpm, sum_cpm,buy)
            
            idx = idx+1

        if buy:
            return 'buy'
        else:
            return '-'



    # 로직 epsilon의 매도 여부
    def logic_epsilon_check_sell(self, df, org_m, stock):
        #print('logic epsilon check sell run')
        epsilon_df = df['Close']

        idx = 0
        sell = False

        org_m = org_m
        stock = stock
        target_rate = 0.15
        
        for price in epsilon_df:

            if idx < 51:
                idx = idx+1
                continue

            ret_m = price*stock
            ret_rate = self.get_rate(ret_m, org_m)
            
            if ret_rate > target_rate:
                sell = True
            else:
                sell = False

            #print(price, org_m, stock, ret_m, ret_rate, sell)

            
            idx = idx+1

        if sell:
            return 'sell'
        else:
            return '-'



 

    # 로직 epsilon의 수익률
    # epsilon:
    #  - 매수: 누적 등락률이 -% 일 경우 매수
    #  - 매도: target_rate + 이면 매도
    #  - 누적 등락률이 0.3 이상이면 0으로 초기화
    def logic_epsilon(self, df):
        print('logic epsilon run')
        epsilon_df = df['Close']

        idx = 0
        investing = False

        org_m = 1000000
        invest_m = 0
        target_rate = 0.15
        sum_cpm=0
 

        wait_idx = 0

        ret_money = 0
        stock = 0
        tmp_m = 0

        
        for price in epsilon_df:

            if idx < 51:
                idx = idx+1
                continue

            #avr_price = (price+delta_df[idx-1])/2
            cpm = self.get_rate(price,epsilon_df[idx-1])
            sum_cpm = sum_cpm+cpm

            
            if sum_cpm < 0 and not investing and wait_idx==0:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = self.get_rate(ret_m, invest_m)
            

            #print(price, cpm, sum_cpm, invest_m, stock, ret_m, ret_rate, investing)

            
            if ret_rate > target_rate:
                investing = False
                stock = 0
                tmp_m = ret_m
                sum_cpm = 0
                wait_idx = 2 

            if sum_cpm > 0.3:
                sum_cpm = 0

            if wait_idx > 0:
                wait_idx = wait_idx-1


            
            idx = idx+1


        if ret_m == 0:
            ret_m = tmp_m

        ret = self.get_rate(ret_m, org_m)
        return ret


    # 로직 zeta의 수익률
    # zeta:
    #  - 매수: 누적 등락률이 -% 일 경우 매수
    #  - 매도: target_rate + 이면 매도
    #  - 누적 등락률이 0.3 이상이면 0으로 초기화
    def logic_zeta(self, df):
        print('logic epsilon run')
        zeta_df = df['Close']

        idx = 0
        investing = False

        org_m = 1000000
        invest_m = 0
        target_rate = 0.15
        sum_cpm=0
 

        wait_idx = 0

        ret_money = 0
        stock = 0
        tmp_m = 0

        
        for price in zeta_df:

            if idx < 51:
                print(price)
                idx = idx+1
                continue

            #avr_price = (price+delta_df[idx-1])/2
            cpm = self.get_rate(price,zeta_df[idx-1])
            sum_cpm = sum_cpm+cpm

            
            if sum_cpm < 0 and not investing and wait_idx==0:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = self.get_rate(ret_m, invest_m)
            

            print(price, cpm, sum_cpm, invest_m, stock, ret_m, ret_rate, investing)

            
            if ret_rate > target_rate:
                investing = False
                stock = 0
                tmp_m = ret_m
                sum_cpm = 0
                wait_idx = 2 

            if sum_cpm > 0.3:
                sum_cpm = 0

            if wait_idx > 0:
                wait_idx = wait_idx-1


            
            idx = idx+1


        if ret_m == 0:
            ret_m = tmp_m

        ret = self.get_rate(ret_m, org_m)
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

    def choose_logic(self, file_name):
        obj_dm = DataManagement()
        df = obj_dm.load_data_market_cap(file_name)
        
        logic_name_list = ['dca','alpha','gamma','delta','epsilon']
        logic_list = []
        set_zero = []


        for name, code in zip(df['종목명'],df['Code']):
            tmp_df = obj_dm.load_data_from_yf(code)
            
            ret_list = [obj.logic_dca(tmp_df), obj.logic_alpha(tmp_df),obj.logic_gamma(tmp_df), obj.logic_delta(tmp_df), obj.logic_epsilon(tmp_df)]

            ret_list.index(max(ret_list))

            #print(ret_list)
            #print(name, logic_name_list[ret_list.index(max(ret_list))])
            logic_list.append(logic_name_list[ret_list.index(max(ret_list))])
            set_zero.append(0)


        df['logic'] = logic_list
        df['price'] = set_zero
        df['stock'] = set_zero

        #print(df)
        df.to_csv('./datas/final_data.csv',sep=',',encoding="utf-8-sig")





        

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

        #dca, dca_m = obj.logic_dca(tmp_df)
        alpha = obj.logic_alpha(tmp_df)

        print(alpha)


        #print(alpha/dca - 1)
    
        
        
        """
        if alpha_m/dca_m < 0.3:
            print(0)
        else:
            print(alpha/dca-1)
        """

def back_test_gamma(file_name):
    obj = Logic()
    obj_dm = DataManagement()

    df = obj_dm.load_data_market_cap(file_name)

    for name, code in zip(df['종목명'],df['Code']):
        tmp_df = obj_dm.load_data_from_yf(code)

        #dca, dca_m = obj.logic_dca(tmp_df)
        gamma = obj.logic_gamma(tmp_df)


        #print(gamma/dca - 1)
        print(gamma)
        #print(name, dca, alpha, dca_er_m, alpha_er_m, alpha_er_m/dca_er_m -1 )
        """
        if gamma_m/dca_m < 0.3:
            print(0)
        else:
            print(gamma/dca-1)
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


def back_test_delta(file_name):
    obj = Logic()
    obj_dm = DataManagement()

    df = obj_dm.load_data_market_cap(file_name)

    for name, code in zip(df['종목명'],df['Code']):
        tmp_df = obj_dm.load_data_from_yf(code)

        delta = obj.logic_delta(tmp_df)
        print(delta)

def back_test_epsilon(file_name):
    obj = Logic()
    obj_dm = DataManagement()

    df = obj_dm.load_data_market_cap(file_name)

    for name, code in zip(df['종목명'],df['Code']):
        tmp_df = obj_dm.load_data_from_yf(code)

        epsilon = obj.logic_epsilon(tmp_df)
        print(epsilon)




def back_test_one(name):
    obj_dm = DataManagement()
    code = obj_dm.name_to_code(name)
    #code = 'msft'

    #code = '012450.KS'
    #code = '005930.KS'
    #code = '196170.KQ'
    df = obj_dm.load_data_from_yf(code)
 
    """
    ret = obj.logic_alpha(df)
    print('alpha: ',ret)
    ret = obj.logic_gamma(df)
    print('gamma: ',ret)
    ret = obj.logic_delta(df)
    print('delta: ',ret)
    #print(ret)
    """
    #ret = obj.logic_epsilon(df)
    #print('epsilon: ',ret)

    #ret = obj.logic_zeta(df)
    #print('zeta: ',ret)

    ret = obj.logic_dca(df)
    print('dca: ',ret)


    #ret = obj.logic_alpha(df)
    #print('alpha: ',ret)



    #ret = obj.logic_alpha_v3(df)
    #ret = obj.logic_dca(df)
    
    #ret = obj.logic_epsilon(df)

    #print(ret)




if __name__ == '__main__':
    obj = Logic()

    #obj.choose_logic('back_test.csv')
    
    #obj_dm = DataManagement()
    
    #df = obj_dm.load_data_market_cap('market_cap_kosdaq.csv')
    back_test_one('RFHIC')

    #back_test_dca('back_test.csv')
    #back_test_alpha('back_test.csv')
    #back_test_gamma('back_test.csv')
    #back_test_delta('back_test.csv')
    #back_test_epsilon('back_test.csv')


    #back_test_theta('back_test.csv')
    """
    back_test_alpha('market_cap_kospi2.csv')
    """

    """
    back_test_theta('market_cap_kosdaq.csv')
    back_test_theta('market_cap_kospi2.csv')
    """



