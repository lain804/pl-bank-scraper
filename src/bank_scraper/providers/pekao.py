from decimal import Decimal

from curl_cffi import requests

from bank_scraper.providers.base import RateProvider
from bs4 import BeautifulSoup
from datetime import date
from loguru import logger
from bank_scraper.models import (
    ExchangeRate, 
    Rates
)

logger = logger.bind(provider="PEKAO")

class PekaoProvider(RateProvider):
    def get_rates(self):
        url = "https://www.pekao.com.pl/.rest/currencies/file"
        params = {
            "type": "XML",
            "source": "PEKAO",
            "date": date.today().isoformat(),
            "table": 1
        }

        try:
            r = requests.get(
                url=url,
                params=params
            )
            r.raise_for_status()
            logger.debug(f"{r.status_code} {r.response_size} {r.url}")
        except Exception as e:
            logger.exception(f"Failed to get rates XML {e}")
            exit(1)

        soup = BeautifulSoup(
            markup=r.text,
            features="xml"
        )

        rates: Rates = {}

        for position in soup.find_all("pozycja"):
            rate = ExchangeRate()
            rate["buy"] = Decimal(position.find("kupno").text)
            rate["sell"] = Decimal(position.find("sprzedaz").text)
            currency_name = position.find("iso").text
            rates[currency_name] = rate

        return rates            