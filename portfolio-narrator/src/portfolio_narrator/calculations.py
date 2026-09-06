"""All numeric calculation logic for the portfolio narrator.

This module is the single source of truth for arithmetic in the project.
No other module should ever compute percentages, sums, or other derived
numbers — downstream code (news lookup, narration) must only ever consume
pre-computed values from here, never generate numbers of its own. This
keeps the LLM-facing layer strictly a text-generation layer: it explains
numbers, it does not calculate them.
"""


def calculate_move(ticker: str, shares: float, today_close: float, prev_close: float) -> dict:
    """Calculate the price move for a single holding between two closes.

    Returns a dict with:
      - ticker: str
      - shares: float
      - pct_change: percentage change from prev_close to today_close
      - euro_change: change in position value (in the holding's native currency)
      - today_close: today's closing price, rounded
      - prev_close: previous closing price, rounded
      - value_today: position value at today's close, rounded

    All numeric fields are rounded to 2 decimals.
    """
    pct_change = (today_close - prev_close) / prev_close * 100
    euro_change = (today_close - prev_close) * shares
    value_today = today_close * shares

    return {
        "ticker": ticker,
        "shares": shares,
        "pct_change": round(pct_change, 2),
        "euro_change": round(euro_change, 2),
        "today_close": round(today_close, 2),
        "prev_close": round(prev_close, 2),
        "value_today": round(value_today, 2),
    }


def build_daily_report(moves: list[dict]) -> dict:
    """Aggregate a list of per-holding moves into a daily portfolio report.

    Returns a dict with:
      - total_pct: total percentage change across all holdings, weighted by
        value, rounded to 2 decimals
      - total_euro: total euro change across all holdings, rounded to 2 decimals
      - moves: the input moves sorted by absolute pct_change, descending

    Raises ValueError if moves is empty.
    """
    if not moves:
        raise ValueError("moves must not be empty")

    total_euro = sum(move["euro_change"] for move in moves)
    total_value_today = sum(move["value_today"] for move in moves)
    total_prev_value = total_value_today - total_euro

    total_pct = (total_euro / total_prev_value * 100) if total_prev_value else 0.0

    sorted_moves = sorted(moves, key=lambda move: abs(move["pct_change"]), reverse=True)

    return {
        "total_pct": round(total_pct, 2),
        "total_euro": round(total_euro, 2),
        "moves": sorted_moves,
    }
