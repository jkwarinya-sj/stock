import pandas as pd
from DataManager import DataManager 
import logging
import queue
from LogManager import LogManager
import numpy as np


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

    @staticmethod
    def _make_cpm_delta(df):
        return df['Delta']/(df['Close'] - df['Delta'])

    @staticmethod
    def _make_avr_delta(df):
        d_rate = df['Delta_rate']

        gain = d_rate.clip(lower=0)
        loss = d_rate.clip(upper=0)
    
        df['Gain_mean'] = gain[gain != 0].expanding().mean()
        df['Loss_mean'] = loss[loss != 0].expanding().mean()

        df =df.fillna(0)

        return df





    @staticmethod
    def _make_cpm(df):
        return Logic.get_rate(df['Close'], df['Max'])

    @staticmethod
    def _make_cpm_avr(df):
        return Logic.get_rate(df['Close'], df['Avr'])

    @staticmethod
    def _make_z_score(df):
        if df['Std'] == 0:
            return 0

        return (df['Close']-df['Avr'])/df['Std']

    @staticmethod
    def _make_rsi(df):

        delta = df['Close'].diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        period=10
        avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
        avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    @classmethod
    def _check_sell_by_target_rate(cls, df, org_m, stock):
        target_df = df['Close']

        stock = stock
        org_m = org_m * stock
        sell = False
        target_rate = 0.15

        price = target_df.iloc[-1]

        ret_m = price*stock
        ret_rate = cls.get_rate(ret_m, org_m)

        if ret_rate > target_rate:
            sell = True
        else:
            sell = False

        log.info("%s, %s, %s, %s", org_m, ret_m, ret_rate, sell)

        return sell

    
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

        if df.empty:
            return 0

        df['Max'] = df['Close'].rolling(window=52).max()
        df["Cpm"] = df.apply(cls._make_cpm, axis=1)
        alpha_df = df[['Close', 'Max', 'Cpm']]
        idx = 0

        org_m = 1000000
        ret_m = 0
        tmp_m = 0
        stock = 0
        invest_m = 0

        start_rate = 0.05
        target_rate = 0.15
        #target_rate = 0.25
        investing = False

        for price, max_price, cpm in zip(alpha_df['Close'], alpha_df['Max'], alpha_df['Cpm']):
            if idx < 51:
                log.debug(price)
                idx = idx+1
                continue

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
            
            idx = idx+1


        if ret_m == 0:
            ret_m = tmp_m

        return cls.get_rate(ret_m, org_m)

    # 로직 alpha에 매수 여부
    @classmethod
    def _check_buy(cls, df):
        log.info('logic alpha check buy run')
        df['Max'] = df['Close'].rolling(window=52).max()
        df["Cpm"] = df.apply(cls._make_cpm, axis=1)
        alpha_df = df[['Close', 'Max', 'Cpm']]

        idx = 0

        start_rate = 0.05
        buy = False

        cpm = alpha_df['Cpm'].iloc[-1]

        if cpm < -(start_rate):
            buy = True
        else:
            buy = False

        if buy:
            return 'buy'
        else:
            return '-'

    # 로직alpha에 매도 여부
    @classmethod
    def _check_sell(cls, df, org_m, stock):
        log.info('logic alpha check sell run')
        
        sell = cls._check_sell_by_target_rate(df, org_m, stock)
        
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

        if df.empty:
            return 0

        df['Max'] = df['Close'].rolling(window=52).max()
        df["Cpm"] = df.apply(cls._make_cpm, axis=1)
        gamma_df = df[['Close', 'Max', 'Cpm']]

        idx = 0
        ret_m = 0
        stock = 0
        org_m = 1000000
        invest_m = 0
        tmp_m = 0
        target_rate = 0.15

        investing = False

        for price, max_price, cpm in zip(gamma_df['Close'], gamma_df['Max'], gamma_df['Cpm']):

            if idx < 51:
                log.debug(price)
                idx = idx+1
                continue
        
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

            idx = idx+1

        if ret_m == 0:
            ret_m = tmp_m

        return cls.get_rate(ret_m, org_m)

    # 로직 gamma의 매수 여부
    @classmethod
    def _check_buy(cls, df):
        log.info('logic gamma check buy run')
        df['Max'] = df['Close'].rolling(window=52).max()
        df["Cpm"] = df.apply(cls._make_cpm, axis=1)
        gamma_df = df[['Close', 'Max', 'Cpm']]

        idx = 0
        target_rate = 0.15

        buy = False
        
        cpm = gamma_df['Cpm'].iloc[-1]

        if cpm <= -(target_rate):
            buy = True
        else:
            buy = False

        if buy:
            return 'buy'
        else:
            return '-'



    # 로직 gamma의 매도 여부
    @classmethod
    def _check_sell(cls, df, org_m, stock):
        log.info('logic gamma check sell run')
        df['Max'] = df['Close'].rolling(window=52).max()
        df["Cpm"] = df.apply(cls._make_cpm, axis=1)
        gamma_df = df[['Close', 'Max', 'Cpm']]

        idx = 0
        
        sell = False
        
        cpm = gamma_df['Cpm'].iloc[-1]

        if cpm >= 0:
            sell = True
        else:
            sell = False


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

        if df.empty:
            return 0

        df['Avr'] = df['Close'].rolling(window=2).mean()
        df["Cpm"] = df.apply(cls._make_cpm_avr, axis=1)
        delta_df = df[['Close', 'Avr', 'Cpm']]

        idx = 0
        investing = False

        org_m = 1000000
        invest_m = 0
        target_rate = 0.15
        #target_rate = 0.25

        ret_money = 0
        stock = 0
        tmp_m = 0
        ret_m = 0
        
        for price, avr, cpm in zip(delta_df['Close'], delta_df['Avr'], delta_df['Cpm']):
        #for price in delta_df:
            if idx < 51:
                log.debug(price)
                idx = idx+1
                continue

            avr_price = avr
            if cpm < 0 and not investing:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = cls.get_rate(ret_m, invest_m)

            #log.debug("%s, %s, %s, %s, %s, %s, %s, %s", price, avr_price, cpm, invest_m, stock, ret_m, ret_rate, investing)
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
        df['Avr'] = df['Close'].rolling(window=2).mean()
        df["Cpm"] = df.apply(cls._make_cpm_avr, axis=1)
        delta_df = df[['Close', 'Avr', 'Cpm']]

        idx = 0
        buy = False

        cpm = delta_df['Cpm'].iloc[-1]
 
        if cpm < 0:
            buy = True
        else:
            buy = False

        if buy:
            return 'buy'
        else:
            return '-'


    # 로직 delta의 매도 여부
    @classmethod
    def _check_sell(cls, df, org_m, stock):
        log.info('logic delta check sell run')
                
        sell = cls._check_sell_by_target_rate(df, org_m, stock)

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
        #target_rate = 0.2
        sum_cpm=0

        ret_money = 0
        stock = 0
        tmp_m = 0
        ret_m = 0
        
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
        
        sell = cls._check_sell_by_target_rate(df, org_m, stock)

        if sell:
            return 'sell'
        else:
            return '-'

