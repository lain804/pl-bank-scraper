from loguru import logger
import sys
from bank_scraper.providers.pekao import PekaoProvider
import json

def main():
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    provider = PekaoProvider()

    print(
        json.dumps(
            provider.get_rates(),
            indent=4,
            default=str
        )
    )

if __name__ == "__main__":
    main()