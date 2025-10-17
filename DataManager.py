import os
import pandas as pd
import yfinance as yf
import logging
from LogManager import LogManager
import requests
import FinanceDataReader as fdr
import datetime


log = LogManager.get_logger(logging.ERROR)


class DataManager:
    
    def __init__(self):
        log.info('Start DataManagement')
 
    # .csv 파일을 읽어서 dataframe 반환
    @classmethod
    def load_data_from_csv(cls, file_name, base_path='./datas'):
        file_name = os.path.join(base_path, file_name)
        try:
            df = pd.read_csv(file_name, index_col=0)
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_name}")

    # dataframe을.csv 파일로 저장
    @classmethod
    def save_data_to_csv(cls, file_name, df, base_path='./datas'):
        file_name = os.path.join(base_path, file_name)
        df.to_csv(file_name, sep=',', encoding="utf-8-sig")

    # 주식명을 받아서 주식 코드 반환
    @classmethod
    def name_to_code(cls, name, base_path='./datas'):
        file_name = os.path.join(base_path, 'krx.csv')
        #file_name = "./datas/krx.csv"
        krx_df = pd.read_csv(file_name)

        ret_code = 'none'
        for market, code, cname in zip(krx_df['시장구분'],krx_df['단축코드'],krx_df['한글 종목약명']):
            if name == cname:
                ret_code = code
                """
                if market == 'KOSPI':
                    ret_code = ret_code + '.KS'
                else:
                    ret_code = ret_code + '.KQ'
                """
                break

        #print(ret_code)
        return ret_code

    # dataframe에 주식 코드 추가
    @classmethod
    def add_code(cls, df, base_path='./datas'):
        a_df = df

        code_list = []

        for name in a_df['종목명']:
            code = cls.name_to_code(name, base_path)
            code_list.append(code)

        a_df['Code'] = code_list

        return a_df


    @classmethod
    def _load_data_from_fd(cls, code, start, end):
        #today = datetime.date.today()
        df = fdr.DataReader(code, start, end)
        #df["weekday"] = df.index.weekday
        #df = df[df["weekday"] == 4]

        df.index = pd.to_datetime(df.index)
        w_df = df.resample('W-FRI').last()

        #log.debug(w_df)
        return w_df


    @classmethod
    def load_stock_data(cls, code, start="2018-01-01", end=datetime.date.today()):
        """
        ret = cls._check_yf_connection()
        if ret:
            df = cls._load_data_from_yf(code, start)
        else:
            code = code.split(".")[0]
            df = cls._load_data_from_fd(code, start)
        """
        code = code.split(".")[0]
        df = cls._load_data_from_fd(code, start, end)

        return df

    """
    # 주식코드를 받아서 dataframe 반환
    @classmethod
    def _load_data_from_yf(cls, code, start="2018-01-01"):
        data = yf.Ticker(code)
        df = data.history(start=start)
        df["weekday"] = df.index.weekday

        df = df[df["weekday"] == 4]

        return df

    @classmethod
    def _check_yf_connection(cls):
        url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=AAPL"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                print("✅ yfinance 서버 연결 성공")
                return True
            else:
                print(f"⚠️ 연결 실패: HTTP {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ 연결 오류: {e}")
            return False
    """


if __name__ == '__main__':

    """
    # 데이터 가공
    obj = DataManager()
    df = obj.load_data_from_csv('name_list.csv')
    df = obj.add_code(df)
    obj.save_data_to_csv('code_list.csv', df)
    log.debug(df)
    """

    df = DataManager.load_stock_data('105560', end='2024-12-31')
    log.debug(df)