class Logic_zeta(Logic):

    def __init__(self):
        log.info("Start Logic")

    # 로직 zeta의 수익률
    # zeta:
    #  - 매수 : 52주 평균 대비 평균 하락률 보다 작을 경우 매수
    #  - 매도: target_rate + 이면 매도
    @classmethod
    def run_logic(cls, df):
        log.info('logic zeta run')

        if df.empty:
            return 0

        idx = 0

        df['Avr'] = df['Close'].rolling(window=52).mean()
        df["Cpm"] = df.apply(cls._make_cpm_avr, axis=1)
        zeta_df = df[['Close', 'Avr', 'Cpm']]

        org_m = 1000000
        ret_m = 0
        tmp_m = 0
        stock = 0
        invest_m = 0

        target_rate = 0.15
        #target_rate = 0.75
        investing = False
        cpm_list = []

        for price, avr, cpm in zip(zeta_df['Close'], zeta_df['Avr'], zeta_df['Cpm']):
            if idx < 51:
                log.debug("%s", price)
                idx = idx+1
                continue

            if cpm < 0.0:
                cpm_list.append(cpm)

            if len(cpm_list) == 0:
                cpm_mean = 0
            else:
                cpm_mean = np.mean(np.array(cpm_list))

            if cpm_mean >= cpm and not investing:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = cls.get_rate(ret_m, invest_m)

            log.debug("%s, %s, %s, %s, %s, %s, %s, %s, %s", price, avr, cpm, cpm_mean ,invest_m, stock, ret_m, ret_rate, investing)

            if ret_rate > target_rate:
                investing = False
                invest_m = 0
                stock = 0
                tmp_m = ret_m
            
            idx = idx+1

        if ret_m == 0:
            ret_m = tmp_m

        return cls.get_rate(ret_m, org_m)


    # 로직 zeta의 매수 여부
    @classmethod
    def _check_buy(cls, df):
        log.info('logic zeta check buy run')
        #zeta_df = df['Close']
        idx = 0
        #q = queue.Queue()

        df['Avr'] = df['Close'].rolling(window=52).mean()
        df["Cpm"] = df.apply(cls._make_cpm_avr, axis=1)
        zeta_df = df[['Close', 'Avr', 'Cpm']]

        org_m = 1000000
        ret_m = 0
        tmp_m = 0
        stock = 0
        invest_m = 0

        target_rate = 0.15
        buy = False
        cpm_list = []

        for price, avr, cpm in zip(zeta_df['Close'], zeta_df['Avr'], zeta_df['Cpm']):
            if idx < 51:
                log.debug("%s", price)
                idx = idx+1
                continue

            #avr_price = np.mean(np.array(list(q.queue)))
            #cpm = cls.get_rate(price, avr_price)

            if cpm < 0.0:
                cpm_list.append(cpm)

            if len(cpm_list) == 0:
                cpm_mean = 0
            else:
                cpm_mean = np.mean(np.array(cpm_list))

            if cpm_mean >= cpm:
                buy = True
            else:
                buy = False

            log.debug("%s, %s, %s, %s, %s, %s", price, avr, cpm, cpm_mean ,ret_m,buy)
            idx = idx+1

        if buy:
            return 'buy'
        else:
            return '-'

    # 로직 zeta의 매도 여부
    @classmethod
    def _check_sell(cls, df, org_m, stock):
        log.info('logic zeta check sell run')
        
        sell = cls._check_sell_by_target_rate(df, org_m, stock)

        if sell:
            return 'sell'
        else:
            return '-'


