import httpx, httpx2, pytest

from fastcore.utils import noop
from fasttransport.errors import APIError
from fastspec.spec import OpSpec

from fastgws.core import GWSOpFunc, GWSTransport


def test_google_batch_wire_format_and_results():
    spec = OpSpec(group='things', name='get', path='v1/things/{id}', verb='GET', route_params=['id'], query_params=['fields'])
    op = GWSOpFunc(spec, GWSTransport(), 'https://api.example/', noop)
    content,requests = op._batch_content([dict(id='one', fields='id,name'), dict(id='missing')], 'req')
    assert b'GET /v1/things/one?fields=id%2Cname HTTP/1.1' in content

    lines = [b'--res', b'Content-Type: application/http', b'', b'HTTP/1.1 200 OK', b'Content-Type: application/json', b'', b'{"id":"one"}',
        b'--res', b'Content-Type: application/http', b'', b'HTTP/1.1 403 Forbidden', b'Content-Type: application/json', b'',
        b'{"error":{"message":"slow down","errors":[{"reason":"userRateLimitExceeded"}]}}', b'--res--', b'']
    body = b'\r\n'.join(lines)
    response = httpx.Response(200, headers={'Content-Type':'multipart/mixed; boundary=res'}, content=body)
    result = op._batch_results(response, requests)
    assert result[0].id == 'one'
    assert isinstance(result[1], APIError) and result[1].retryable


def test_google_rate_limit_error_stays_retryable():
    spec = OpSpec(group='things', name='get', path='v1/things/{id}', verb='GET', route_params=['id'])
    op = GWSOpFunc(spec, GWSTransport(), 'https://api.example/', noop)
    request = httpx2.Request('GET', 'https://api.example/v1/things/one')
    response = httpx2.Response(403, request=request,
        json={'error':{'message':'slow down', 'errors':[{'reason':'rateLimitExceeded'}]}})
    with pytest.raises(httpx2.HTTPStatusError) as http_error: response.raise_for_status()
    with pytest.raises(APIError) as api_error: op._raise_with_context(http_error.value, endpoint='', route=None, query=None, body=None)
    assert api_error.value.retryable
