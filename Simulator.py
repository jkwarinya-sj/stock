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
        for name, code, logic, price, stock in zip(df['Name'],df['Code'],df['Logic'],df['Price'],df['Stock']):
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
        print(curr/1000000-1, curr-1000000)

    def update_logic(self, end=datetime.date.today(), out_file='test.csv'):
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
        DataManager.save_data_to_csv(out_file, df, self.base_path)

        return logic_list


    def make_portfolio(self, out_file='test.csv'):
        today = datetime.date.today()
        out_file = today.strftime("%y%m%d") + '.csv'
        df = DataManager.load_data_from_csv(self.in_file)

        portfolio_df = df[df['Stock'] > 0].copy()

        buying_price_list = []
        current_price_list = []
        profit_list = []
        return_rate_list = []
        
        for s in self.stock_list:
            if s.stock > 0:
                stock_df = DataManager.load_stock_data(s.code, '2023-01-01')
        
                buying_price = s.get_cost
                current_price = stock_df['Close'].iloc[-1] * s.stock
                profit = current_price - buying_price
                return_rate = current_price/buying_price - 1

                buying_price_list.append(round(buying_price,0))
                current_price_list.append(round(current_price,0))
                profit_list.append(round(profit,0))
                return_rate_list.append(round(return_rate,3))


        portfolio_df['Buying_price'] = buying_price_list
        portfolio_df['Current_price'] = current_price_list
        portfolio_df['Profit'] = profit_list
        portfolio_df['Return_rate'] = return_rate_list

        total_buying_price = 1000000
        total_current_price = sum(current_price_list)
        total_profit = total_current_price - total_buying_price
        total_return_rate = total_current_price/total_buying_price - 1


        new_row = pd.DataFrame([{'Name': 'Summary', 'Buying_price': total_buying_price, 'Current_price':total_current_price, 'Profit':total_profit, 'Return_rate':total_return_rate}])
        portfolio_df = pd.concat([portfolio_df, new_row], ignore_index=True)

        DataManager.save_data_to_csv(out_file, portfolio_df)

    def test(self):
        df = pd.DataFrame([ s.to_data_frame  for s in self.stock_list])
        print(df)


if __name__ == '__main__':
    obj = Simulator('invest_1017.csv')
    #obj.run()
    #obj.check_current_profit()
    #obj.update_logic()
    obj.make_portfolio()
    #obj.decide_invest()



