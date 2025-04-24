import streamlit as st
from data_fetcher import fetch_stock_data, fetch_news
from analysis_engine import (
    perform_technical_analysis,
    perform_sentiment_analysis,
    generate_trading_signals,
    calculate_position_size,
    generate_heatmap_data,
    perform_sector_analysis,
    summarize_news
)
from backtesting_engine import run_backtest
from portfolio_manager import get_portfolio_data, calculate_portfolio_metrics, assess_risk
from visualization import (
    plot_price_chart,
    plot_technical_indicators,
    plot_heatmap,
    plot_sector_analysis,
    plot_equity_curve
)
from config import DEFAULT_SYMBOL, DEFAULT_TIMEFRAME, DEFAULT_ACCOUNT_SIZE, DEFAULT_RISK_PER_TRADE
from utils import format_dataframe

st.set_page_config(page_title="Stock Market Prediction App", layout="wide")

def main():
    st.title("Stock Market Prediction App")
    
    # Sidebar for user inputs
    with st.sidebar:
        st.header("Settings")
        symbol = st.text_input("Stock Symbol", DEFAULT_SYMBOL).upper()
        timeframe = st.selectbox("Timeframe", ['1d', '1w', '1m', '1y'], index=['1d', '1w', '1m', '1y'].index(DEFAULT_TIMEFRAME))
        account_size = st.number_input("Account Size ($)", min_value=1000, value=DEFAULT_ACCOUNT_SIZE)
        risk_per_trade = st.number_input("Risk per Trade (%)", min_value=0.01, max_value=1.0, value=DEFAULT_RISK_PER_TRADE, step=0.01)

    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Charts & Analysis", "Trading Signals", "Portfolio", "Heatmap & Sector", "News"])

    with tab1:
        st.header("Price and Technical Analysis")
        try:
            stock_data = fetch_stock_data(symbol, timeframe)
            plot_price_chart(stock_data, symbol)
            analysis = perform_technical_analysis(stock_data)
            plot_technical_indicators(stock_data, analysis)
        except Exception as e:
            st.error(f"Error fetching data: {e}")

    with tab2:
        st.header("Trading Signals & Position Sizing")
        try:
            stock_data = fetch_stock_data(symbol, timeframe)
            signals = generate_trading_signals(stock_data)
            if signals:
                st.subheader("Trading Signals")
                st.table(signals)
            else:
                st.info("No trading signals generated.")
            
            position = calculate_position_size(stock_data, account_size, risk_per_trade)
            st.subheader("Position Sizing")
            st.write(f"Position Size: {position['position_size']:.2f} shares")
            st.write(f"Stop Loss: ${position['stop_loss']:.2f}")
            st.write(f"Risk Amount: ${position['risk_amount']:.2f}")
        except Exception as e:
            st.error(f"Error generating signals: {e}")

    with tab3:
        st.header("Portfolio Tracker & Risk Management")
        try:
            portfolio = get_portfolio_data()
            metrics = calculate_portfolio_metrics(portfolio)
            risk = assess_risk(portfolio)
            
            st.subheader("Portfolio Metrics")
            st.write(f"Total Value: ${metrics['total_value']:.2f}")
            st.write(f"Average Return: {metrics['average_return']*100:.2f}%")
            st.write(f"Holdings: {metrics['holdings']}")
            
            st.subheader("Risk Assessment")
            st.write(f"VaR (5%): {risk['var_5_percent']*100:.2f}%")
            st.write(f"Volatility: {risk['volatility']*100:.2f}%")
            
            st.subheader("Backtesting")
            stock_data = fetch_stock_data(symbol, '1y')
            stock_data = stock_data.reset_index()
            backtest_results = run_backtest(stock_data)
            st.write(f"Backtest Return: {backtest_results['return']:.2f}%")
            st.write(f"Sharpe Ratio: {backtest_results['sharpe']:.2f}")
            plot_equity_curve(backtest_results)
        except Exception as e:
            st.error(f"Error in portfolio section: {e}")

    with tab4:
        st.header("Heatmap & Sector Analysis")
        try:
            heatmap_data = generate_heatmap_data()
            plot_heatmap(heatmap_data)
            
            sector_analysis = perform_sector_analysis()
            plot_sector_analysis(sector_analysis)
        except Exception as e:
            st.error(f"Error in heatmap/sector analysis: {e}")

    with tab5:
        st.header("Sentiment Analysis & News Summary")
        try:
            news_articles = fetch_news(symbol)
            sentiment = perform_sentiment_analysis(news_articles)
            st.subheader("Sentiment Analysis")
            st.write(f"Average Sentiment: {sentiment['average_sentiment']:.2f}")
            st.write(f"Article Count: {sentiment['article_count']}")
            
            summary = summarize_news(news_articles)
            st.subheader("AI News Summary")
            st.write(summary)
        except Exception as e:
            st.error(f"Error in news section: {e}")

if __name__ == "__main__":
    main()
