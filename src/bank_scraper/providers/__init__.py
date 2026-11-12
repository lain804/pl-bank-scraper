import importlib
import inspect
import pkgutil

from bank_scraper.providers.base import RateProvider

for module in pkgutil.iter_modules(__path__):
    if module.name != "base":
        importlib.import_module(f"{__name__}.{module.name}")

PROVIDERS = []

for cls in RateProvider.__subclasses__():
    # make sure the provider is actually implemented and not just inherits the base RateProvider class
    if not inspect.isabstract(cls):
        PROVIDERS.append(cls)