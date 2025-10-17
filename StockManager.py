import logging
from LogManager import LogManager

log = LogManager.get_logger(logging.DEBUG)

class Stock:
    def __init__(self, name, code, logic, price, stock, check_func):
        self.name = name
        self.code = code
        self.buy_price = price
        self.stock = stock
        self.logic = logic
        self.check_func = check_func

    def run(self, df):
        if self.logic == 'dca':
            print(self.name, 'dca_skip')
            return

        status = ''
        status = self.check_func(df, self.buy_price, self.stock)

        if status == 'buy' or status == 'sell':
            print(self.name, status)

    def check_current_profit(self, df):
        curr_price = df['Close'][-1]
        if self.buy_price != 0:
            print(self.name, self.buy_price*self.stock, curr_price*self.stock, curr_price/self.buy_price-1)

    @property
    def get_cost(self):
        return self.buy_price * self.stock

    @property
    def to_data_frame(self):
        return {
            'Name': self.name,
            'Code': self.code,
            'Logic': self.logic,
            'Price': self.buy_price,
            'Stock': self.stock
        }
            


