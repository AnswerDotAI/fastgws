import json

from fastgws import cli


class _SchemaApi:
    def schema(self, path, resolve_refs=False): return {"path": path, "resolve_refs": resolve_refs}

    def resolve_endpoint(self, path):
        class _Endpoint:
            signature = "(page_size=None)"
            __doc__ = "endpoint docs"

            def __call__(self, *args, **kwargs): return {"args": list(args), "kwargs": kwargs}

        return _Endpoint()


def test_cli_services(capsys, monkeypatch):
    monkeypatch.setattr(cli, "REGISTRY", {"drive": {"description": "Drive"}})
    cli.main(["services"])
    assert "drive" in capsys.readouterr().out


def test_cli_schema(capsys, monkeypatch):
    monkeypatch.setattr(cli, "FastGWS", lambda: _SchemaApi())
    cli.main(["schema", "drive.files.create", "--resolve-refs"])
    data = json.loads(capsys.readouterr().out)
    assert data["resolve_refs"] is True


def test_cli_endpoint_help(capsys, monkeypatch):
    monkeypatch.setattr(cli, "FastGWS", lambda: _SchemaApi())
    cli.main(["drive.files.list", "--help"])
    out = capsys.readouterr().out
    assert "drive.files.list" in out
    assert "endpoint docs" in out
