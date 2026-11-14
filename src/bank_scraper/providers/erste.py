from curl_cffi import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from bank_scraper.models import (
    Rates, 
    ExchangeRate
)
from bank_scraper.providers.base import RateProvider

class ErsteProvider(RateProvider):
    @staticmethod
    def get_rates():
        response = requests.get('https://www.erste.pl/przydatne-informacje/kursy-walut')
        response.raise_for_status()

        soup = BeautifulSoup(
            markup=response.text,
            features="lxml"
        )

        currency_element_children = soup.find_all(
            "td",
            class_="exchangeRates__flag"
        )

        rates: Rates = {}

        for child in currency_element_children:
            currency = child.parent
            iso_currency = currency.find("button").get("data-symbol-id").upper()
            if rates.get(iso_currency) != None:
                continue

            bank_buy_price = Decimal(currency.find(
                "td",
                class_="exchangeRates__buy"
            ).text)

            bank_sell_price = Decimal(currency.find(
                "td",
                class_="exchangeRates__sell"
            ).text)

            rate = ExchangeRate()
            rate["buy"] = bank_sell_price
            rate["sell"] = bank_buy_price

            rates[iso_currency] = rate

        return rates