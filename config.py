from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class Config:
    # API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Default Parameters
    DEFAULT_TICKER = os.getenv('DEFAULT_TICKER', 'AAPL')
    DATA_CACHE_DURATION = int(os.getenv('DATA_CACHE_DURATION', 3600))
    
    # Sector Configurations
    SECTOR_CONFIGS = {
        'Technology': {
            'key_metrics': ['R&D Expenses', 'Revenue Growth', 'Profit Margin'],
            'analysis_focus': ['Innovation', 'Market Share', 'Competition']
        },
        'Healthcare': {
            'key_metrics': ['FDA Approvals', 'Clinical Trials', 'Patent Portfolio'],
            'analysis_focus': ['Regulatory Environment', 'Research Pipeline', 'Market Access']
        },
        'Finance': {
            'key_metrics': ['Net Interest Margin', 'NPL Ratio', 'Capital Adequacy'],
            'analysis_focus': ['Interest Rates', 'Credit Quality', 'Regulatory Compliance']
        },
        'Energy': {
            'key_metrics': ['Production Costs', 'Reserves', 'Environmental Impact'],
            'analysis_focus': ['Commodity Prices', 'Sustainability', 'Regulations']
        }
    }
    
    # Gemini Model Configuration
    MODEL_CONFIG = {
        'temperature': 0.7,
        'top_p': 0.8,
        'top_k': 40,
        'max_output_tokens': 2048,
    }
    
    # Technical Analysis Parameters
    TECHNICAL_PARAMS = {
        'short_term_ma': 20,
        'long_term_ma': 50,
        'rsi_period': 14,
        'volatility_window': 20
    }
