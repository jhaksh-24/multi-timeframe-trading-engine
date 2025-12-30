from backtesting import Backtest, Strategy
from data.market_data import MarketData
from strategy.strategy import EMAStrategy

class BacktestStrategy(Strategy):

    # Initializing the strategy with EMA core logic
    def init(self):
        self.core = EMAStrategy()

    def next(self):

        # Executing trading logic for each data point
        price = self.data.Close[-1]
        low = self.data.Low[-1]

        signal, qty = self.core.eval(price)
        
        # Entering position with risk-based stop loss and take profit
        if signal == "BUY" and not self.position:
            risk = price - low
            self.buy(
                size = qty,
                sl = low,
                tp = price + 3*risk
            )

        elif signal == "EXIT" and self.position:
            self.position.close()

# Loading historical market data
data = MarketData.getMarketData("BTC-USD", "2y", "1d")

# Configuration and running of backtest
bt = Backtest(
    data,
    BacktestStrategy,
    cash=100000,
    commission=0.0005
)

stats = bt.run()

# print(stats)

# Extracting and formating trade history
trades = stats._trades.copy()

trades_df = trades[[
    "EntryTime",
    "ExitTime",
    "EntryPrice",
    "ExitPrice",
    "Size"
]].copy()

trades_df["Symbol"] = "BTC-USD"
trades_df["Direction"] = trades_df["Size"].apply(
    lambda x: "BUY" if x > 0 else "SELL"
)

# Exporting trade log
trades_df.to_csv("logs/backtest_trades.csv", index=False)

