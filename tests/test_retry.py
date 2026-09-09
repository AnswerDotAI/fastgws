import httpx2

from fasttransport.errors import APIError
import fastgws.core as core


def quota_error(unit='1/min/{project}/{user}', start='1700000000', headers=None):
    detail = {'@type':'type.googleapis.com/google.rpc.ErrorInfo', 'reason':'RATE_LIMIT_EXCEEDED',
              'metadata':{'quota_unit':unit, 'window_start_time':start}}
    raw = {'error':{'details':[detail]}}
    return APIError('Quota exceeded', status_code=403, raw=raw, response=httpx2.Response(403, headers=headers))


def test_retry_hints_and_limits():
    def delay(err, **kwargs): return core._retry_delay(err, 0, 0, 64, now=1700000030, **kwargs)

    err = quota_error()
    assert core._retryable(err)
    assert delay(err) == 31
    assert delay(quota_error('1/100s/{project}')) == 71
    assert delay(quota_error('1/d/{project}')) is None
    assert delay(quota_error('1/d/{project}', start='1699913631')) == 2
    assert delay(err, max_wait=30) is None
    assert delay(err, max_wait=31) == 31

    for hint in ['12', 'Tue, 14 Nov 2023 22:14:00 GMT']:
        assert delay(quota_error(headers={'Retry-After':hint})) == (12 if hint == '12' else 10)
    assert delay(quota_error(headers={'Retry-After':'301'})) is None
    assert delay(quota_error(headers={'Retry-After':'0'}), max_wait=0) == 0
    assert delay(quota_error(headers={'Retry-After':'Tue, 14 Nov 2023 22:13:00 GMT'})) == 0

    retry = {'@type':'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay':'2.125s'}
    err.raw['error']['details'].append(retry)
    assert delay(err) == 2.125
    err.response = httpx2.Response(403, headers={'Retry-After':'5'})
    assert delay(err) == 5
    err.response = None
    retry['retryDelay'] = '301s'
    assert delay(err) is None
    for value in ['invalid', '-1s', 'NaNs', 'Infinitys', None]:
        retry['retryDelay'] = value
        assert delay(err) == 31

    for value in ['nan', 'inf', '-inf', 'invalid']:
        assert delay(quota_error(headers={'Retry-After':value})) == 31
        assert delay(quota_error(start=value)) == 0
    assert delay(quota_error(headers={'Retry-After':'-1'})) == 31
    for unit in ['1/0s/{project}', '1/week/{project}', 'invalid', None]:
        assert delay(quota_error(unit)) == 0
    err.raw['error']['details'].insert(0, {'@type':'type.googleapis.com/google.rpc.ErrorInfo', 'metadata':{}})
    assert delay(err) == 31
    assert core._retry_delay(APIError('Unavailable', status_code=503), 2, 1, 64, max_wait=3) is None


def test_google_error_locations():
    for raw in [None, 'not JSON', {'error':'not an object'}, {'error':{'details':None}},
                {'unrelated':{'reason':'rateLimitExceeded'}}, {'error':{'errors':[{'reason':None}]}}]:
        err = APIError('Forbidden', status_code=403, raw=raw)
        assert not core._retryable(err)
        assert core._retry_delay(err, 0, 0, 64) == 0
    err = APIError('Forbidden', status_code=403, raw={'error':{'errors':[{'reason':'userRateLimitExceeded'}]}})
    assert core._retryable(err)
