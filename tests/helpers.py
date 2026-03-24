class FakeCredentials:
    def __init__(self): self.calls = []

    def before_request(self, request, method, url, headers):
        self.calls.append((method, url))
        headers["Authorization"] = "Bearer test-token"


class FakeTransport:
    def __init__(self, result=None):
        self.calls = []
        self.result = result if result is not None else {"ok": True}

    def execute(self, spec, *, credentials=None):
        self.calls.append((spec, credentials))
        return self.result


class FakeResponse:
    def __init__(self, *, ok=True, status_code=200, payload=None, content=b"", headers=None, text=""):
        self.ok = ok
        self.status_code = status_code
        self._payload = payload
        self.content = content
        self.headers = headers or {}
        self.text = text

    def json(self): return self._payload


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        return self.responses.pop(0)
