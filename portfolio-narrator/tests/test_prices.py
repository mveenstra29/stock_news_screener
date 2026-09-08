"""Tests for prices.py.

These tests make a real network call to Yahoo Finance via yfinance, using
a well-known, stable ticker (AAPL). We don't assert exact price values
since those change every trading day — only that the function returns
the shape it promises without erroring.
"""

from portfolio_narrator.prices import get_price_data


def test_get_price_data():
    result = get_price_data("AAPL")

    # AAPL trades every weekday, so we should always get real data back.
    assert result is not None

    today_close, prev_close = result
    assert isinstance(today_close, float)
    assert isinstance(prev_close, float)

    # Prices should be positive numbers, not zero or negative.
    assert today_close > 0
    assert prev_close > 0
