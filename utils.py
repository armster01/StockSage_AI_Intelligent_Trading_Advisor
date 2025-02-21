import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import google.generativeai as genai
from config import Config

class StockAnalyzer:
    def __init__(self):
        self.config = Config()
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def get_stock_data(self, ticker, period='1y'):
        """Fetch stock data and calculate technical indicators"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if hist.empty:
                raise ValueError(f"No data found for ticker {ticker}")
            
            # Calculate technical indicators
            hist['SMA20'] = hist['Close'].rolling(window=20).mean()
            hist['SMA50'] = hist['Close'].rolling(window=50).mean()
            hist['RSI'] = self.calculate_rsi(hist['Close'])
            hist['Volatility'] = hist['Close'].pct_change().rolling(window=20).std()
            
            return {
                'historical_data': hist,
                'info': stock.info,
                'technical_indicators': self.get_technical_summary(hist)
            }
        except Exception as e:
            raise Exception(f"Error fetching stock data: {str(e)}")
    
    def calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def get_technical_summary(self, data):
        """Generate technical analysis summary"""
        latest = data.iloc[-1]
        sma20 = latest['SMA20']
        sma50 = latest['SMA50']
        rsi = latest['RSI']
        
        return {
            'trend': 'Bullish' if sma20 > sma50 else 'Bearish',
            'rsi': float(rsi),
            'volatility': float(latest['Volatility']),
            'sma20': float(sma20),
            'sma50': float(sma50)
        }
    
    async def get_ai_analysis(self, ticker, data, sector):
        """Generate AI analysis using Gemini"""
        prompt = self._create_analysis_prompt(ticker, data, sector)
        response = await self.model.generate_content(
            prompt,
            generation_config=self.config.MODEL_CONFIG
        )
        return response.text
    
    def _create_analysis_prompt(self, ticker, data, sector):
        """Create detailed prompt for AI analysis"""
        sector_config = self.config.SECTOR_CONFIGS.get(sector, {})
        technical_data = data['technical_indicators']
        
        return f"""
        Analyze the stock {ticker} in the {sector} sector:
        
        Technical Analysis:
        - Trend: {technical_data['trend']}
        - RSI: {technical_data['rsi']:.2f}
        - Volatility: {technical_data['volatility']:.2%}
        
        Sector-Specific Analysis:
        - Key Metrics: {sector_config.get('key_metrics', [])}
        - Focus Areas: {sector_config.get('analysis_focus', [])}
        
        Please provide:
        1. Market sentiment and trend analysis
        2. Key technical indicators interpretation
        3. Sector-specific insights
        4. Risk assessment
        5. Short-term outlook (1-3 months)
        6. Long-term potential (1-2 years)
        """
