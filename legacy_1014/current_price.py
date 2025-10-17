import yfinance as yf
from DataManagement import DataManagement 


obj_dm = DataManagement()

df = obj_dm.load_data_market_cap('invest_test.csv')


for name, code in zip(df['종목명'],df['Code']):
    ticker = yf.Ticker(code)

    # 최근 1일간의 주가 데이터 가져오기
    hist = ticker.history(period="1d")

    # 마지막 종가 확인 (현재가)
    current_price = hist['Close'].iloc[-1]
    stock = 100000/current_price

    print(f"{name}의 현재가: {current_price}, {stock}")



"""
# Apple 주식 티커 객체 생성
aapl = yf.Ticker("AAPL")

# 최근 1일간의 주가 데이터 가져오기
hist = aapl.history(period="1d")

# 마지막 종가 확인 (현재가)
current_price = hist['Close'].iloc[-1]

print(f"애플(AAPL)의 현재가: {current_price}")
"""
