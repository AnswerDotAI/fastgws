class FastGWSError(Exception): ...


class DiscoveryError(FastGWSError): ...


class ValidationError(FastGWSError): ...


class APIError(FastGWSError):
    def __init__(self, message, *, status_code=None, method=None, url=None, body=None):
        super().__init__(message)
        self.status_code = status_code
        self.method = method
        self.url = url
        self.body = body
