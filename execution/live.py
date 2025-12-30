from binance.client import Client
import os
import time
from datetime import datetime, timezone, UTC
from dotenv import load_dotenv
from strategy.strategy import EMAStrategy


class LiveTest:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("BINANCE_API_KEY_TEST")
        api_secret = os.getenv("BINANCE_API_SECRET_TEST")

        if not api_key or not api_secret:
            raise RuntimeError("Binance Testnet API keys missing")

        self.client = Client(api_key, api_secret, testnet=True)
        self.strategy = EMAStrategy()
        self.symbol = "BTCUSDT"
        self.qty = 0.001
        self.in_position = False

        self.csv_file = "logs/live_trades.csv"

        if not os.path.exists(self.csv_file):
            with open(self.csv_file, "w") as f:
                f.write("EntryTime,ExitTime,EntryPrice,ExitPrice,Size,Symbol,Direction\n")

    def run(self):

        start_time = time.time()
        max_duration = 5 * 60 * 60

        while time.time() - start_time < max_duration:
            ticker = self.client.get_symbol_ticker(symbol=self.symbol)
            price = float(ticker["price"])

            signal, _ = self.strategy.eval(price)

            print(f"{datetime.utcnow()} | Price: {price} | Signal: {signal}")

            if signal == "BUY" and not self.in_position:
                self.client.order_market_buy(
                    symbol=self.symbol,
                    quantity=self.qty
                )
                self.in_position = True
                self.entry_time = datetime.now(UTC)
                self.entry_price = price
                print("BUY executed")

            elif signal == "EXIT" and self.in_position:
                exit_time = datetime.now(UTC)
                exit_price = price
    
                self.client.order_market_sell(
                    symbol=self.symbol,
                    quantity=self.qty
                )
    
                with open(self.csv_file, "a") as f:
                    f.write(
                        f"{self.entry_time},"
                        f"{exit_time},"
                        f"{self.entry_price},"
                        f"{exit_price},"
                        f"{self.qty},"
                        f"{self.symbol},"
                        f"BUY\n"
                    )
    
                self.in_position = False
                self.entry_time = None
                self.entry_price = None
                print("SELL executed")            

            time.sleep(60)


if __name__ == "__main__":
    live = LiveTest()
    live.run()

