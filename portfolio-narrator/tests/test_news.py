"""Tests for news.py.

This test makes a real network call to Finnhub, using a well-known ticker
(AAPL). We don't assert on exact article content since news changes daily
— only that the result matches the shape get_news promises.
"""

from portfolio_narrator import config
from portfolio_narrator.news import get_news


def test_get_news():
    result = get_news("AAPL", config.FINNHUB_API_KEY)

    assert isinstance(result, list)
    for article in result:
        assert isinstance(article, dict)
        assert "headline" in article
        assert "summary" in article
