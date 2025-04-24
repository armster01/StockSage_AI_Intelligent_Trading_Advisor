from datetime import datetime, timedelta
import pandas as pd

def get_date_range(timeframe):
    """Calculate start and end dates based on timeframe."""
    end_date = datetime.now()
    if timeframe == '1d':
        start_date = end_date - timedelta(days=1)
    elif timeframe == '1w':
        start_date = end_date - timedelta(days=7)
    elif timeframe == '1m':
        start_date = end_date - timedelta(days=30)
    elif timeframe == '1y':
        start_date = end_date - timedelta(days=365)
    else:
        start_date = end_date - timedelta(days=30)
    return start_date, end_date

def format_dataframe(df):
    """Format DataFrame for Streamlit display."""
    return df.reset_index().round(2)
