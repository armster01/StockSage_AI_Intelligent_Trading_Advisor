import pandas as pd
import numpy as np
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic import PredictionServiceClient
from config import GEMINI_API_KEY, SYMBOLS_FOR_HEATMAP, SECTOR_ETFS
from data_fetcher import fetch_stock_data
import numpy as np
import pandas as pd

def sma(series, period=20):
    return series.rolling(window=period).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(series, fastperiod=12, slowperiod=26, signalperiod=9):
    fast_ema = series.ewm(span=fastperiod, adjust=False).mean()
    slow_ema = series.ewm(span=slowperiod, adjust=False).mean()
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signalperiod, adjust=False).mean()
    return macd_line, signal_line

def atr(high, low, close, period=14):
    high_low = high - low
    high_close = (high - close.shift()).abs()
    low_close = (low - close.shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

def perform_technical_analysis(data):
    """Perform technical analysis using pandas/numpy."""
    close = data['Close']
    sma_values = sma(close, 20)
    rsi_values = rsi(close, 14)
    macd_line, signal_line = macd(close)
    
    return {
        'sma': sma_values.tolist(),
        'rsi': rsi_values.tolist(),
        'macd': macd_line.tolist(),
        'signal': signal_line.tolist()
    }

def perform_sentiment_analysis(articles):
    """Perform sentiment analysis using Gemini API."""
    aiplatform.init(credentials=GEMINI_API_KEY)
    client = PredictionServiceClient()
    endpoint = "projects/PROJECT_ID/locations/LOCATION/endpoints/ENDPOINT_ID"  # TODO: Replace with your endpoint resource name
    sentiment_scores = []

    for article in articles:
        instance = {
            "content": f"Analyze the sentiment of this financial news article (return a score between -1 and 1): {article}"
        }
        instances = [instance]
        parameters = {
            "temperature": 0.7,
            "maxOutputTokens": 50
        }
        response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)
        try:
            # Assuming the prediction response contains the text in predictions[0]
            score = float(response.predictions[0])
        except (ValueError, IndexError, KeyError):
            score = 0.0
        sentiment_scores.append(score)

    return {
        'average_sentiment': np.mean(sentiment_scores) if sentiment_scores else 0.0,
        'article_count': len(articles)
    }

def generate_trading_signals(data):
    """Generate trading signals based on technical indicators."""
    sma_values = sma(data['Close'], 20)
    signals = []
    for i in range(1, len(data)):
        if data['Close'].iloc[i] > sma_values.iloc[i] and data['Close'].iloc[i-1] <= sma_values.iloc[i-1]:
            signals.append({'date': data.index[i], 'type': 'buy', 'price': data['Close'].iloc[i]})
        elif data['Close'].iloc[i] < sma_values.iloc[i] and data['Close'].iloc[i-1] >= sma_values.iloc[i-1]:
            signals.append({'date': data.index[i], 'type': 'sell', 'price': data['Close'].iloc[i]})
    return signals

def calculate_position_size(data, account_size, risk_per_trade):
    """Calculate position size based on risk management."""
    atr_values = atr(data['High'], data['Low'], data['Close'], 14)
    stop_loss = atr_values.iloc[-1] * 2
    risk_amount = account_size * risk_per_trade
    position_size = risk_amount / stop_loss
    return {
        'position_size': position_size,
        'stop_loss': stop_loss,
        'risk_amount': risk_amount
    }

def generate_heatmap_data():
    """Generate heatmap data for multiple symbols."""
    heatmap = []
    for symbol in SYMBOLS_FOR_HEATMAP:
        data = fetch_stock_data(symbol, '1m')
        returns = data['Close'].pct_change().mean() * 252  # Annualized return
        volatility = data['Close'].pct_change().std() * np.sqrt(252)  # Annualized volatility
        heatmap.append({
            'symbol': symbol,
            'return': returns,
            'volatility': volatility
        })
    return heatmap

def perform_sector_analysis():
    """Perform sector analysis using sector ETFs."""
    analysis = []
    for sector, symbol in SECTOR_ETFS.items():
        data = fetch_stock_data(symbol, '1m')
        performance = data['Close'].pct_change().mean() * 252
        analysis.append({
            'sector': sector,
            'performance': performance,
            'last_price': data['Close'][-1]
        })
    return analysis

def summarize_news(articles):
    """Generate AI-based news summary using Gemini API."""
    aiplatform.init(credentials=GEMINI_API_KEY)
    client = PredictionServiceClient()
    endpoint = "projects/PROJECT_ID/locations/LOCATION/endpoints/ENDPOINT_ID"  # TODO: Replace with your endpoint resource name
    combined_text = " ".join(articles[:5])  # Limit to 5 articles

    instance = {
        "content": f"Summarize the following financial news in 100 words or less: {combined_text}"
    }
    instances = [instance]
    parameters = {
        "temperature": 0.7,
        "maxOutputTokens": 100
    }
    response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)
    try:
        return response.predictions[0]
    except (IndexError, KeyError):
        return ""
