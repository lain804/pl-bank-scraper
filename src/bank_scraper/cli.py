from loguru import logger
import sys
from bank_scraper.providers import PROVIDERS
import json

def main():
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    for provider in PROVIDERS:
        print(provider.__name__)
        print(
            json.dumps(
                provider.get_rates(),
                indent=4,
                default=str
            )
        )

if __name__ == "__main__":
    main()