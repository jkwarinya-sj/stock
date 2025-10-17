import pandas as pd
from DataManager import DataManager 
import logging
import queue
from LogManager import LogManager


log = LogManager.get_logger(logging.ERROR)


class Logic:
    
    def __init__(self):
        log.info("Start Logic")

    @classmethod
    def get_rate(cls, ret, org):
        if org == 0:
            return 0
        else:
            return ret/org-1

    @classmethod
    def check_status(cls, df, org_m, stock):
        if stock == 0:
            ret = cls._check_buy(df)
        else:
            ret = cls._check_sell(df, org_m, stock)

        return ret

    @classmethod
    def run_logic(cls, df):
        log.info('run_logic')

    
class Logic_dca(Logic):

    def __init__(self):
        log.info("Start Logic")

    # DCA 방식으로 투자 시 수익률
    @classmethod
    def run_logic(cls, df):
        dca_df = df['Close']

        invest_m = 10000
        stock = 0
        idx = 0
        org_m = 0
        ret_m = 0

        for price in dca_df:
            if idx < 51:
                log.debug(price)
                idx = idx+1
                continue

            stock = stock+invest_m/price
            org_m = org_m + invest_m
            ret_m = stock * price

            idx = idx+1

            log.debug("%s, %s, %s, %s", price, org_m, ret_m, cls.get_rate(ret_m, org_m))

        return cls.get_rate(ret_m, org_m)




class Logic_alpha(Logic):

    def __init__(self):
        log.info("Start Logic")

    # 로직 alpha에 대한 수익률
    # alpha:
    # - 매수 : 52주 고점 대비 -start_rate 충족 시 매수
    # - 매도 : 매수가 대비 +target_rate 충족 시 매도
    @classmethod
    def run_logic(cls, df):
        log.info('logic alpha run')
        alpha_df = df['Close']
        idx = 0
        q = queue.Queue()

        org_m = 1000000
        ret_m = 0
        tmp_m = 0
        stock = 0
        invest_m = 0

        start_rate = 0.05
        target_rate = 0.15
        investing = False
        first_flag = True

        for price in alpha_df:
            q.put(price)
            if idx < 51:
                log.debug(price)
                idx = idx+1
                continue

            max_price = max(list(q.queue))
            cpm = cls.get_rate(price, max_price)

            if cpm < -(start_rate) and not investing:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = cls.get_rate(ret_m, invest_m)

            log.debug("%s, %s, %s, %s, %s, %s, %s, %s", price, max_price, cpm, invest_m, stock, ret_m, ret_rate, investing)

            if ret_rate > target_rate:
                investing = False
                invest_m = 0
                stock = 0
                tmp_m = ret_m
            
            q.get()
            idx = idx+1


        if ret_m == 0:
            ret_m = tmp_m

        return cls.get_rate(ret_m, org_m)

    """
    @classmethod
    def check_status(cls, df, org_m, stock):
        if stock == 0:
            ret = self._check_buy(df)
        else:
            ret = self._check_sell(df, org_m, stock)

        return ret
    """

    # 로직 alpha에 매수 여부
    @classmethod
    def _check_buy(cls, df):
        log.info('logic alpha check buy run')
        alpha_df = df['Close']
        idx = 0
        q = queue.Queue()

        start_rate = 0.05
        buy = False

        for price in alpha_df:
            q.put(price)
            if idx < 51:
                idx = idx+1
                log.debug(price)
                continue

            max_price = max(list(q.queue))
            cpm = cls.get_rate(price, max_price)

            if cpm < -(start_rate):
                buy = True
            else:
                buy = False

            log.debug("%s, %s, %s, %s", price, max_price, cpm, buy)
            
            q.get()
            idx = idx+1

        if buy:
            return 'buy'
        else:
            return '-'

    # 로직alpha에 매도 여부
    @classmethod
    def _check_sell(cls, df, org_m, stock):
        log.info('logic alpha check sell run')
        alpha_df = df['Close']


        stock = stock
        org_m = org_m * stock
        sell = False
        target_rate = 0.15

        #price = alpha_df[-1]
        price = alpha_df.iloc[-1]

        ret_m = price*stock
        ret_rate = cls.get_rate(ret_m, org_m)

        if ret_rate > target_rate:
            sell = True
        else:
            sell = False

        log.info("%s, %s, %s, %s", org_m, ret_m, ret_rate, sell)


        if sell:
            return 'sell'
        else:
            return '-'


