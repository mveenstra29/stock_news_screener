"""Fetches historical price data for portfolio holdings via yfinance."""


def get_price_data(ticker: str) -> dict:
    """Fetch today's and the previous trading day's closing price for a ticker.

    Should use yfinance (e.g. yf.Ticker(ticker).history(...)) to pull recent
    daily closes and return a dict like:
      {"ticker": ticker, "today_close": <float>, "prev_close": <float>}

    This function must only fetch and return raw price data — it must NOT
    compute percentages, differences, or any other derived numbers. All
    arithmetic belongs in calculations.py.
    """
    # TODO: implement
    raise NotImplementedError
