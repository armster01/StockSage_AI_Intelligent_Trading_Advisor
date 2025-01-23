class Config:
    # Gemini API settings
    MODEL_NAME = "gemini-pro"
    TEMPERATURE = 0.7
    MAX_TOKENS = 1024
    
    # Technical Analysis Parameters
    RSI_PERIOD = 14
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30
    
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    
    MA_SHORT = 20
    MA_LONG = 50
    
    # Portfolio Settings
    DEFAULT_BUDGET = 10000
    DEFAULT_RISK_TOLERANCE = "Moderate"  # Conservative, Moderate, Aggressive
    
    # Time periods
    DEFAULT_TIMEFRAME = "6mo"  # Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max