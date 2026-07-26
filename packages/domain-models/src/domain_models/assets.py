"""Multi-asset classification shared by services and agents."""

from enum import Enum


class AssetClass(str, Enum):
    CRYPTO = "crypto"
    EQUITY = "equity"
    FOREX = "forex"
    FUTURES = "futures"
    ETF = "etf"
