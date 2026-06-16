from .auth import *
from .core import *
from functools import cache

import httpx

__version__ = "0.2.4"

@cache
def apis():
    return httpx.get('https://discovery.googleapis.com/discovery/v1/apis').json()['items']

def services():
    return {a['name'] for a in apis()}

def __getattr__(name):
    service = name.lower()
    if service in services():
        cls = type(name, (GWSApi,), {'service': service})
        globals()[name] = cls
        return cls
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")