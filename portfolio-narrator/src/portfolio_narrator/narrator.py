"""Turns pre-computed portfolio numbers and news into a natural-language narrative.

Architecture principle: the LLM never computes numbers. Every percentage,
euro amount, and total consumed here must come from calculations.py
(via the daily report dict). This module's job is purely to phrase and
contextualize numbers it is handed, using news.py headlines for color —
never to derive or double-check the arithmetic itself.
"""

import json

import anthropic

from portfolio_narrator import config

MODEL = "claude-sonnet-4-6"

MAX_TOKENS = 800

# The system prompt sets the model's role and rules *before* it ever sees
# the actual data, and is sent as a separate field from the user message
# (see `system=` below) rather than being pasted into the same text. This
# keeps "how you must behave" cleanly separated from "here is today's
# data" — the model treats the system prompt as a standing instruction
# that applies no matter what shows up in the user message, rather than
# something it might reinterpret alongside the numbers. It's also the one
# place we spell out, in full, the "never compute numbers" rule this
# whole project depends on.
SYSTEM_PROMPT = """You are a financial writing assistant that turns pre-calculated portfolio data into a short evening-briefing narrative in Dutch.

CRITICAL RULE: you must NEVER calculate, recompute, re-derive, verify, round, or estimate any number yourself. Every percentage, euro amount, price, and total you use MUST be copied exactly, character-for-character, from the JSON data given to you in the user message. This rule applies even to arithmetic that looks trivial - adding two numbers together, checking whether a percentage "looks right", or restating a total in a different form. Treat every number in the data as a fixed, opaque fact you are not permitted to check, correct, or improve, even if you believe you have spotted an error. Never introduce a number that does not appear verbatim in the provided data.

Your only job is to write clear, natural Dutch prose that:
- References the given numbers exactly as provided, without altering them
- Uses the provided news headlines and summaries to explain WHY the biggest movers moved, when news is available for them
- Reads like a short evening briefing to a friend: plain everyday language, no financial jargon, no investment advice, no disclaimers

Write exactly 3 to 4 paragraphs."""


def write_narrative(daily_report: dict, news_by_ticker: dict) -> str:
    """Generate a natural-language daily portfolio summary in Dutch.

    Args:
      daily_report: the dict returned by calculations.build_daily_report —
        contains total_pct, total_euro, and the sorted per-holding moves.
        Every number in here is already final; this function only phrases
        them, it never recalculates anything.
      news_by_ticker: a dict mapping ticker -> list of {"headline",
        "summary"} dicts from news.get_news, used to add context for the
        biggest movers. Tickers with no news simply won't have an entry.

    Returns:
      A Dutch-language narrative string (a few paragraphs), or a Dutch
      fallback message starting with "Kon geen verslag genereren:" if the
      Anthropic API call fails for any reason (bad key, rate limit,
      network error) — this function must never raise, since a failed
      narrative should not crash the rest of the pipeline.
    """
    # We bundle the report and news into one plain dict and send it as
    # JSON text in the user message, clearly labeled as data. json.dumps
    # with indent=2 just keeps it human-readable if we ever print the
    # prompt while debugging.
    payload = {
        "daily_report": daily_report,
        "news_by_ticker": news_by_ticker,
    }
    user_message = (
        "Hier zijn de reeds berekende cijfers en het bijbehorende nieuws "
        "voor het dagelijkse portfolio-overzicht, als JSON. Gebruik deze "
        "gegevens exact zoals ze zijn - bereken niets opnieuw:\n\n"
        f"{json.dumps(payload, indent=2)}"
    )

    try:
        # The client reads the key from config, which loads it from .env
        # via python-dotenv — the key itself never appears in source code.
        client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        # A successful response's content is a list of content blocks
        # (normally just one, for a plain text reply); .text is the
        # actual generated string inside that block.
        return response.content[0].text

    except (anthropic.APIError, TypeError) as error:
        # anthropic.APIError is the base class for every error the SDK
        # raises once a request actually reaches the API — a rejected
        # (wrong) API key, rate limits, and connection/network failures
        # all land here. A *missing* or empty API key is different: the
        # SDK catches that before sending anything, while building the
        # request headers, and raises a plain TypeError instead — so we
        # catch that too. Either way we degrade gracefully instead of
        # crashing, since a missing narrative shouldn't take down the
        # rest of the pipeline.
        return f"Kon geen verslag genereren: {error}"
