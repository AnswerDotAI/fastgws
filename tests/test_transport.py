from fastgws.transport import RequestSpec, RequestsTransport

from tests.helpers import FakeCredentials, FakeResponse, FakeSession


def test_transport_wraps_json_and_applies_credentials():
    session = FakeSession([FakeResponse(payload={"nextPageToken": "x", "files": [{"id": "1"}]}, headers={"content-type": "application/json"})])
    transport = RequestsTransport(session=session)
    creds = FakeCredentials()
    result = transport.execute(RequestSpec("GET", "https://example.com"), credentials=creds)
    assert result.nextPageToken == "x"
    assert result.files[0].id == "1"
    assert creds.calls == [("GET", "https://example.com")]


def test_transport_downloads_bytes(tmp_download):
    session = FakeSession([FakeResponse(content=b"abc", headers={"content-type": "application/octet-stream"})])
    transport = RequestsTransport(session=session)
    path = transport.execute(RequestSpec("GET", "https://example.com", download=str(tmp_download)))
    assert path.read_bytes() == b"abc"
