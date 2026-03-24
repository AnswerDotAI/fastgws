import json

import pytest

from fastgws import cli
from fastgws.core import FastGWS
from fastgws.errors import ValidationError

from tests.helpers import FakeCredentials, FakeTransport


def test_explicit_credentials_are_used():
    creds = FakeCredentials()
    transport = FakeTransport({"files": []})
    api = FastGWS(credentials=creds, transport=transport)
    api.drive.files.list()
    assert transport.calls[0][1] is creds


def test_adc_is_used_when_credentials_missing(monkeypatch):
    sentinel = object()
    monkeypatch.setattr("fastgws.core.default_credentials", lambda scopes=None: sentinel)
    transport = FakeTransport({"files": []})
    api = FastGWS(credentials=None, transport=transport)
    api.drive.files.list()
    assert transport.calls[0][1] is sentinel


class _FakeOAuthCreds:
    def __init__(self, payload=None): self.payload = payload or dict(type="authorized_user", refresh_token="rtok")

    def to_json(self): return json.dumps(self.payload)


class _FakeFlow:
    def __init__(self, creds): self.creds = creds

    def run_local_server(self, port=0): return self.creds


def test_auth_login_saves_authorized_user_credentials(tmp_path, monkeypatch, capsys):
    config_dir = tmp_path / "cfg"
    secret_path = tmp_path / "client_secret.json"
    secret_path.write_text(json.dumps({"installed": dict(client_id="id", client_secret="secret", project_id="proj")}))
    flow = _FakeFlow(_FakeOAuthCreds())
    monkeypatch.setenv("FASTGWS_CONFIG_DIR", str(config_dir))
    monkeypatch.setattr("fastgws.auth.InstalledAppFlow.from_client_secrets_file", lambda path, scopes: flow)

    code = cli.main(["auth", "login", "--client-secret", str(secret_path), "--scopes", "scope1,scope2"])
    assert code == 0
    saved = json.loads((config_dir / "credentials.json").read_text())
    assert saved["type"] == "authorized_user"
    assert saved["refresh_token"] == "rtok"
    assert (config_dir / "client_secret.json").exists()
    out = json.loads(capsys.readouterr().out)
    assert out["credentials_file"].endswith("credentials.json")
    assert out["scopes"] == ["scope1", "scope2"]


def test_saved_authorized_user_credentials_are_preferred(tmp_path, monkeypatch):
    config_dir = tmp_path / "cfg"
    config_dir.mkdir()
    creds_path = config_dir / "credentials.json"
    creds_path.write_text(json.dumps({"type": "authorized_user"}))
    sentinel = object()
    monkeypatch.setenv("FASTGWS_CONFIG_DIR", str(config_dir))
    monkeypatch.setattr("fastgws.auth.load_authorized_user", lambda path, scopes=None: sentinel)
    monkeypatch.setattr("fastgws.auth.google_auth_default", lambda scopes=None: (_ for _ in ()).throw(AssertionError("ADC should not be used")))
    transport = FakeTransport({"files": []})

    api = FastGWS(credentials=None, transport=transport)
    api.drive.files.list()
    assert transport.calls[0][1] is sentinel


def test_saved_authorized_user_credentials_keep_their_original_scopes(tmp_path, monkeypatch):
    config_dir = tmp_path / "cfg"
    config_dir.mkdir()
    (config_dir / "credentials.json").write_text(json.dumps({"type": "authorized_user"}))
    calls = []

    def _load(path, scopes=None):
        calls.append(scopes)
        return object()

    monkeypatch.setenv("FASTGWS_CONFIG_DIR", str(config_dir))
    monkeypatch.setattr("fastgws.auth.load_authorized_user", _load)
    monkeypatch.setattr("fastgws.auth.google_auth_default", lambda scopes=None: (_ for _ in ()).throw(AssertionError("ADC should not be used")))
    transport = FakeTransport({"files": []})

    FastGWS(credentials=None, transport=transport).drive.files.list()
    assert calls == [None]


def test_auth_login_requires_client_secret(tmp_path, monkeypatch):
    monkeypatch.setenv("FASTGWS_CONFIG_DIR", str(tmp_path / "cfg"))
    with pytest.raises(ValidationError): cli.main(["auth", "login"])
