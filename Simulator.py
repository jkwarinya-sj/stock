import logging
from LogManager import LogManager
from DataManager import DataManager 
from StockManager import Stock
import Logic as l
import pandas as pd
import datetime
#from tqdm import tqdm
from tqdm import tqdm, tqdm_pandas

log = LogManager.get_logger(logging.DEBUG)
method_dict={}
method_dict['alpha'] = l.Logic_alpha.check_status
method_dict['gamma'] = l.Logic_gamma.check_status
method_dict['delta'] = l.Logic_delta.check_status
method_dict['epsilon'] = l.Logic_epsilon.check_status
method_dict['dca'] = ''

logic_name_list = ['dca','alpha','gamma','delta','epsilon']


class Simulator:
    
    def __init__(self, file_name, base_path='./datas'):
        log.info('Start simulator')
        self.in_file = file_name
        self.base_path = base_path

        self._setup()

    def _setup(self):
        df = DataManager.load_data_from_csv(self.in_file, self.base_path)
        log.debug(df)

        self.stock_list = []
        for name, code, logic, price, stock in zip(df['종목명'],df['Code'],df['logic'],df['price'],df['stock']):
            stock = Stock(name, code, logic, price, stock, method_dict[logic])
            self.stock_list.append(stock)

    def decide_invest(self, end=datetime.date.today()):
        status_list = []
        for s in self.stock_list:
            df = DataManager.load_stock_data(s.code, start="2023-01-01", end=end)

            if s.logic == 'dca':
                print(s.name, 'dca_skip')
                status_list.append('dca_skip')
                continue

            status = s.check_func(df, s.buy_price, s.stock)
            
            #if status == 'buy' or status == 'sell':
            print(s.name, status)
            status_list.append(status)
        return status_list



    """
    def run(self):
        for stock in self.stock_list:
            df = DataManager.load_stock_data(stock.code)
            stock.run(df)
    """

    def check_current_profit(self):
        #for stock in self.stock_list:
        #    df = DataManager.load_stock_data(stock.code)
        #    stock.check_current_profit(df)

        cost = (sum([s.get_cost for s in self.stock_list]))
        curr = (sum([DataManager.load_stock_data(s.code)['Close'][-1] * s.stock for s in self.stock_list if s.stock > 0]))
        print(curr/1000000-1)

    def update_logic(self, end=datetime.date.today()):
        #df = DataManager.load_data_from_csv(self.in_file)
        #log.debug(df)

        logic_class = [l.Logic_dca, l.Logic_alpha, l.Logic_gamma, l.Logic_delta, l.Logic_epsilon]

        logic_list = []
        price_list = []
        stock_list = []

        tqdm.pandas()

        for s in self.stock_list:
            stock_df = DataManager.load_stock_data(s.code, start='2023-01-01', end=end)
            ret_list = []

            if s.stock == 0:
                ret_list.append([obj.run_logic(stock_df) for obj in logic_class])
                ret_list = sum(ret_list,[])
                update_logic = logic_name_list[ret_list.index(max(ret_list))]
                s.logic = update_logic
                #logic_list.append(logic_name_list[ret_list.index(max(ret_list))])
                logic_list.append(update_logic)
                #stock_list.append(0)
                #price_list.append(0)

            else:
                logic_list.append(s.logic)
                #stock_list.append(s.stock)
                #price_list.append(s.buy_price)

            
        
        """

        for name, code, stock, price, logic in tqdm(zip(df['종목명'],df['Code'],df['stock'],df['price'],df['logic'])):
            stock_df = DataManager.load_stock_data(code, start='2023-01-01', end=end)
            ret_list = []

            if stock == 0:
                ret_list.append([obj.run_logic(stock_df) for obj in logic_class])
                ret_list = sum(ret_list,[])
                logic_list.append(logic_name_list[ret_list.index(max(ret_list))])
                stock_list.append(0)
                price_list.append(0)

            else:
                logic_list.append(logic)
                stock_list.append(stock)
                price_list.append(price)

        df['logic'] = logic_list
        df['price'] = price_list
        df['stock'] = stock_list

        """

        df = pd.DataFrame([ s.to_data_frame  for s in self.stock_list])
        DataManager.save_data_to_csv('test5.csv', df, self.base_path)

        return logic_list


    def make_portfolio(self):
        df = DataManager.load_data_from_csv(self.in_file)

        portfolio_df = df[df['stock'] > 0]

        curr_price_list = []
        earn_rate_list = []

        for code, stock, price in zip(portfolio_df['Code'], portfolio_df['stock'], portfolio_df['price']):
            stock_df = DataManager.load_stock_data(code, '2023-01-01')
            curr_price = stock_df['Close'][-1]
            curr_price_list.append(curr_price)

            earn_rate = curr_price/price - 1
            earn_rate_list.append(earn_rate)


            #logic_class[logic_name_list.index(logic)].run_logic(stock_df)
            #print(logic_idx)

        portfolio_df['curr_price'] = curr_price_list
        portfolio_df['earn_rate'] = earn_rate_list
        DataManager.save_data_to_csv('test4.csv', portfolio_df)

    def test(self):
        df = pd.DataFrame([ s.to_data_frame  for s in self.stock_list])
        print(df)


if __name__ == '__main__':
    obj = Simulator('final_data_1013.csv')
    #obj.run()
    #obj.check_current_profit()
    #obj.update_logic()
    #obj.make_portfolio()
    obj.decide_invest()



