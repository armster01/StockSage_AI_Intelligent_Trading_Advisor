import streamlit as st
import pandas as pd
from config import Config
from utils import (
    get_stock_data,
    calculate_technical_indicators,
    create_stock_chart,
    get_ai_analysis,
    generate_trade_signals
)

def main():
    st.set_page_config(page_title="Stock Market Advisor", layout="wide")
    
    st.title("Stock Market Advisor")
    
    # Sidebar - User Settings
    st.sidebar.header("Settings")
    
    # Stock Symbol Input
    symbol = st.sidebar.text_input("Enter Stock Symbol", "AAPL").upper()
    
    # Time Period Selection
    timeframe = st.sidebar.selectbox(
        "Select Time Period",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=2
    )
    
    # Risk Profile
    risk_tolerance = st.sidebar.selectbox(
        "Risk Tolerance",
        ["Conservative", "Moderate", "Aggressive"],
        index=1
    )
    
    # Investment Budget
    budget = st.sidebar.number_input(
        "Investment Budget ($)",
        min_value=1000,
        value=Config.DEFAULT_BUDGET,
        step=1000
    )
    
    # Fetch and process stock data
    df = get_stock_data(symbol, timeframe)
    
    # 🛠 Debugging: Display fetched data
    st.write("Fetched Data Preview:", df.head())

    # ✅ Handling Empty DataFrame
    if df is None or df.empty:
        st.error("Stock data is empty. Please check the symbol or try a different time period.")
        return

    # ✅ Ensure 'Close' Column Exists
    if 'Close' not in df.columns:
        st.error("Close price data is missing. Try a different stock or period.")
        return
    
    # Calculate technical indicators
    df = calculate_technical_indicators(df)
    
    # Display stock chart in full width
    st.subheader("Stock Chart and Technical Analysis")
    chart = create_stock_chart(df, symbol)
    st.plotly_chart(chart, use_container_width=True)
    
    # Display current price and basic stats in columns
    col1, col2, col3 = st.columns(3)
    
    current_price = df['Close'].iloc[-1]
    price_change = df['Close'].iloc[-1] - df['Close'].iloc[-2]
    price_change_pct = (price_change / df['Close'].iloc[-2]) * 100
    
    with col1:
        st.metric(
            "Current Price",
            f"${current_price:.2f}",
            f"{price_change_pct:.2f}%"
        )
    
    with col2:
        st.metric("RSI", f"{df['RSI'].iloc[-1]:.2f}")
    
    with col3:
        st.metric("MACD", f"{df['MACD'].iloc[-1]:.2f}")
    
    # AI Analysis and Trading Signals in two columns
    col_analysis, col_signals = st.columns(2)
    
    with col_analysis:
        st.subheader("AI Analysis")
        analysis = get_ai_analysis(df, symbol)
        st.write(analysis)
    
    with col_signals:
        st.subheader("Trading Signals")
        signals = generate_trade_signals(df)
        
        if signals:
            for signal, reason in signals:
                color = "green" if signal == "BUY" else "red"
                st.markdown(
                    f"<div style='padding: 10px; border-radius: 5px; "
                    f"background-color: {color}; color: white;'>"
                    f"<b>{signal}</b>: {reason}</div>",
                    unsafe_allow_html=True
                )
        else:
            st.info("No clear trading signals at the moment.")
    
    # Position Sizing Calculator
    st.subheader("Position Sizing")
    max_position = budget * (
        0.02 if risk_tolerance == "Conservative"
        else 0.05 if risk_tolerance == "Moderate"
        else 0.10
    )
    
    shares = int(max_position / current_price)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Recommended Position:")
        st.write(f"- Shares: {shares}")
        st.write(f"- Total Value: ${(shares * current_price):.2f}")
    with col2:
        st.write("Risk Profile:")
        st.write(f"- Maximum Position Size: ${max_position:.2f}")
        st.write(f"- Risk Level: {risk_tolerance}")

if __name__ == "__main__":
    main()