class Logic_eta(Logic):

    def __init__(self):
        log.info("Start Logic")

    # 로직 eta의 수익률
    # eta:
    #  - 매수 : 50일 평균에 대한 평균회기 z-socre가 -2 보다 작을 경우 매수
    #  - 매도: target_rate + 이면 매도
    @classmethod
    def run_logic(cls, df):
        log.info('logic eta run')

        if df.empty:
            return 0

        idx = 0

        df['Avr'] = df['Close'].rolling(window=10).mean()
        df['Std'] = df['Close'].rolling(window=10).std(ddof=0)
        df["Z_Score"] = df.apply(cls._make_z_score, axis=1)
        eta_df = df[['Close', 'Avr', 'Z_Score', 'Std']]

        org_m = 1000000
        ret_m = 0
        tmp_m = 0
        stock = 0
        invest_m = 0

        target_rate = 0.15
        #target_rate = 0.55
        investing = False

        for price, avr, std_price, z_score in zip(eta_df['Close'], eta_df['Avr'], eta_df['Std'], eta_df['Z_Score']):
            if idx < 51:
                log.debug("%s", price)
                idx = idx+1
                continue
            
            cpm = cls.get_rate(price, avr)

            if z_score < -2.0 and not investing:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = cls.get_rate(ret_m, invest_m)

            log.debug("%s, %s, %s, %s, %s, %s, %s, %s, %s", price, avr, std_price, z_score ,invest_m, stock, ret_m, ret_rate, investing)

            if ret_rate > target_rate:
                investing = False
                invest_m = 0
                stock = 0
                tmp_m = ret_m
            
            idx = idx+1


        if ret_m == 0:
            ret_m = tmp_m

        return cls.get_rate(ret_m, org_m)


    # 로직 eta의 매수 여부
    @classmethod
    def _check_buy(cls, df):
        log.info('logic eta check buy run')
        #idx = 0

        df['Avr'] = df['Close'].rolling(window=10).mean()
        df['Std'] = df['Close'].rolling(window=10).std(ddof=0)
        df["Z_Score"] = df.apply(cls._make_z_score, axis=1)
        eta_df = df[['Close', 'Avr', 'Z_Score', 'Std']]
    
        if eta_df['Z_Score'].iloc[-1] < -2.0:
            buy = True
        else:
            buy = False

        if buy:
            return 'buy'
        else:
            return '-'


    # 로직 eta의 매도 여부
    @classmethod
    def _check_sell(cls, df, org_m, stock):
        log.info('logic eta check sell run')
        
        sell = cls._check_sell_by_target_rate(df, org_m, stock)

        if sell:
            return 'sell'
        else:
            return '-'

