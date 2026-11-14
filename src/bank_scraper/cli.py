import sys
import json

from loguru import logger

from bank_scraper.providers import *

def main():
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    for provider in PROVIDERS:
        print(
            json.dumps(
                provider.get_rates(),
                indent=4,
                default=str
            )
        )

if __name__ == "__main__":
    main()