# portfolio-narrator

Generates a daily natural-language narrative of your portfolio's price
moves — "ASML is up 3.2% today, adding €340 to your position, following
reports of..." — by combining live prices, portfolio holdings, and recent
news, then handing pre-computed numbers to an LLM to write up.

## Architecture principle: the LLM never computes numbers

All arithmetic in this project lives in one place:
[`src/portfolio_narrator/calculations.py`](src/portfolio_narrator/calculations.py).
It is the single source of truth for every percentage, euro amount, and
total the app produces.

Every other module is downstream of it:

- [`prices.py`](src/portfolio_narrator/prices.py) fetches raw closing
  prices — never derives a change from them.
- [`news.py`](src/portfolio_narrator/news.py) fetches headlines — never
  infers a number from them.
- [`narrator.py`](src/portfolio_narrator/narrator.py) calls Claude to
  phrase the numbers it's handed — it never calculates or double-checks
  them.

This separation exists because LLMs are unreliable at arithmetic and can
silently hallucinate plausible-looking numbers. By making `calculations.py`
the only place numbers are ever produced, and treating every other module
(especially the LLM-facing `narrator.py`) as a pure consumer of those
numbers, the numeric output of the app stays deterministic and testable
independent of the LLM. If you're extending this project, new numeric
logic belongs in `calculations.py`, not sprinkled into the code that talks
to Claude.

## Project layout

```
portfolio-narrator/
├── portfolio.json           # your holdings (ticker + shares)
├── data/                    # local cache/db (gitignored)
├── output/                  # generated narratives (gitignored)
├── src/portfolio_narrator/
│   ├── config.py            # loads .env (API keys)
│   ├── portfolio.py         # loads portfolio.json
│   ├── calculations.py      # ALL numeric logic — the source of truth
│   ├── prices.py            # fetches prices via yfinance (stub)
│   ├── news.py              # fetches headlines via a news API (stub)
│   ├── narrator.py          # calls Claude to write the narrative (stub)
│   └── main.py              # orchestrates the pipeline (stub)
└── tests/
```

`prices.py`, `news.py`, `narrator.py`, and `main.py` are intentionally left
as stubs (`# TODO: implement`) to be built out one at a time.
`calculations.py` is fully implemented and tested, since it's the part
that has to be rock-solid.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency and
environment management.

1. Install dependencies and create the virtual environment:

   ```
   uv sync
   ```

2. Copy `.env.example` to `.env` and fill in your API keys:

   ```
   cp .env.example .env
   ```

   - `ANTHROPIC_API_KEY` — from the [Anthropic Console](https://console.anthropic.com/)
   - `NEWS_API_KEY` — from your news API provider

3. Edit `portfolio.json` with your own holdings.

4. Run the app (once `main.py` is implemented):

   ```
   uv run python -m portfolio_narrator.main
   ```

   Or, after `uv sync` installs the project's console script:

   ```
   uv run portfolio-narrator
   ```

## Running tests

```
uv run pytest
```

`tests/test_calculations.py` is fully implemented and covers positive,
negative, and zero-change scenarios. `tests/test_prices.py` and
`tests/test_narrator.py` are skipped stubs to fill in alongside their
corresponding modules.
