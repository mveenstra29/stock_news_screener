# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This project uses [uv](https://docs.astral.sh/uv/) for dependency and environment management.

```
uv sync                                    # install dependencies / create venv
uv run pytest                              # run all tests
uv run pytest tests/test_calculations.py   # run a single test file
uv run pytest tests/test_calculations.py::test_name  # run a single test
uv run python -m portfolio_narrator.main   # run the app directly
uv run portfolio-narrator                  # run via installed console script
```

Setup: copy `.env.example` to `.env` and fill in `ANTHROPIC_API_KEY` and `NEWS_API_KEY`. Holdings live in `portfolio.json` (ticker + shares).

## Architecture principle: the LLM never computes numbers

All arithmetic lives in exactly one place: [`src/portfolio_narrator/calculations.py`](src/portfolio_narrator/calculations.py). It is the single source of truth for every percentage, euro amount, and total the app produces. Every other module is a downstream consumer:

- [`prices.py`](src/portfolio_narrator/prices.py) fetches raw closing prices via yfinance — never derives a change from them.
- [`news.py`](src/portfolio_narrator/news.py) fetches headlines via a news API — never infers a number from them.
- [`narrator.py`](src/portfolio_narrator/narrator.py) calls Claude to phrase the numbers it's handed (embedding `calculations.py` output verbatim into the prompt) — it never calculates or double-checks them.
- [`main.py`](src/portfolio_narrator/main.py) orchestrates the pipeline: `portfolio.load_portfolio` → `prices.get_price_data` (per holding) → `calculations.calculate_move` + `calculations.build_daily_report` → `news.get_news` (for top movers) → `narrator.write_narrative`.

This separation exists because LLMs are unreliable at arithmetic and can silently hallucinate plausible-looking numbers. New numeric logic belongs in `calculations.py`, never sprinkled into the code that talks to Claude, and existing modules' docstrings enforce this boundary — preserve it when extending them.

## Project state

`prices.py`, `news.py`, `narrator.py`, and `main.py` are stubs (`raise NotImplementedError`) meant to be built out one at a time, in that dependency order (each stub's docstring specifies its exact expected inputs/outputs and the library to use). `calculations.py` is fully implemented and tested since it has to be rock-solid; `tests/test_calculations.py` covers positive, negative, and zero-change scenarios. `tests/test_prices.py` and `tests/test_narrator.py` are skipped placeholders to fill in alongside their corresponding modules.

`data/` and `output/` are gitignored working directories for local cache and generated narratives, respectively.

## Workflow

I am learning to code, so after every session explain very detailed what is done