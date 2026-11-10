from abc import ABC, abstractmethod
from bank_scraper.models import Rates

class RateProvider(ABC):
    @abstractmethod
    def get_rates(self) -> Rates:
        """
        Return PLN buy/sell prices for one unit of a given currency
        """