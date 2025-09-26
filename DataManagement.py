import os
import pandas as pd
import yfinance as yf

class DataManagement:
    
    def __init__(self):
        print('Start DataManagement')
    
    # .xlsx 파일을 읽어서 dataframe 반환
    def load_data_from_excel(self, file_name):
        #print(file_name)
        file_name = os.path.join("./datas", file_name)
        self.df = pd.read_excel(file_name)
        #print(self.df)

        return self.df

    # 주식코드를 받아서 dataframe 반환
    def load_data_from_yf(self, code):
        data = yf.Ticker(code)
        self.df = data.history(interval="1wk", start="2023-01-01")
        #print(self.df)

        return self.df


    # 주식명을 받아서 주식 코드 반환
    def name_to_code(self, name):
        file_name = "./datas/krx.csv"
        krx_df = pd.read_csv(file_name)

        ret_code = 'none'
        for market, code, cname in zip(krx_df['시장구분'],krx_df['단축코드'],krx_df['한글 종목약명']):
            if name == cname:
                ret_code = code
                if market == 'KOSPI':
                    ret_code = ret_code + '.KS'
                else:
                    ret_code = ret_code + '.KQ'
                break

        #print(ret_code)
        return ret_code

    # .csv 파일을 읽어서 dataframe 반환
    def load_data_from_csv(self, file_name):
        file_name = os.path.join("./datas", file_name)
        self.df = pd.read_csv(file_name)
        #print(self.df)

        return self.df


    def adj_df(self):
        self.a_df = self.df[['종목명','ROE']]

        code_list = []

        for name in self.a_df['종목명']:
            code = self.name_to_code(name)
            #print(name,code)
            code_list.append(code)

        self.a_df['Code'] = code_list
        self.a_df = self.a_df.drop('ROE', axis=1)


    def load_data_market_cap(self, file_name):
        self.load_data_from_csv(file_name)
        self.adj_df()

        #print(self.a_df)

        return self.a_df





if __name__ == '__main__':
    obj = DataManagement()
    #obj.load_data_from_excel("samsung_week.xlsx")
    #obj.load_data_from_yf("005930.KS")

    #code = obj.name_to_code('알테오젠')
    #print(obj.load_data_from_csv('market_cap_kospi.csv'))
    obj.load_data_market_cap('market_cap_kospi2.csv')
    #obj.calc()


