from backtesting import Backtest, Strategy
from data.market_data import MarketData
from strategy.strategy import EMAStrategy

class BacktestStrategy(Strategy):
    def init(self):
        self.core = EMAStrategy()

    def next(self):
        price = self.data.Close[-1]
        low = self.data.Low[-1]

        signal, qty = self.core.eval(price)

        if signal == "BUY" and not self.position:
            risk = price - low
            self.buy(
                size = qty,
                sl = low,
                tp = price + 3*risk
            )

        elif signal == "EXIT" and self.position:
            self.position.close()

data = MarketData.getMarketData("BTC-USD", "2y", "1d")

bt = Backtest(
    data,
    BacktestStrategy,
    cash=100000,
    commission=0.0005
)

stats = bt.run()

# print(stats)

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

trades_df.to_csv("logs/backtest_trade.csv", index=False)

