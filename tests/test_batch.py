import email.errors, email.parser, email.policy, gzip, h11, httpx2, pytest

from fastcore.utils import noop
from fasttransport.errors import APIError
from fastspec.spec import OpSpec

from fastgws.core import GWSOpFunc, GWSTransport
import fastgws.core as core


def test_google_batch_wire_format_and_results():
    spec = OpSpec(group='things', name='get', path='v1/things/{id}', verb='GET', route_params=['id'], query_params=['fields'])
    op = GWSOpFunc(spec, GWSTransport(), 'https://api.example/', noop)
    content,requests = op._batch_content([dict(id='one', fields='id,name'), dict(id='missing')], 'req')
    assert b'GET /v1/things/one?fields=id%2Cname HTTP/1.1' in content

    post_spec = OpSpec(group='things', name='create', path='things', verb='POST', body_params=['text'])
    post = GWSOpFunc(post_spec, GWSTransport(), 'https://api.example/', noop)
    content,post_requests = post._batch_content([dict(text='café\r\nnext line')], 'req')
    msg = email.parser.BytesParser(policy=email.policy.default).parsebytes(b'Content-Type: multipart/mixed; boundary=req\r\n\r\n' + content)
    assert next(msg.iter_parts()).get_payload(decode=True) == core.request_bytes(post_requests[0])

    lines = [b'--res', b'Content-Type: application/http', b'', b'HTTP/1.1 200 OK', b'Content-Type: application/json', b'', b'{"id":"one"}',
        b'--res', b'Content-Type: application/http', b'', b'HTTP/1.1 403 Forbidden', b'Content-Type: application/json', b'',
        b'{"error":{"message":"slow down","errors":[{"reason":"userRateLimitExceeded"}]}}', b'--res--', b'']
    body = b'\r\n'.join(lines)
    response = httpx2.Response(200, headers={'Content-Type':'multipart/mixed; boundary=res'}, content=body)
    result = op._batch_results(response, requests)
    assert result[0].id == 'one'
    assert isinstance(result[1], APIError) and result[1].retryable

    payload = b'one\r\ntwo\n\xff\x00\r\n'
    part = b'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\n\r\n' + payload
    body = b'--res\r\nContent-Type: application/http\r\n\r\n' + part + b'\r\n--res--\r\n'
    response = httpx2.Response(200, headers={'Content-Type':'multipart/mixed; boundary="res"'}, content=body)
    assert op._batch_results(response, requests[:1]) == [payload]
    for ctype,content in [('text/plain', body), ('multipart/mixed; boundary=res', body.removesuffix(b'--res--\r\n')),
                          ('multipart/mixed; boundary=res', body.replace(b'application/http', b'text/plain'))]:
        response = httpx2.Response(200, headers={'Content-Type':ctype}, content=content)
        with pytest.raises((ValueError, email.errors.MessageDefect)): op._batch_results(response, requests[:1])


def test_http_message_framing():
    payload = b'one\r\ntwo\n\xff\x00'
    request = httpx2.Request('POST', 'https://api.example/things?q=one', content=payload)
    wire = core.request_bytes(request)
    head,body = wire.split(b'\r\n\r\n', 1)
    assert head.startswith(b'POST /things?q=one HTTP/1.1\r\n')
    assert body == payload

    headers = b'X-Value: one\r\nX-Value: two\r\nContent-Type: application/octet-stream\r\n'
    response = core.response_from_bytes(b'HTTP/1.1 200 OK\r\n' + headers + b'\r\n' + payload, request)
    assert response.content == payload
    assert response.headers.get_list('x-value') == ['one', 'two']
    assert response.request is request

    chunked = b'HTTP/1.1 100 Continue\r\n\r\nHTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n4\r\nbody\r\n0\r\n\r\n'
    assert core.response_from_bytes(chunked, request).content == b'body'
    compressed = gzip.compress(payload)
    wire = b'HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Length: %d\r\n\r\n' % len(compressed) + compressed
    assert core.response_from_bytes(wire, request).content == payload
    assert core.response_from_bytes(b'HTTP/1.1 204 No Content\r\n\r\n', request).content == b''
    head_request = httpx2.Request('HEAD', request.url)
    assert core.response_from_bytes(b'HTTP/1.1 200 OK\r\nContent-Length: 100\r\n\r\n', head_request).content == b''

    for wire in [b'', b'not HTTP\r\n\r\n', b'HTTP/1.1 200 OK\r\nbroken header\r\n\r\n',
                 b'HTTP/1.1 200 OK\r\nContent-Length: 4\r\n\r\nabc',
                 b'HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\nextra',
                 b'HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\nz\r\n',
                 b'HTTP/1.1 101 Switching Protocols\r\n\r\n']:
        with pytest.raises(h11.RemoteProtocolError): core.response_from_bytes(wire, request)


def test_google_rate_limit_error_stays_retryable():
    spec = OpSpec(group='things', name='get', path='v1/things/{id}', verb='GET', route_params=['id'])
    op = GWSOpFunc(spec, GWSTransport(), 'https://api.example/', noop)
    request = httpx2.Request('GET', 'https://api.example/v1/things/one')
    response = httpx2.Response(403, request=request,
        json={'error':{'message':'slow down', 'errors':[{'reason':'rateLimitExceeded'}]}})
    with pytest.raises(httpx2.HTTPStatusError) as http_error: response.raise_for_status()
    with pytest.raises(APIError) as api_error: op._raise_with_context(http_error.value)
    assert api_error.value.retryable
    assert api_error.value.endpoint == 'GET /v1/things/one'