class Logic_gamma(Logic):

    def __init__(self):
        log.info("Start Logic")

    # 로직 gamma의 수익률
    # gamma:
    #  - 매수: 이전 12개월 최고가 대비 -n% 이하일 경우 매수
    #   - 매도: 이전 12개월 최고가 대비 + 이면 매도
    @classmethod
    def run_logic(cls, df):
        log.info('logic gamma run')
        gamma_df = df['Close']
        q = queue.Queue()

        idx = 0
        ret_m = 0
        stock = 0
        org_m = 1000000
        invest_m = 0
        tmp_m = 0
        target_rate = 0.15

        investing = False
        
        #period = 37

        for price in gamma_df:
            q.put(price)
            #if idx > period:
            #    q.put(price)


            if idx < 51:
                log.debug(price)
                idx = idx+1
                continue
                
            max_price = max(list(q.queue))
            cpm = cls.get_rate(price, max_price)
        
            if cpm <= -(target_rate) and not investing:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = cls.get_rate(ret_m, invest_m)

            log.debug("%s, %s, %s, %s, %s, %s, %s, %s", price, max_price, cpm, invest_m, stock, ret_m, ret_rate, investing)

            if cpm >= 0 and investing:
                investing = False
                invest_m = 0
                stock = 0
                tmp_m = ret_m

            q.get()
            idx = idx+1

        if ret_m == 0:
            ret_m = tmp_m

        return cls.get_rate(ret_m, org_m)

    # 로직 gamma의 매수 여부
    @classmethod
    def _check_buy(cls, df):
        log.info('logic gamma check buy run')
        gamma_df = df['Close']
        q = queue.Queue()

        idx = 0
        target_rate = 0.15

        buy = False
        
        for price in gamma_df:
            q.put(price)
            if idx < 51:
                idx = idx+1
                log.debug(price)
                continue

            max_price = max(list(q.queue))
            cpm = cls.get_rate(price, max_price)
        
            if cpm <= -(target_rate):
                buy = True
            else:
                buy = False

            log.debug("%s, %s, %s, %s", price, max_price, cpm, buy)
            
            q.get()
            idx = idx+1

        if buy:
            return 'buy'
        else:
            return '-'



    # 로직 gamma의 매도 여부
    @classmethod
    def _check_sell(cls, df, org_m, stock):
        log.info('logic gamma check sell run')
        gamma_df = df['Close']
        q = queue.Queue()
        idx = 0
        
        sell = False
        
        #l_price = gamma_df[-1]
        l_price = gamma_df.iloc[-1]

        for price in gamma_df:
            q.put(price)
            if idx < 51:
                idx = idx+1
                continue
                
            max_price = max(list(q.queue))

            q.get()
            idx = idx+1

        cpm = cls.get_rate(l_price, max_price)

        if cpm >= 0:
            sell = True
        else:
            sell = False

        log.debug('%s, %s, %s', org_m, cpm, sell)


        if sell:
            return 'sell'
        else:
            return '-'


class Logic_delta(Logic):

    def __init__(self):
        log.info("Start Logic")

    # 로직 delta의 수익률
    # delta:
    #  - 매수: 10일 평균 -% 이하일 경우 매수
    #  - 매도: target_rate + 이면 매도
    @classmethod
    def run_logic(cls, df):
        log.info('logic delta run')
        delta_df = df['Close']

        idx = 0
        investing = False

        org_m = 1000000
        invest_m = 0
        target_rate = 0.15

        ret_money = 0
        stock = 0
        tmp_m = 0
        
        for price in delta_df:
            if idx < 51:
                log.debug(price)
                idx = idx+1
                continue

            #avr_price = (price+delta_df[idx-1])/2
            avr_price = (price+delta_df.iloc[idx-1])/2
            cpm = cls.get_rate(price, avr_price)

            if cpm < 0 and not investing:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = cls.get_rate(ret_m, invest_m)

            log.debug("%s, %s, %s, %s, %s, %s, %s, %s", price, avr_price, cpm, invest_m, stock, ret_m, ret_rate, investing)
            if ret_rate > target_rate:
                investing = False
                stock = 0
                tmp_m = ret_m
            idx = idx+1

        if ret_m == 0:
            ret_m = tmp_m

        return cls.get_rate(ret_m, org_m)

    # 로직 delta의 매수 여부
    @classmethod
    def _check_buy(cls, df):
        log.info('logic delta check buy run')
        delta_df = df['Close']

        idx = 0
        buy = False
 
        for price in delta_df:
            if idx < 51:
                idx = idx+1
                log.debug(price)
                continue

            #avr_price = (price+delta_df[idx-1])/2
            avr_price = (price+delta_df.iloc[idx-1])/2
            cpm = cls.get_rate(price, avr_price)


            if cpm < 0:
                buy = True
            else:
                buy = False

            log.debug("%s, %s, %s, %s", price, avr_price, cpm, buy)

            idx = idx+1

        if buy:
            return 'buy'
        else:
            return '-'



    # 로직 delta의 매도 여부
    @classmethod
    def _check_sell(cls, df, org_m, stock):
        log.info('logic delta check sell run')
        delta_df = df['Close']


        idx = 0
        sell = False

        target_rate = 0.15
        stock = stock
        org_m = org_m * stock
 
        #price = delta_df[-1]
        price = delta_df.iloc[-1]

        ret_m = price*stock

        ret_rate = cls.get_rate(ret_m, org_m)

        if ret_rate > target_rate:
            sell = True
        else:
            sell = False

        log.debug("%s, %s, %s, %s", price, org_m, ret_rate, sell)

        if sell:
            return 'sell'
        else:
            return '-'



