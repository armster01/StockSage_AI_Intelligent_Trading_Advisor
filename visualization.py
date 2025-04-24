import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import format_dataframe

def plot_price_chart(data, symbol):
    """Plot interactive price chart with candlestick and volume bar charts."""
    fig = go.Figure()

    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlestick'
    ))

    # Volume bar chart on secondary y-axis
    fig.add_trace(go.Bar(
        x=data.index,
        y=data['Volume'],
        name='Volume',
        marker_color='lightblue',
        yaxis='y2'
    ))

    # Layout settings
    fig.update_layout(
        title=f'{symbol} Price and Volume',
        xaxis_title='Date',
        yaxis_title='Price',
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right',
            showgrid=False,
            position=0.15
        ),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )

    st.plotly_chart(fig)

def plot_technical_indicators(data, analysis):
    """Plot technical indicators (SMA, RSI, MACD)."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close Price'))
    fig.add_trace(go.Scatter(x=data.index, y=analysis['sma'], name='SMA (20)'))
    fig.update_layout(title='Price and SMA', xaxis_title='Date', yaxis_title='Price')
    st.plotly_chart(fig)

    fig_rsi = px.line(x=data.index, y=analysis['rsi'], title='RSI')
    fig_rsi.update_layout(xaxis_title='Date', yaxis_title='RSI')
    st.plotly_chart(fig_rsi)

    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=data.index, y=analysis['macd'], name='MACD'))
    fig_macd.add_trace(go.Scatter(x=data.index, y=analysis['signal'], name='Signal'))
    fig_macd.update_layout(title='MACD', xaxis_title='Date', yaxis_title='Value')
    st.plotly_chart(fig_macd)

def plot_heatmap(heatmap_data):
    """Plot performance heatmap."""
    df = pd.DataFrame(heatmap_data)
    # Create a non-negative size variable for marker size
    size_values = df['return'].abs()
    fig = px.scatter(df, x='volatility', y='return', color='return', size=size_values,
                     hover_data=['symbol'], title='Performance Heatmap')
    fig.update_layout(xaxis_title='Volatility', yaxis_title='Return')
    st.plotly_chart(fig)

def plot_sector_analysis(analysis):
    """Plot sector performance."""
    df = pd.DataFrame(analysis)
    fig = px.bar(df, x='sector', y='performance', title='Sector Performance')
    fig.update_layout(xaxis_title='Sector', yaxis_title='Annualized Return')
    st.plotly_chart(fig)

def plot_equity_curve(backtest_results):
    """Plot backtest equity curve."""
    df = pd.DataFrame(backtest_results['equity_curve'])
    fig = px.line(df, x='Date', y='Equity', title='Backtest Equity Curve')
    fig.update_layout(xaxis_title='Date', yaxis_title='Equity')
    st.plotly_chart(fig)