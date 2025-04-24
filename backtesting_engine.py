from backtesting import Backtest, Strategy
import pandas as pd

class SMACrossover(Strategy):
    def sma(self, series, period):
        return series.rolling(window=period).mean()

    def init(self):
        self.sma1 = self.I(self.sma, self.data.Close, 20)
        self.sma2 = self.I(self.sma, self.data.Close, 50)

    def crossover(self, series1, series2):
        return series1[-1] > series2[-1] and series1[-2] <= series2[-2]

    def next(self):
        if self.crossover(self.sma1, self.sma2):
            self.buy()
        elif self.crossover(self.sma2, self.sma1):
            self.sell()

def run_backtest(data, strategy='sma_crossover', params={}):
    """Run backtesting using Backtesting.py."""
    bt = Backtest(data, SMACrossover, cash=10000, commission=.002)
    stats = bt.run()
    return {
        'equity_curve': stats['_equity_curve'][['Equity']].reset_index().to_dict(),
        'trades': stats['_trades'].to_dict(),
        'return': stats['Return [%]'],
        'sharpe': stats['Sharpe Ratio']
    }
