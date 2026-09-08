"""Fetches recent news headlines for a ticker via the Finnhub API."""

from datetime import date, timedelta

import requests

FINNHUB_NEWS_URL = "https://finnhub.io/api/v1/company-news"


def get_news(ticker: str, api_key: str) -> list[dict]:
    """Fetch recent company news headlines for a ticker from Finnhub.

    Calls Finnhub's "company news" endpoint for the given ticker, covering
    the last 3 days, and returns the 3 most recent articles.

    Args:
      ticker: the stock symbol to look up, e.g. "AAPL" or "ASML.AS".
      api_key: your Finnhub API token (config.FINNHUB_API_KEY).

    Returns:
      A list of up to 3 dicts, newest first, each shaped like:
        {"headline": <str>, "summary": <str>}
      Returns an empty list if the request fails for any reason (bad
      response, network error, invalid ticker) or if Finnhub has no news
      to report — this function must never raise, since missing news
      should never crash the rest of the pipeline.

    This function must only fetch and return news metadata — it must NOT
    compute or infer any numeric values about the holding's performance.
    """
    # Finnhub wants the date range as plain YYYY-MM-DD strings. We ask for
    # everything published in the last 3 calendar days.
    today = date.today()
    three_days_ago = today - timedelta(days=3)

    params = {
        "symbol": ticker,
        "from": three_days_ago.isoformat(),
        "to": today.isoformat(),
        "token": api_key,
    }

    try:
        # timeout=10 makes sure a slow/unresponsive API can't hang the
        # whole pipeline forever.
        response = requests.get(FINNHUB_NEWS_URL, params=params, timeout=10)
        # raise_for_status() turns a 4xx/5xx HTTP response (bad ticker,
        # bad API key, rate limit, etc.) into an exception, which we
        # catch below instead of letting it propagate.
        response.raise_for_status()
        articles = response.json()
    except requests.RequestException:
        # Covers connection errors, timeouts, and the bad-status errors
        # raised by raise_for_status() above.
        return []

    # A healthy response is a list of article dicts. If Finnhub ever sends
    # back something else, or simply has no articles, there's nothing to
    # sort or map — just report "no news found".
    if not isinstance(articles, list) or not articles:
        return []

    # Finnhub's docs say articles come back newest first, but we sort
    # explicitly by the "datetime" field (a Unix timestamp) rather than
    # trust that ordering, in case it's ever wrong or changes.
    articles.sort(key=lambda article: article.get("datetime", 0), reverse=True)

    # Keep only the 3 most recent, and map Finnhub's field names onto the
    # simple {headline, summary} shape the rest of the app expects.
    return [
        {"headline": article.get("headline", ""), "summary": article.get("summary", "")}
        for article in articles[:3]
    ]
