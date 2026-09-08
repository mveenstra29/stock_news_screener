"""Loads configuration and secrets from the .env file."""

import os

from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
