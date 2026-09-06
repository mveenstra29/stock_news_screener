"""Turns pre-computed portfolio numbers and news into a natural-language narrative.

Architecture principle: the LLM never computes numbers. Every percentage,
euro amount, and total consumed here must come from calculations.py
(via the daily report dict). This module's job is purely to phrase and
contextualize numbers it is handed, using news.py headlines for color —
never to derive or double-check the arithmetic itself.
"""

MODEL = "claude-sonnet-4-6"


def write_narrative(daily_report: dict, news_by_ticker: dict) -> str:
    """Generate a natural-language daily portfolio summary.

    Args:
      daily_report: the dict returned by calculations.build_daily_report —
        contains total_pct, total_euro, and the sorted per-holding moves.
      news_by_ticker: a dict mapping ticker -> list of news items from
        news.get_news, used to add context for the biggest movers.

    Should build a prompt that embeds the pre-computed numbers from
    daily_report verbatim (never re-derived), call the Anthropic client
    (model=MODEL) via client.messages.create, and return the resulting
    text narrative.
    """
    # TODO: implement
    raise NotImplementedError
