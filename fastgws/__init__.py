"""Modules:

- `fastgws.addons`: Google Workspace Add-ons deployment and test-installation lifecycle.
- `fastgws.admin`: Workspace user and license administration through Google APIs.
- `fastgws.skill`: Use fastgws to read and work with Google Workspace and Google APIs from Python. This skill exposes the base `GWSApi` client, OAuth credential loading, and generated Google API operations, and Workspace user administration. Use it when the task needs access to Gmail, Calendar, Drive, Docs, Sheets, Places, or another Google API published through Google's discovery documents."""

from .auth import *
from .core import *
from .admin import *
from .addons import *
from functools import cache

import httpx

__version__ = "0.2.9"

@cache
def apis(): return httpx.get('https://discovery.googleapis.com/discovery/v1/apis').json()['items']

def services(): return {a['name'] for a in apis()}

def __getattr__(name):
    service = name.lower()
    if service in services():
        cls = type(name, (GWSApi,), {'service': service})
        globals()[name] = cls
        return cls
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