class Logic_theta(Logic):

    def __init__(self):
        log.info("Start Logic")

    # 로직 theta의 수익률
    # eta:
    #  - 매수 : 50일 평균에 대한 평균회기 z-socre가 -2 보다 작을 경우 매수
    #  - 매도 : 50일 평균에 대한 평균회기 z-socre가 2 보다 큰 경우 매수
    @classmethod
    def run_logic(cls, df):
        log.info('logic theta run')

        if df.empty:
            return 0

        idx = 0

        df['Avr'] = df['Close'].rolling(window=10).mean()
        df['Std'] = df['Close'].rolling(window=10).std(ddof=0)
        df["Z_Score"] = df.apply(cls._make_z_score, axis=1)
        theta_df = df[['Close', 'Avr', 'Z_Score', 'Std']]

        org_m = 1000000
        ret_m = 0
        tmp_m = 0
        stock = 0
        invest_m = 0

        investing = False


        for price, avr, std_price, z_score in zip(theta_df['Close'], theta_df['Avr'], theta_df['Std'], theta_df['Z_Score']):
            if idx < 51:
                log.debug("%s", price)
                idx = idx+1
                continue
            
            if z_score < -2.0 and not investing:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = cls.get_rate(ret_m, invest_m)

            log.debug("%s, %s, %s, %s, %s, %s, %s, %s, %s", price, avr, std_price, z_score ,invest_m, stock, ret_m, ret_rate, investing)

            if z_score > 2.0 and investing:
                investing = False
                invest_m = 0
                stock = 0
                tmp_m = ret_m
            
            idx = idx+1

        if ret_m == 0:
            ret_m = tmp_m

        return cls.get_rate(ret_m, org_m)

    # 로직 theta의 매수 여부
    @classmethod
    def _check_buy(cls, df):
        log.info('logic theta check buy run')

        buy = False

        df['Avr'] = df['Close'].rolling(window=10).mean()
        df['Std'] = df['Close'].rolling(window=10).std(ddof=0)
        df["Z_Score"] = df.apply(cls._make_z_score, axis=1)
        theta_df = df[['Close', 'Avr', 'Z_Score', 'Std']]

        if theta_df['Z_Score'].iloc[-1] < -2.0:
            buy = True
        else:
            buy = False

        if buy:
            return 'buy'
        else:
            return '-'

    # 로직 theta의 매도 여부
    @classmethod
    def _check_sell(cls, df, org_m, stock):
        
        log.info('logic theta check sell run')

        sell = False

        df['Avr'] = df['Close'].rolling(window=10).mean()
        df['Std'] = df['Close'].rolling(window=10).std(ddof=0)
        df["Z_Score"] = df.apply(cls._make_z_score, axis=1)
        theta_df = df[['Close', 'Avr', 'Z_Score', 'Std']]

        z_score = theta_df['Z_Score'].iloc[-1]
        log.debug(z_score)
        if theta_df['Z_Score'].iloc[-1] > 2.0:
            sell = True
        else:
            sell = False

        if sell:
            return 'sell'
        else:
            return '-'




class Logic_iota(Logic):

    def __init__(self):
        log.info("Start Logic")

    # 로직 iota의 수익률
    # eta:
    #  - 매수 : 50일 평균에 대한RSI가 40  보다 작을 경우 매수
    #  - 매도: target_rate + 이면 매도
    @classmethod
    def run_logic(cls, df):
        log.info('logic iota run')

        if df.empty:
            return 0


        idx = 0

        org_m = 1000000
        ret_m = 0
        tmp_m = 0
        stock = 0
        invest_m = 0

        target_rate = 0.15
        #target_rate = 0.2
        investing = False
        
        df['RSI'] = cls._make_rsi(df)

        log.debug(df)

        iota_df = df[['Close','RSI']]


        for price, rsi in zip(iota_df['Close'], iota_df['RSI']):
            #log.debug("%s", price)
            #if idx > 41:
            #    log.debug("%s, %s", price, rsi)

            if idx < 51:
                log.debug("%s", price)
                idx = idx+1
                continue

            if rsi < 40  and not investing:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = cls.get_rate(ret_m, invest_m)

            log.debug("%s, %s, %s, %s, %s, %s, %s", price, rsi, invest_m, stock, ret_m, ret_rate, investing)

            if ret_rate > target_rate:
                investing = False
                invest_m = 0
                stock = 0
                tmp_m = ret_m
            
            idx = idx+1


        if ret_m == 0:
            ret_m = tmp_m

        return cls.get_rate(ret_m, org_m)


    # 로직 iota의 매수 여부
    @classmethod
    def _check_buy(cls, df):
        log.info('logic iota check buy run')
        buy = False

        df['RSI'] = cls._make_rsi(df)

        log.debug(df)
        iota_df = df[['Close','RSI']]
        rsi = iota_df['RSI'].iloc[-1]

        if rsi < 40:
            buy = True
        else:
            buy = False

        if buy:
            return 'buy'
        else:
            return '-'

    # 로직 iota의 매도 여부
    @classmethod
    def _check_sell(cls, df, org_m, stock):
        log.info('logic iota check sell run')

        sell = cls._check_sell_by_target_rate(df, org_m, stock)

        if sell:
            return 'sell'
        else:
            return '-'


