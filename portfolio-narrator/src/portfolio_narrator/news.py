"""Fetches recent news headlines for a ticker via a news API."""


def get_news(ticker: str) -> list[dict]:
    """Fetch recent news headlines relevant to the given ticker.

    Should use `requests` to call a news API (e.g. NewsAPI, keyed by
    config.NEWS_API_KEY) and return a list of dicts like:
      [{"title": <str>, "url": <str>, "published_at": <str>}, ...]

    This function must only fetch and return news metadata — it must NOT
    compute or infer any numeric values about the holding's performance.
    """
    # TODO: implement
    raise NotImplementedError
