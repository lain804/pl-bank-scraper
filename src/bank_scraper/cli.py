import sys
import json

from loguru import logger

from bank_scraper.providers import PekaoProvider

def main():
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    print(
        json.dumps(
            PekaoProvider.get_rates(),
            indent=4,
            default=str
        )
    )

if __name__ == "__main__":
    main()