class Logic_kapa(Logic):

    def __init__(self):
        log.info("Start Logic")

    # 로직 kapa의 수익률
    # kapa:
    #  - 매수 : 50일 평균에 대한RSI가 40  보다 작을 경우 매수
    #  - 매도 : 50일 평균에 대한RSI가 70  보다 큰 경우 매수
    @classmethod
    def run_logic(cls, df):
        log.info('logic kapa run')

        if df.empty:
            return 0

        idx = 0

        org_m = 1000000
        ret_m = 0
        tmp_m = 0
        stock = 0
        invest_m = 0

        target_rate = 0.15
        investing = False
        
        df['RSI'] = cls._make_rsi(df)

        log.debug(df)

        kapa_df = df[['Close','RSI']]

        for price, rsi in zip(kapa_df['Close'], kapa_df['RSI']):
            #log.debug("%s", price)
            #if idx > 41:
            #    log.debug("%s, %s", price, rsi)

            if idx < 51:
                log.debug("%s", price)
                idx = idx+1
                continue

            if rsi < 40  and not investing:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = cls.get_rate(ret_m, invest_m)

            log.debug("%s, %s, %s, %s, %s, %s, %s", price, rsi, invest_m, stock, ret_m, ret_rate, investing)

            if rsi > 70 and investing:
                investing = False
                invest_m = 0
                stock = 0
                tmp_m = ret_m
            
            idx = idx+1

        if ret_m == 0:
            ret_m = tmp_m

        return cls.get_rate(ret_m, org_m)

    # 로직 kapa의 매수 여부
    @classmethod
    def _check_buy(cls, df):
        log.info('logic kapa check buy run')
        buy = False

        df['RSI'] = cls._make_rsi(df)

        log.debug(df)
        kapa_df = df[['Close','RSI']]
        rsi = kapa_df['RSI'].iloc[-1]

        if rsi < 40:
            buy = True
        else:
            buy = False

        if buy:
            return 'buy'
        else:
            return '-'

    # 로직 iota의 매도 여부
    @classmethod
    def _check_sell(cls, df, org_m, stock):
        log.info('logic kapa check sell run')
        sell = False

        df['RSI'] = cls._make_rsi(df)

        log.debug(df)
        kapa_df = df[['Close','RSI']]
        rsi = kapa_df['RSI'].iloc[-1]

        if rsi > 70:
            sell = True
        else:
            sell = False

        if sell:
            return 'sell'
        else:
            return '-'

