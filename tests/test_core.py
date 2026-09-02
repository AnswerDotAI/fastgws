import asyncio

from fastgws import GWSApi


def test_from_discovery_url():
    url = 'https://www.googleapis.com/discovery/v1/apis/drive/v3/rest'
    api = asyncio.run(GWSApi.from_discovery_url(url))
    assert (api.service, api.version) == ('drive', 'v3')
    assert api.files.list.verb == 'GET'
