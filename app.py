import streamlit as st
import plotly.graph_objects as go
from utils import StockAnalyzer
from config import Config
import asyncio

class StockSageApp:
    def __init__(self):
        self.config = Config()
        self.analyzer = StockAnalyzer()
        
    def setup_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="StockSage AI",
            page_icon="📈",
            layout="wide"
        )
        st.title("📈 StockSage AI")
        st.subheader("AI-Powered Stock Analysis with Gemini")
    
    def create_sidebar(self):
        """Create and handle sidebar inputs"""
        st.sidebar.title("Analysis Parameters")
        ticker = st.sidebar.text_input(
            "Enter Stock Ticker",
            self.config.DEFAULT_TICKER
        ).upper()
        
        sector = st.sidebar.selectbox(
            "Select Sector",
            list(self.config.SECTOR_CONFIGS.keys())
        )
        
        return ticker, sector
    
    def plot_stock_chart(self, data):
        """Create interactive stock price chart"""
        if data.empty:
            st.error("No data available for the selected stock.")
            return None
            
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="OHLC"
        )])
        
        # Add moving averages if enough data points are available
        if len(data) >= 20:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['SMA20'],
                name="20 Day MA",
                line=dict(color='orange')
            ))
        
        if len(data) >= 50:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['SMA50'],
                name="50 Day MA",
                line=dict(color='blue')
            ))
        
        fig.update_layout(
            title="Stock Price Analysis",
            yaxis_title="Price",
            xaxis_title="Date",
            template="plotly_white"
        )
        
        return fig
    
    def display_technical_indicators(self, data):
        """Display technical analysis indicators"""
        if data is None or 'technical_indicators' not in data:
            st.error("Technical indicators data not available.")
            return
            
        tech_data = data['technical_indicators']
        
        cols = st.columns(4)
        cols[0].metric("Trend", tech_data['trend'])
        cols[1].metric("RSI", f"{tech_data['rsi']:.2f}")
        cols[2].metric("Volatility", f"{tech_data['volatility']:.2%}")
        cols[3].metric(
            "Price Action",
            "Above MA" if tech_data['sma20'] > tech_data['sma50'] else "Below MA"
        )
    
    async def run(self):
        """Main application loop"""
        self.setup_page()
        ticker, sector = self.create_sidebar()
        
        if st.sidebar.button("Analyze"):
            try:
                with st.spinner("Fetching data and generating analysis..."):
                    # Get stock data
                    stock_data = self.analyzer.get_stock_data(ticker)
                    
                    if stock_data is None or stock_data['historical_data'].empty:
                        st.error(f"No data available for ticker {ticker}. Please check if the ticker symbol is correct.")
                        return
                    
                    # Create tabs
                    tab1, tab2, tab3 = st.tabs([
                        "Stock Analysis",
                        "Technical Indicators",
                        "AI Insights"
                    ])
                    
                    with tab1:
                        chart = self.plot_stock_chart(stock_data['historical_data'])
                        if chart is not None:
                            st.plotly_chart(chart, use_container_width=True)
                    
                    with tab2:
                        self.display_technical_indicators(stock_data)
                    
                    with tab3:
                        ai_analysis = await self.analyzer.get_ai_analysis(
                            ticker,
                            stock_data,
                            sector
                        )
                        st.markdown(ai_analysis)
                
            except Exception as e:
                st.error(f"Error analyzing stock: {str(e)}")

def main():
    app = StockSageApp()
    asyncio.run(app.run())

if __name__ == "__main__":
    main()