class Logic_lamda(Logic):

    def __init__(self):
        log.info("Start Logic")

    # 로직 lamda의 수익률
    # lamda:
    #  - 매수 : 전체 평균 변화량(-)보다 현재 변화량이 작은경우 매수
    #  - 매도 : 전체 평균 변화량(+)보다 현재 수익률이이 큰경우 매도
    @classmethod
    def run_logic(cls, df):
        log.info('logic lamda run')

        if df.empty:
            return 0

        idx = 0

        org_m = 1000000
        ret_m = 0
        tmp_m = 0
        stock = 0
        invest_m = 0

        target_rate = 0.15
        investing = False

        delta = df['Close'].diff()
        df['Delta'] = delta
        df["Delta_rate"] = df.apply(cls._make_cpm_delta, axis=1)
        df = cls._make_avr_delta(df)

        for price, rate, g_mean, l_mean in zip(df['Close'], df['Delta_rate'], df['Gain_mean'], df['Loss_mean']):
            if idx < 51:
                log.debug("%s", price)
                idx = idx+1
                continue

            if rate < l_mean and not investing:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = cls.get_rate(ret_m, invest_m)

            log.debug("%s, %s, %s, %s, %s, %s, %s, %s", price, rate, g_mean, l_mean, invest_m, stock, ret_m, ret_rate)

            if ret_rate > g_mean and g_mean != 0 and investing:
                investing = False
                invest_m = 0
                stock = 0
                tmp_m = ret_m

            idx = idx+1

        if ret_m == 0:
            ret_m = tmp_m

        return cls.get_rate(ret_m, org_m)

    # 로직 lamda의 매수 여부
    @classmethod
    def _check_buy(cls, df):
        log.info('logic lamda check buy run')
        buy = False

        delta = df['Close'].diff()
        df['Delta'] = delta
        df["Delta_rate"] = df.apply(cls._make_cpm_delta, axis=1)
        df = cls._make_avr_delta(df)

        rate = df['Delta_rate'].iloc[-1]
        l_mean = df['Loss_mean'].iloc[-1]

        log.debug("%s, %s", rate, l_mean)

        if rate < l_mean:
            buy = True
        else:
            buy = False

        if buy:
            return 'buy'
        else:
            return '-'

    # 로직 lamda의 매도 여부
    @classmethod
    def _check_sell(cls, df, org_m, stock):
        log.info('logic lamda check sell run')
        sell = False
        
        delta = df['Close'].diff()
        df['Delta'] = delta
        df["Delta_rate"] = df.apply(cls._make_cpm_delta, axis=1)
        df = cls._make_avr_delta(df)

        ret_m = df['Close'][-1]*stock
        ret_rate = cls.get_rate(ret_m, org_m)
        g_mean = df['Gain_mean'][-1]

        log.debug("%s, %s", ret_rate, g_mean)

        if ret_rate > g_mean and g_mean != 0:
            sell = True
        else:
            sell = False

        if sell:
            return 'sell'
        else:
            return '-'


class Logic_mu(Logic):

    def __init__(self):
        log.info("Start Logic")

    # 로직 mu의 수익률
    # lamda:
    #  - 매수 : 전체 평균 변화량(-)보다 현재 변화량이 작은경우 매수
    #  - 매도: target_rate + 이면 매도
    @classmethod
    def run_logic(cls, df):
        log.info('logic mu run')

        if df.empty:
            return 0

        idx = 0

        org_m = 1000000
        ret_m = 0
        tmp_m = 0
        stock = 0
        invest_m = 0

        target_rate = 0.15
        investing = False

        delta = df['Close'].diff()
        df['Delta'] = delta
        df["Delta_rate"] = df.apply(cls._make_cpm_delta, axis=1)
        df = cls._make_avr_delta(df)

        for price, rate, g_mean, l_mean in zip(df['Close'], df['Delta_rate'], df['Gain_mean'], df['Loss_mean']):
            if idx < 51:
                log.debug("%s", price)
                idx = idx+1
                continue

            if rate < l_mean and not investing:
                investing = True
                if tmp_m == 0:
                    invest_m = org_m
                else:
                    invest_m = tmp_m
                stock = invest_m/price

            ret_m = price*stock
            ret_rate = cls.get_rate(ret_m, invest_m)

            log.debug("%s, %s, %s, %s, %s, %s, %s, %s", price, rate, g_mean, l_mean, invest_m, stock, ret_m, ret_rate)

            if ret_rate > target_rate and investing:
                investing = False
                invest_m = 0
                stock = 0
                tmp_m = ret_m

            idx = idx+1

        if ret_m == 0:
            ret_m = tmp_m

        return cls.get_rate(ret_m, org_m)

    # 로직 mu의 매수 여부
    @classmethod
    def _check_buy(cls, df):
        log.info('logic mu check buy run')
        buy = False

        delta = df['Close'].diff()
        df['Delta'] = delta
        df["Delta_rate"] = df.apply(cls._make_cpm_delta, axis=1)
        df = cls._make_avr_delta(df)

        rate = df['Delta_rate'].iloc[-1]
        l_mean = df['Loss_mean'].iloc[-1]

        log.debug("%s, %s", rate, l_mean)

        if rate < l_mean:
            buy = True
        else:
            buy = False

        if buy:
            return 'buy'
        else:
            return '-'

    # 로직 mu의 매도 여부
    @classmethod
    def _check_sell(cls, df, org_m, stock):
        log.info('logic mu check sell run')
        #sell = False
        
        sell = cls._check_sell_by_target_rate(df, org_m, stock)

        """
        delta = df['Close'].diff()
        df['Delta'] = delta
        df["Delta_rate"] = df.apply(cls._make_cpm_delta, axis=1)
        df = cls._make_avr_delta(df)

        ret_m = df['Close'][-1]*stock
        ret_rate = cls.get_rate(ret_m, org_m)
        g_mean = df['Gain_mean'][-1]

        log.debug("%s, %s", ret_rate, g_mean)

        if ret_rate > g_mean and g_mean != 0:
            sell = True
        else:
            sell = False
        """

        if sell:
            return 'sell'
        else:
            return '-'