class Logic_epsilon(Logic):

    def __init__(self):
        log.info("Start Logic")

    # 로직 epsilon의 수익률
    # epsilon:
    #  - 매수: 누적 등락률이 -% 일 경우 매수
    #  - 매도: target_rate + 이면 매도
    #  - 누적 등락률이 0.3 이상이면 0으로 초기화
    @classmethod
    def run_logic(cls, df):
        log.info('logic epsilon run')
        epsilon_df = df['Close']

        idx = 0
        investing = False

        org_m = 1000000
        invest_m = 0
        target_rate = 0.15
        sum_cpm=0

        ret_money = 0
        stock = 0
        tmp_m = 0
        
        for price in epsilon_df:
            if idx < 51:
                log.debug(price)
                idx = idx+1
                continue

            #cpm = cls.get_rate(price,epsilon_df[idx-1])
            cpm = cls.get_rate(price,epsilon_df.iloc[idx-1])
            sum_cpm = sum_cpm+cpm
            
            if sum_cpm < 0 and not investing:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = cls.get_rate(ret_m, invest_m)

            log.debug("%s, %s, %s, %s, %s, %s, %s, %s",price, cpm, sum_cpm, invest_m, stock, ret_m, ret_rate, investing)
            
            if ret_rate > target_rate:
                investing = False
                stock = 0
                tmp_m = ret_m
                sum_cpm = 0

            if sum_cpm > 0.3:
                sum_cpm = 0
            
            idx = idx+1

        if ret_m == 0:
            ret_m = tmp_m

        return cls.get_rate(ret_m, org_m)


    # 로직 epsilon의 매수 여부
    @classmethod
    def _check_buy(cls, df):
        log.info('logic epsilon check buy run')
        epsilon_df = df['Close']

        idx = 0
        sum_cpm=0
        buy = False
        
        for price in epsilon_df:
            if idx < 51:
                idx = idx+1
                log.debug(price)
                continue

            #cpm = cls.get_rate(price,epsilon_df[idx-1])
            cpm = cls.get_rate(price,epsilon_df.iloc[idx-1])
            sum_cpm = sum_cpm+cpm
            
            if sum_cpm < 0:
                buy = True
            else:
                buy = False

            if sum_cpm > 0.3:
                sum_cpm = 0

            log.debug("%s, %s, %s, %s",price, cpm, sum_cpm, buy)
            
            idx = idx+1

        if buy:
            return 'buy'
        else:
            return '-'



    # 로직 epsilon의 매도 여부
    @classmethod
    def _check_sell(cls, df, org_m, stock):
        log.info('logic epsilon check sell run')
        epsilon_df = df['Close']
        
        idx = 0
        sell = False

        org_m = org_m * stock
        stock = stock
        target_rate = 0.15
        
        #price = epsilon_df[-1]
        price = epsilon_df.iloc[-1]

        ret_m = price*stock
        ret_rate = cls.get_rate(ret_m, org_m)

        if ret_rate > target_rate:
            sell = True
        else:
            sell = False

        log.info("%s, %s, %s, %s", org_m, price, ret_rate, sell)

        if sell:
            return 'sell'
        else:
            return '-'


def back_test_gamma(file_name):
    df = DataManager.load_data_from_csv('final_data_1013.csv')

    for name, code in zip(df['종목명'],df['Code']):
        tmp_df = DataManager.load_stock_data(code)

        print(Logic_gamma.run_logic(tmp_df))

 


if __name__ == '__main__':
    #obj = Logic()
    #obj2 = DataManagement()
    #df = DataManager.load_stock_data('010130')
    #Logic_gamma.run_logic(df)

    back_test_gamma('back_test.csv')

    




