from fastgws.core import FastGWS


class _PagingTransport:
    def __init__(self): self.calls = []

    def execute(self, spec, *, credentials=None):
        self.calls.append(spec)
        token = dict(spec.query).get("pageToken")
        if token == "next-1": return {"files": [{"id": "2"}]}
        return {"nextPageToken": "next-1", "files": [{"id": "1"}]}


def test_pages_and_items_follow_next_page_token():
    api = FastGWS(transport=_PagingTransport(), credentials=object())
    pages = list(api.drive.files.list.pages())
    assert len(pages) == 2
    items = list(api.drive.files.list.items())
    assert [o["id"] for o in items] == ["1", "2"]
