import pandas as pd
import numpy as np
from data_fetcher import fetch_stock_data

def get_portfolio_data():
    """Fetch portfolio data (mock implementation)."""
    portfolio = [
        {'symbol': 'AAPL', 'shares': 100, 'avg_price': 150.0},
        {'symbol': 'MSFT', 'shares': 50, 'avg_price': 300.0}
    ]
    return portfolio

def calculate_portfolio_metrics(portfolio):
    """Calculate portfolio metrics."""
    total_value = 0
    returns = []
    for holding in portfolio:
        data = fetch_stock_data(holding['symbol'], '1m')
        current_price = data['Close'][-1]
        value = holding['shares'] * current_price
        total_value += value
        holding_return = (current_price - holding['avg_price']) / holding['avg_price']
        returns.append(holding_return)
    
    return {
        'total_value': total_value,
        'average_return': np.mean(returns) if returns else 0.0,
        'holdings': len(portfolio)
    }

def assess_risk(portfolio):
    """Assess portfolio risk using VaR."""
    returns = []
    for holding in portfolio:
        data = fetch_stock_data(holding['symbol'], '1m')
        daily_returns = data['Close'].pct_change().dropna()
        returns.extend(daily_returns)
    
    var = np.percentile(returns, 5)  # 5% VaR
    return {
        'var_5_percent': var,
        'volatility': np.std(returns) * np.sqrt(252) if returns else 0.0
    }