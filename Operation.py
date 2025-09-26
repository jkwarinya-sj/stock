import pandas as pd
from DataManagement import DataManagement 
from Logic_v2 import Logic 

class Data:
    def __init__(self, name, code, logic, check_buy, check_sell, price, stock):
        self.name = name
        self.code = code
        self.check_buy = check_buy
        self.check_sell = check_sell
        self.price = price
        self.stock = stock
        self.logic = logic

    def run(self, df):
        if self.logic == 'dca':
            print('dca skip')
            return

        status = ''

        if self.stock == 0:
            status = self.check_buy(df)
        else:
            status = self.check_sell(df, self.price, self.stock)

        print(self.name, status)


class Operating:
    
    def __init__(self):
        print("Start Operating")
        self.obj_dm = DataManagement()
        self.df = self.obj_dm.load_data_from_csv('final_data.csv')
        logic_m = Logic()
        self.method_dict_buy={}
        self.method_dict_buy['alpha'] = logic_m.logic_alpha_check_buy
        self.method_dict_buy['gamma'] = logic_m.logic_gamma_check_buy
        self.method_dict_buy['delta'] = logic_m.logic_delta_check_buy
        self.method_dict_buy['epsilon'] = logic_m.logic_epsilon_check_buy
        self.method_dict_buy['dca'] = ''
        
        self.method_dict_sell={}
        self.method_dict_sell['alpha'] = logic_m.logic_alpha_check_sell
        self.method_dict_sell['gamma'] = logic_m.logic_gamma_check_sell
        self.method_dict_sell['delta'] = logic_m.logic_delta_check_sell
        self.method_dict_sell['epsilon'] = logic_m.logic_epsilon_check_sell
        self.method_dict_sell['dca'] = ''

        self.set_data()
 
    def set_data(self):
        self.data_list = []
        for name, code, logic, price, stock in zip(self.df['종목명'],self.df['Code'],self.df['logic'],self.df['price'],self.df['stock']):
            d = Data(name,
                    code,
                    logic,
                    self.method_dict_buy[logic],
                    self.method_dict_sell[logic],
                    price,
                    stock
                    )
            self.data_list.append(d)


    def run(self):
        for data in self.data_list:
            tmp_df = self.obj_dm.load_data_from_yf(data.code)
            data.run(tmp_df)
            
            





if __name__ == '__main__':
    obj = Operating()
    obj.run()


