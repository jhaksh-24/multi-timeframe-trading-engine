# Project Title  
**Multi Timeframe Strategy Execution & Trade Matching**  

A multi timeframe execution of a strategy (EMA here) to decide whether to execute a trade or not in both **backtest** and **live trade** environments.  

---

## Project Objective  

The objective of this project plays on four fronts which are as follows:

- A strictly deterministic rule based quantitative trading strategy implementation  
- Implementation of the strategy in a clean and modular class based architecture  
- Ensured identical behaviour on backtest trades and live trades, irrespective of timeframes  
- A clean distinction between **strategy logic**, **execution logic**, and **logging**  

---

## High Level Architecture  

Multi Timeframe Strategy Execution & Trade Matching
├── data
│ ├── init.py
│ ├── market_data.py
│ └── pycache
│ ├── init.cpython-313.pyc
│ └── market_data.cpython-313.pyc
├── execution
│ ├── backtest.py
│ ├── init.py
│ ├── live.py
│ └── pycache
│ ├── backtest.cpython-313.pyc
│ ├── engine.cpython-313.pyc
│ ├── init.cpython-313.pyc
│ └── live.cpython-313.pyc
├── logs
│ ├── backtest_trades.csv
│ ├── backup_live_trades.csv
│ └── live_trades.csv
├── README.md
└── strategy
├── init.py
├── pycache
│ ├── init.cpython-313.pyc
│ └── strategy.cpython-313.pyc
└── strategy.py


---

## Directory Overview  

- **data/** -> Uses *yfinance* to get market data, which is used by `execution/backtest.py` for backtesting.  
- **execution/** -> Contains two engines for executing trades : `backtest.py` and `live.py`.  
  - **backtest.py** -> Uses the framework *backtesting.py* to backtest our EMA strategy (`strategy/strategy.py`) and stores logs in `logs/backtest_trades.csv`.  
  - **live.py** -> Implemented using the *Binance Testnet REST API*, reuses the same EMA strategy logic, and logs to `logs/live_trades.csv`.  
- **strategy/** -> Implements the core EMA logic in `strategy.py`, returning both position size and signal.  
- **logs/** -> Stores logs from both execution files (`backtest_trades.csv` and `live_trades.csv`).  

---

## Strategy Logic  

The strategy implemented is **Exponential Moving Average (EMA)** and is defined through two functions that is  
`eval()` and `EMA()` (which essentially is the math behind EMA).

### EMA Calculation Logic  

At a given time *t*:
- Inputs: time period, EMA at *t-1*, and new price  
- The smoothing factor (alpha) is defined as:  
    alpha = 2 / (time period + 1)
- The recursive formula for EMA:  
    EMA_t = (alpha * new_price) + ((1 - alpha) * EMA_(t-1))

    (Though I didn’t use recursion in code the design remembers the last state in the application logic itself for performance reasons.)

- If an EMA at *t-1* doesn’t exist, we initialize it with a **Simple Moving Average (SMA)**, which is the basically mean of prices over the given period.

### Strategy Application  

We use this in three timeframes:
- **ema_9**
- **ema_44**
- **ema_100**

where 9, 44, and 100 are the time periods.

We append the new price to the list, store the last EMA values, then calculate the new states:

- If `new_price > ema_100` and **ema_9 has a positive crossover** at **ema_44**  
(`ema_9 > ema_44` and `ema_9_old <= ema_44_old`)  
-> Generate a **BUY** signal with position size 1 (in `live.py`, this is overridden to 0.001 since it’s BTC).

- If `new_price < ema_100` and **ema_9 has a negative crossover** at **ema_44**  
(`ema_9 < ema_44` and `ema_9_old >= ema_44_old`)  
-> Generate an **EXIT** signal.

- Otherwise -> Generate a **HOLD** signal with position size 0.

---

## Backtesting Implementation  

- We use the framework **backtesting.py** to simulate our strategy.  
- A wrapper class `BacktestStrategy` is implemented over the original `EMAStrategy` class (which contains the actual logic).  
- The `BacktestStrategy` inherits from the `Strategy` class of *backtesting.py*.  
- The `init()` method initializes an instance of `EMAStrategy`.  
- The `next()` method sets up the new price and low values, calls `EMAStrategy.eval()`, and executes trades based on the signal:  
- `BUY` -> opens a position  
- `EXIT` -> closes a position  

### Data & Execution  
- Uses historical BTC data (`BTC-USD`) fetched via *yfinance*  
- The Backtest instance is created with parameters such as:
- `data`
- `strategy`
- `commission`
- `cash`
- The results from `bt.run()` are logged in `logs/backtest_trades.csv`.

---

## Live Trading System (Binance Testnet REST API)  

- Implemented via a `LiveTest` class.
- Initialized with `BINANCE_API_KEY_TEST` and `BINANCE_API_SECRET_TEST` from `.env` (which is `.gitignore`d).  
- Creates instances of:
- **Client** (Binance Testnet)
- **Strategy**
- Symbol used: **BTCUSDT** (unlike `BTC-USD` in yfinance)
- Quantity is set to **0.001**, position initialized to **False**.  
- Execution runs within a timed loop until `time < max_duration`.

### Execution Flow  

This loop represents a **live execution engine** that:
1. Continuously polls market data  
2. Evaluates the strategy  
3. Conditionally places orders on Binance Testnet  

**Endpoints used:**
- `get_symbol_ticker(...)` -> Wrapper over `GET /api/v3/ticker/price` for latest prices.  
- `order_market_buy(...)` -> Wrapper over Binance’s market buy API.  
- `order_market_sell(...)` -> Wrapper over Binance’s market sell API.  
- `time.sleep()` -> Defines our polling interval.  

Logs are stored in **logs/live_trades.csv**.

---

## Setup & Configuration  

The setup is intentionally minimal.  
Before running, you must configure your Binance Testnet API keys.

### Step 1 : Create `.env` File  

Create a file named `.env` in the project root and add:

BINANCE_API_KEY_TEST=your_testnet_api_key
BINANCE_API_SECRET_TEST=your_testnet_api_secret


These credentials are:
- Used to fetch market data and execute test trades  
- Never exposed or uploaded (the `.env` file is in `.gitignore`)  

### Step 2 : Install Dependencies  

pip install -r requirements.txt

### Step 3 : Run Backtest or Live Trading  

To run the backtest:

python -m execution.backtest

To run live trading:

python -m execution.live


---

## Design Intent  

One major design intent was that the **execution engine logic** is deliberately made **thin and stateless** with respect to strategy logic.

All trading decisions originate exclusively from the **strategy layer**, ensuring:
- Consistency between backtesting and live trading  
- Easier debugging  
- Deterministic results  

---

## Order Execution & Trade Logging  

Completed trades are persisted to disk in CSV format.  

Each record includes:
- Entry time  
- Exit time  
- Entry price  
- Exit price  
- Quantity  
- Symbol  
- Trade direction  

This file acts as an **execution log** independent of terminal output.  

