"""Unit tests for the calculations module — the project's arithmetic source of truth."""

import pytest

from portfolio_narrator.calculations import build_daily_report, calculate_move


def test_calculate_move_positive_change():
    result = calculate_move("AAPL", shares=5, today_close=110.0, prev_close=100.0)

    assert result["ticker"] == "AAPL"
    assert result["shares"] == 5
    assert result["pct_change"] == 10.0
    assert result["euro_change"] == 50.0
    assert result["today_close"] == 110.0
    assert result["prev_close"] == 100.0
    assert result["value_today"] == 550.0


def test_calculate_move_negative_change():
    result = calculate_move("ASML.AS", shares=10, today_close=90.0, prev_close=100.0)

    assert result["pct_change"] == -10.0
    assert result["euro_change"] == -100.0
    assert result["today_close"] == 90.0
    assert result["prev_close"] == 100.0
    assert result["value_today"] == 900.0


def test_calculate_move_zero_change():
    result = calculate_move("AAPL", shares=5, today_close=100.0, prev_close=100.0)

    assert result["pct_change"] == 0.0
    assert result["euro_change"] == 0.0
    assert result["today_close"] == 100.0
    assert result["prev_close"] == 100.0
    assert result["value_today"] == 500.0


def test_calculate_move_rounds_to_two_decimals():
    result = calculate_move("AAPL", shares=3, today_close=100.333, prev_close=99.111)

    assert result["pct_change"] == round((100.333 - 99.111) / 99.111 * 100, 2)
    assert result["euro_change"] == round((100.333 - 99.111) * 3, 2)
    assert result["today_close"] == 100.33
    assert result["prev_close"] == 99.11
    assert result["value_today"] == round(100.333 * 3, 2)


def test_build_daily_report_totals_and_sorting():
    moves = [
        calculate_move("AAPL", shares=5, today_close=105.0, prev_close=100.0),
        calculate_move("ASML.AS", shares=10, today_close=80.0, prev_close=100.0),
        calculate_move("MSFT", shares=2, today_close=100.0, prev_close=100.0),
    ]

    report = build_daily_report(moves)

    assert report["total_euro"] == 25.0 + (-200.0) + 0.0
    assert [move["ticker"] for move in report["moves"]] == ["ASML.AS", "AAPL", "MSFT"]


def test_build_daily_report_empty_raises():
    with pytest.raises(ValueError):
        build_daily_report([])
