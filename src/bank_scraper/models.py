from decimal import Decimal
from typing import TypedDict

class ExchangeRate(TypedDict):
    buy: Decimal # Customer buys at this rate
    sell: Decimal # Customer sells at this rate

Rates = dict[str, ExchangeRate]