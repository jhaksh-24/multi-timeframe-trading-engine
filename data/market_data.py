import yfinance as yf

class MarketData:
    @staticmethod
    def getMarketData(ticker_symbol, period, interval):

        ticker = yf.Ticker(ticker_symbol)

        historical_data = ticker.history(period = period, interval = interval)

        # print(f"Summary of Historical Data for {ticker_symbol}:")
        # print(historical_data[['Open', 'High', 'Low', 'Close', 'Volume']].tail())

        return historical_data
