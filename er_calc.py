
import yfinance as yf
import sys
import pandas as pd
import queue


class ER_calc:
    def __init__(self, ticker='schd', dist=0.0783, name='tmp'):
        #print("class loading")
        self.ticker = str(ticker)
        self.dist = float(dist)
        self.name = name

        data = yf.Ticker(ticker)
        self.df = data.history(period="11y")

        #print(self.df)


    def calc(self):
        period_arr=[1,2,3,4,5,6,7,8,9,10]
        #period_arr=[1,2,3,4,5]
        total_avr = []
        year = 252
        stock = 1
        div_queue = queue.Queue()
        for p in period_arr:
            idx = 0
            avr_list = []
            for close in self.df['Close']:

                div = self.df['Dividends'][idx]
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
                pre_close = self.df['Close'][idx-(year*p)]
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
        print(self.name, self.ticker ,round(t_avr*100,2), round(min(total_avr)*100,2), round(max(total_avr)*100,2))


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


