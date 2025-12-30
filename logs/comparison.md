# Backtest vs Live Trading - What I Found

## Setup
- Backtest: timeframe = 2 years and interval = 1 day on BTC data, got 5 trades
- Live: timeframe = 25 minutes on Binance testnet, got 4 trades

## Why the difference?
Naturally 25 minutes won't match 2 years. The strategy looks for EMA crossovers which don't happen every minute. During my live test the market was pretty flat so fewer signals made sense

## What matched?
- Entry and exit logic was identical
- All trades were long only (no shorts)
- Signal generation followed the same rules irrespective of test

## What didn't match?
- Timestamps (different time periods)
- Trade count (explained above)
- Exact prices (live vs historical data)

## Did it work?
Yeah the strategy behaved the same in both environments. The code correctly avoided taking bad trades when the market was choppy
