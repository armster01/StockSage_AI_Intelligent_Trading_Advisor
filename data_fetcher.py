import yfinance as yf
import requests
from utils import get_date_range
from config import NEWS_API_KEY

def fetch_stock_data(symbol, timeframe='1d'):
    """Fetch historical stock data using yfinance."""
    start_date, end_date = get_date_range(timeframe)
    stock = yf.Ticker(symbol)
    df = stock.history(start=start_date, end=end_date, interval='1h' if timeframe == '1d' else '1d')
    return df

def fetch_news(symbol):
    """Fetch news articles for a given stock symbol."""
    url = f'https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return [article['content'] for article in articles if article['content']]
    return []