def back_test_zeta(file_name, end_date):
    df = DataManager.load_data_from_csv('final_data_1013.csv')

    for name, code in zip(df['종목명'],df['Code']):
        #tmp_df = DataManager.load_stock_data(code)
        tmp_df = DataManager.load_stock_data(code, end=end_date)
        print(Logic_zeta.run_logic(tmp_df))

def back_test_dca(file_name, end_date):
    df = DataManager.load_data_from_csv(file_name)

    for name, code in zip(df['종목명'],df['Code']):
        tmp_df = DataManager.load_stock_data(code, end=end_date)
        print(Logic_dca.run_logic(tmp_df))

def back_test_alpha(file_name, end_date):
    df = DataManager.load_data_from_csv(file_name)

    for name, code in zip(df['종목명'],df['Code']):
        tmp_df = DataManager.load_stock_data(code, end=end_date)
        print(Logic_alpha.run_logic(tmp_df))

def back_test_gamma(file_name, end_date):
    df = DataManager.load_data_from_csv('final_data_1013.csv')

    for name, code in zip(df['종목명'],df['Code']):
        #tmp_df = DataManager.load_stock_data(code, end=end_date)
        print(Logic_gamma.run_logic(tmp_df))


def back_test(obj, file_name, start_date='2018-01-01', end_date='2024-12-31'):
    df = DataManager.load_data_from_csv(file_name)

    for name, code in zip(df['Name'],df['Code']):
        tmp_df = DataManager.load_stock_data(code, start=start_date, end=end_date)
        #print(name)
        ret = obj.run_logic(tmp_df)
        if ret == -1:
            print(0)
        else:
            print(ret)





if __name__ == '__main__':
    #obj = Logic()
    #obj2 = DataManagement()
    #df = DataManager.load_stock_data('267260')
    #df = DataManager.load_stock_data('005930')
    #df = DataManager.load_stock_data('017670')
    #df = DataManager.load_stock_data('323280')
    #df = DataManager.load_stock_data('443060', end='2024-12-31')
    #Logic_lamda.run_logic(df)
    #Logic_mu.run_logic(df)
    
    #df = DataManager.load_stock_data('443060', start='2020-08-01',end='2022-08-01')
    #Logic_alpha.run_logic(df)
    #Logic_kapa._check_sell(df, 0, 0)

    """
    for logic back_test
    end_date='2024-12-31'
    """
    end_date='2025-09-30'

    #end_date='2022-08-01'
    #start_date='2020-08-01'

    #back_test(Logic_dca, 'back_test_new.csv', end_date=end_date)
    #back_test(Logic_alpha, 'back_test_new.csv', end_date=end_date)
    #back_test(Logic_gamma, 'back_test_new.csv', end_date=end_date)
    #back_test(Logic_delta, 'back_test_new.csv', end_date=end_date)
    #back_test(Logic_epsilon, 'back_test_new.csv', end_date=end_date)
    #back_test(Logic_zeta, 'back_test_new.csv', end_date=end_date)
    #back_test(Logic_eta, 'back_test_new.csv', end_date=end_date)
    #back_test(Logic_theta, 'back_test_new.csv', end_date=end_date)
    #back_test(Logic_iota, 'back_test_new.csv', end_date=end_date)
    #back_test(Logic_kapa, 'back_test_new.csv', end_date=end_date)
    #back_test(Logic_lamda, 'back_test_new.csv', end_date=end_date)
    back_test(Logic_mu, 'back_test_new.csv', end_date=end_date)


