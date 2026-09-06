"""Loads the user's portfolio holdings from a JSON file."""

import json


def load_portfolio(path: str = "portfolio.json") -> list[dict]:
    """Read the portfolio JSON file and return its list of holdings.

    Each holding is a dict with at least "ticker" and "shares" keys.
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["holdings"]
