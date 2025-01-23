import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from ta.trend import MACD
from ta.momentum import RSIIndicator
import google.generativeai as genai
from dotenv import load_dotenv
import os
import ta
from plotly.subplots import make_subplots

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def get_stock_data(symbol, period="6mo"):
    """Fetch stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        return df
    except Exception as e:
        print(f"Error fetching stock data: {str(e)}")
        return None

def calculate_technical_indicators(df):
    """Calculate technical indicators for the stock data"""
    # Calculate RSI
    rsi = RSIIndicator(close=df['Close'], window=14)
    df['RSI'] = rsi.rsi()
    
    # Calculate MACD
    macd = MACD(close=df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    
    # Calculate Moving Averages
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    
    return df

def create_stock_chart(df, symbol):
    """Create an interactive stock chart using Plotly with volume bars"""
    # Create figure with secondary y-axis
    fig = make_subplots(
        rows=2, 
        cols=1, 
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(f'{symbol} Stock Price', 'Volume'),
        row_heights=[0.7, 0.3]
    )

    # Add candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC'
        ),
        row=1, col=1
    )

    # Add Moving Averages to price chart
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['MA20'],
            name='20-day MA',
            line=dict(color='orange', width=1)
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['MA50'],
            name='50-day MA',
            line=dict(color='blue', width=1)
        ),
        row=1, col=1
    )

    # Add volume bars
    colors = ['red' if close < open else 'green' 
              for close, open in zip(df['Close'], df['Open'])]
    
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['Volume'],
            name='Volume',
            marker_color=colors,
            marker_line_width=0
        ),
        row=2, col=1
    )

    # Update layout
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        height=800,  # Increase overall height
        showlegend=True,
        template='plotly_white',
        yaxis_title='Price',
        yaxis2_title='Volume'
    )

    # Update y-axes labels
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    return fig

def get_ai_analysis(stock_data, symbol):
    """Get AI analysis using Gemini API"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Prepare the prompt
        latest_price = stock_data['Close'].iloc[-1]
        rsi = stock_data['RSI'].iloc[-1]
        macd = stock_data['MACD'].iloc[-1]
        macd_signal = stock_data['MACD_Signal'].iloc[-1]
        
        prompt = f"""
        Analyze the following stock data for {symbol}:
        Latest Price: ${latest_price:.2f}
        RSI: {rsi:.2f}
        MACD: {macd:.2f}
        MACD Signal: {macd_signal:.2f}
        
        Provide a brief analysis including:
        1. Current market sentiment
        2. Buy/Sell recommendation
        3. Key reasons for the recommendation
        4. Risk assessment
        
        Be concise and focus on actionable insights.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Error getting AI analysis: {str(e)}")
        return "Unable to generate analysis at this time."

def generate_trade_signals(df):
    """Generate trading signals based on technical indicators"""
    signals = []
    
    # RSI signals
    if df['RSI'].iloc[-1] < 30:
        signals.append(("BUY", "RSI oversold condition"))
    elif df['RSI'].iloc[-1] > 70:
        signals.append(("SELL", "RSI overbought condition"))
    
    # MACD signals
    if df['MACD'].iloc[-1] > df['MACD_Signal'].iloc[-1] and \
       df['MACD'].iloc[-2] <= df['MACD_Signal'].iloc[-2]:
        signals.append(("BUY", "MACD bullish crossover"))
    elif df['MACD'].iloc[-1] < df['MACD_Signal'].iloc[-1] and \
         df['MACD'].iloc[-2] >= df['MACD_Signal'].iloc[-2]:
        signals.append(("SELL", "MACD bearish crossover"))
    
    # Moving Average signals
    if df['MA20'].iloc[-1] > df['MA50'].iloc[-1] and \
       df['MA20'].iloc[-2] <= df['MA50'].iloc[-2]:
        signals.append(("BUY", "Golden Cross (MA20 crosses above MA50)"))
    elif df['MA20'].iloc[-1] < df['MA50'].iloc[-1] and \
         df['MA20'].iloc[-2] >= df['MA50'].iloc[-2]:
        signals.append(("SELL", "Death Cross (MA20 crosses below MA50)"))
    
    return signals