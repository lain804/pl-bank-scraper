from decimal import Decimal
from typing import TypedDict

class ExchangeRate(TypedDict):
    buy: Decimal
    sell: Decimal

Rates = dict[str, ExchangeRate]