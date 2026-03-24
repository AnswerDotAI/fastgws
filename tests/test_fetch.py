import pytest

from fastgws.build.fetch import fetch_discovery_doc, validate_identifier
from fastgws.errors import DiscoveryError, ValidationError


class _Response:
    def __init__(self, ok, status_code, payload):
        self.ok = ok
        self.status_code = status_code
        self._payload = payload

    def json(self): return self._payload


class _Client:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def get(self, url, params=None, timeout=30):
        self.calls.append((url, params, timeout))
        return self.responses.pop(0)


def test_fetch_discovery_doc_falls_back_and_caches(tmp_path):
    client = _Client([_Response(False, 404, {}), _Response(True, 200, {"name": "keep"})])
    doc = fetch_discovery_doc("keep", "v1", client=client, cache_dir=tmp_path)
    assert doc["name"] == "keep"
    cached = fetch_discovery_doc("keep", "v1", client=_Client([]), cache_dir=tmp_path)
    assert cached["name"] == "keep"
    assert len(client.calls) == 2


def test_validate_identifier_rejects_bad_names():
    with pytest.raises(ValidationError, match="invalid service"): validate_identifier("../drive", "service")


def test_fetch_discovery_doc_raises_on_failure():
    client = _Client([_Response(False, 404, {}), _Response(False, 404, {})])
    with pytest.raises(DiscoveryError, match="drive/v3"): fetch_discovery_doc("drive", "v3", client=client)
