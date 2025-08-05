from prometheus_client import start_http_server, Gauge
import requests
import time
import os

# Finnhub API setup
API_KEY = os.getenv("FINNHUB_API_KEY", "YOUR_API_KEY")
SYMBOL = os.getenv("STOCK_SYMBOL", "AAPL")
FINNHUB_URL = f"https://finnhub.io/api/v1/quote?symbol={SYMBOL}&token={API_KEY}"

# Prometheus metrics
current_price = Gauge('stock_current_price', 'Current stock price')
high_price = Gauge('stock_high_price', 'High price of the day')
low_price = Gauge('stock_low_price', 'Low price of the day')
previous_close = Gauge ('stock_previous_close', 'Previous close price')
dividend_yield = Gauge('stock_dividend_yield', 'Dividend yield')

def fetch_stock_data():
    try:
        response = requests.get(FINNHUB_URL)
        data = response.json()
        current_price.set(data.get('c', 0))
        high_price.set(data.get('h', 0))
        low_price.set(data.get('l', 0))
        previous_close.set(data.get('pc', 0))
        dividend_yield.set(data.get('d', 0))  # Assuming 'd' is the dividend yield key
    except Exception as e:
        print(f"Error fetching stock data: {e}")

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        fetch_stock_data()
        time.sleep(15)
