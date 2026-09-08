"""Tests for narrator.py.

This test makes a real call to the Anthropic API with a small, realistic
fake report and fake news dict. We don't assert on exact wording since
LLM output varies from run to run — only that a real narrative came back,
rather than the "Kon geen verslag genereren" fallback string.
"""

from portfolio_narrator.narrator import write_narrative

FAKE_REPORT = {
    "total_pct": 1.85,
    "total_euro": 245.30,
    "moves": [
        {
            "ticker": "ASML.AS",
            "shares": 10,
            "today_close": 680.50,
            "prev_close": 650.20,
            "pct_change": 4.66,
            "euro_change": 303.0,
            "value_today": 6805.0,
        },
        {
            "ticker": "AAPL",
            "shares": 5,
            "today_close": 220.10,
            "prev_close": 231.70,
            "pct_change": -5.01,
            "euro_change": -58.0,
            "value_today": 1100.50,
        },
    ],
}

FAKE_NEWS = {
    "ASML.AS": [
        {
            "headline": "ASML beats expectations on strong AI chip demand",
            "summary": (
                "ASML reported quarterly bookings well above analyst "
                "estimates, driven by demand for advanced lithography "
                "systems used in AI chip production."
            ),
        }
    ],
}


def test_write_narrative():
    result = write_narrative(FAKE_REPORT, FAKE_NEWS)

    assert isinstance(result, str)
    assert len(result) > 50
    assert not result.startswith("Kon geen verslag genereren")
