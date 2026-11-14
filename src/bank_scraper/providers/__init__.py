#import importlib
#import pkgutil

import inspect

from bank_scraper.providers.base import RateProvider
from .pekao import PekaoProvider
from .erste import ErsteProvider

# this is cool but we need to explicitly import the providers for static intellisense
#for module in pkgutil.iter_modules(__path__):
#    if module.name != "base":
#        importlib.import_module(f"{__name__}.{module.name}")

PROVIDERS:list[type[RateProvider]] = []

# subclasses returns a list of immediate subclasses that were imported into this module
for cls in RateProvider.__subclasses__():
    # make sure the provider is actually implemented and doesnt just inherit the base RateProvider class
    if not inspect.isabstract(cls):
        PROVIDERS.append(cls)

__all__ = [
    "RateProvider",
    "PROVIDERS",
    "PekaoProvider",
    "ErsteProvider"
]