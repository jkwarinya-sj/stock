import requests

def check_yfinance_connection():
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=AAPL"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("✅ yfinance 서버 연결 성공")
            return True
        else:
            print(f"⚠️ 연결 실패: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 연결 오류: {e}")
        return False

check_yfinance_connection()
