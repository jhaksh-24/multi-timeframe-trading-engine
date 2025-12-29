from data.market_data import MarketData
from strategy.strategy import Strategy
from execution.engine import Engine

data_15m = MarketData.getMarketData("BTC-USD", "7d", "15m")
# data_1h  = MarketData.getMarketData("BTC-USD", "7d", "1h")
engine = Engine()
strategy = Strategy()

for time15, candle15 in data_15m.iterrows():
    #valid_1h = data_1h[data_1h.index <= time15]

    #if valid_1h.empty:
    #    continue

    #long_candle = valid_1h.iloc[-1]
    #short_open = candle15["Open"]
    short_close = candle15["Close"]
    #long_open = long_candle["Open"]
    #long_close = long_candle["Close"]
    
    #signal, qty = strategy.eval(short_open, short_close, long_open, long_close)
    signal, qty = strategy.eval(short_close)
    engine.exec(signal, qty)

