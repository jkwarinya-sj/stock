
import yfinance as yf
import sys
import pandas as pd


class ER_calc:
    def __init__(self, ticker='schd', dist=0.0783, name='tmp'):
        #print("class loading")
        self.ticker = str(ticker)
        self.dist = float(dist)
        self.name = name

        data = yf.Ticker(ticker)
        self.df = data.history(period="6y")

        #print(self.df)


    def calc(self):
        #period_arr=[1,2,3,4,5,6,7,8,9,10]
        period_arr=[1,2,3,4,5]
        total_avr = []
        year = 252
        for p in period_arr:
            idx = 0
            avr_list = []
            for close in self.df['Close']:
                idx = idx+1
                if(idx < (year+1)*p):
                    continue

                pre_close = self.df['Close'][idx-(year*p)]
                #print(close, pre_close, close/pre_close-1)

                dist = 0
                for i in range(p):
                    dist = dist + self.df['Close'][idx-(year*(i+1))]*self.dist

                avr_list.append((close + dist)/pre_close-1)

            try:
                average = sum(avr_list) / len(avr_list)
                #print(p,average)
                total_avr.append(average)
            except ZeroDivisionError:
                #print(p,0)
                total_avr.append(0)

        t_avr = sum(total_avr) / len(total_avr)
        print(self.name, self.ticker ,round(t_avr*100,2))


if __name__ == '__main__':
    #obj = ER_calc()
    #obj.calc()

    f = open("list.a")
    f_lines = f.readlines()

    for t in f_lines:
        price = float(t.split(' ')[2])

        if price >= 10.0:
            #obj = ER_calc(t.split(' ')[0], t.split(' ')[1], t.split(' ')[3].split('\n')[0])
            obj = ER_calc(t.split(' ')[0], t.split(' ')[1])
            obj.calc()
        #print(t.split(' ')[0])


