"""Orchestrates the full pipeline: portfolio -> prices -> calculations -> news -> narrative."""


def run(portfolio_path: str = "portfolio.json") -> str:
    """Run the end-to-end daily portfolio narration pipeline.

    Should:
      1. Load holdings via portfolio.load_portfolio(portfolio_path).
      2. For each holding, fetch prices via prices.get_price_data.
      3. Compute each move via calculations.calculate_move, then aggregate
         with calculations.build_daily_report — all arithmetic happens here,
         nowhere else.
      4. Fetch news per ticker via news.get_news (e.g. for top movers).
      5. Generate the narrative via narrator.write_narrative.
      6. Return (and/or write to output/) the final narrative text.
    """
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    run()
