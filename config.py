import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# Default settings
DEFAULT_SYMBOL = 'AAPL'
DEFAULT_TIMEFRAME = '1d'
DEFAULT_ACCOUNT_SIZE = 10000
DEFAULT_RISK_PER_TRADE = 0.01
SYMBOLS_FOR_HEATMAP = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
SECTOR_ETFS = {
    'Technology': 'XLK',
    'Healthcare': 'XLV',
    'Financials': 'XLF',
    'Energy': 'XLE'
}
