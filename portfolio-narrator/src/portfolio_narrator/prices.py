"""Fetches historical price data for portfolio holdings via yfinance."""

import yfinance as yf


def get_price_data(ticker: str) -> tuple[float, float] | None:
    """Fetch the two most recent closing prices for a ticker.

    Downloads the last 5 days of daily price history for `ticker` using
    yfinance, then reads off the closing price of the most recent trading
    day ("today") and the one before it ("prev"). We ask for 5 days
    (instead of just 2) as a buffer, since weekends and market holidays
    mean some calendar days have no trading data at all.

    Args:
      ticker: the stock symbol to look up, e.g. "AAPL" or "ASML.AS".

    Returns:
      A tuple (today_close, prev_close) of the two most recent closing
      prices, or None if fewer than 2 days of price history came back
      (e.g. an invalid ticker, or one with no recent trading data).

    This function must only fetch and return raw price data — it must NOT
    compute percentages, differences, or any other derived numbers. All
    arithmetic belongs in calculations.py.
    """
    # yf.Ticker() doesn't fetch anything by itself — it just gives us a
    # handle to that one stock, which we then ask for data.
    stock = yf.Ticker(ticker)

    # .history() is what actually calls out to Yahoo Finance and downloads
    # a table of daily prices: one row per trading day, with columns like
    # Open, High, Low, Close, Volume. period="5d" means "the last 5
    # calendar days", not "5 trading days" — some of those days may have
    # no row at all if the market was closed.
    history = stock.history(period="5d")

    # If the ticker is invalid, delisted, or just hasn't traded enough
    # recently, the table can come back empty or with only one row. We
    # need at least 2 rows to have a "today" and a "previous day", so we
    # bail out with None rather than crashing on a missing row.
    if len(history) < 2:
        return None

    # yfinance returns rows ordered oldest to newest, so the last row is
    # the most recent close and the one before it is the previous close.
    today_close = history["Close"].iloc[-1]
    prev_close = history["Close"].iloc[-2]

    # The values above are numpy float64 (yfinance uses pandas under the
    # hood). We convert to plain Python float so the rest of the app
    # (calculations.py) works with ordinary numbers, not numpy types.
    return (float(today_close), float(prev_close))
