from decimal import Decimal
from datetime import date
import json
from typing import Any

import quickjs
from curl_cffi import requests
from bs4 import BeautifulSoup
from bs4.element import PageElement
from loguru import logger

from bank_scraper.providers.base import RateProvider
from bank_scraper.models import (
    ExchangeRate,
    Rates
)
from bank_scraper.constants import *

logger = logger.bind(provider="PEKAO")

class PekaoProvider(RateProvider):
    @staticmethod
    def get_rates():
        url = "https://www.pekao.com.pl/kursy-walut/lista-walut"

        try:
            r = requests.get(
                url=url
            )
            r.raise_for_status()
            logger.debug(f"{r.status_code} {r.response_size} {r.url}")
        except Exception as e:
            logger.exception(f"Failed to get rates XML {e}")
            exit(EXIT_FAILURE)

        soup = BeautifulSoup(
            markup=r.text,
            features="lxml"
        )

        currency_rates_script_element: PageElement = None
        for script in soup.find_all("script",type="text/javascript"):
            if "currenciesJson" in script.text:
                currency_rates_script_element = script
                break

        if currency_rates_script_element is None:
            logger.error("Failed to locate script with currenciesJson")
            exit(EXIT_FAILURE)

        ctx = quickjs.Context()
        ctx.set_memory_limit(16*MB)
        ctx.set_max_stack_size(1*MiB)
        ctx.set_time_limit(500 * ms)

        ctx.eval(currency_rates_script_element.text)

        currencies: quickjs.Object = ctx.eval("currenciesJson")
        currencies_json_serialized = currencies.json()
        currencies_json_deserialized:dict = json.loads(currencies_json_serialized)

        rates_deserialized = currencies_json_deserialized.get("exchangeRatesDTO",{}).get("rates")
        if rates_deserialized is None:
            logger.error("Failed to find currency exchange rates")
            exit(EXIT_FAILURE)

        rates: Rates = {}

        for currency in rates_deserialized:
            rate = ExchangeRate()
            rate["buy"] = Decimal(str(currency["sellOffer"]))
            rate["sell"] = Decimal(str(currency["purchaseOffer"]))
            rates[currency["currencyISOCode"]] = rate

        return rates