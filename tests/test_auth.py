import asyncio, json, threading, pytest
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from fastgws.auth import oauth_creds, solveit_creds, in_solveit

GM = 'https://www.googleapis.com/auth/gmail.modify'

def mk_broker(resp, status=200):
    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            if self.path != '/gmail_token' or self.headers.get('Authorization') != 'uid1:key':
                return self.send_error(401)
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode())
        def log_message(self, *a): pass
    srv = HTTPServer(('127.0.0.1', 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

def _use(monkeypatch, srv):
    monkeypatch.setenv('SOLVELP_URL', f'http://127.0.0.1:{srv.server_port}')
    monkeypatch.setenv('AAI_USER_KEY', 'uid1:key')

def test_solveit_creds(monkeypatch, tmp_path):
    monkeypatch.setenv('XDG_CONFIG_HOME', str(tmp_path))
    monkeypatch.delenv('AAI_USER_KEY', raising=False)
    assert not in_solveit()
    with pytest.raises(ValueError): solveit_creds([GM])

    expiry = (datetime.now(timezone.utc) + timedelta(seconds=3599)).isoformat()
    srv = mk_broker(dict(access_token='at-1', expiry=expiry, email='eg@answer.ai', scopes=[GM]))
    _use(monkeypatch, srv)
    creds = asyncio.run(oauth_creds(scopes=[GM]))
    assert creds.valid and creds.token == 'at-1' and creds.email == 'eg@answer.ai'
    assert creds.expiry.tzinfo is None  # google-auth requires naive UTC expiry
    with pytest.raises(ValueError, match='reconnect'): solveit_creds([GM, GM + '.extra'])
    srv.shutdown()

    srv = mk_broker(dict(error='not_connected', connect_url='https://solve.it.com/dashboard'), status=404)
    _use(monkeypatch, srv)
    with pytest.raises(ValueError, match='dashboard'): solveit_creds([GM])
    srv.shutdown()

def test_solveit_local_credentials(monkeypatch, tmp_path):
    from unittest.mock import AsyncMock
    from fastgws import auth
    monkeypatch.setenv('AAI_USER_KEY', 'uid1:key')
    monkeypatch.setenv('SOLVELP_URL', 'http://127.0.0.1')
    monkeypatch.setenv('XDG_CONFIG_HOME', str(tmp_path))
    loader = AsyncMock()
    monkeypatch.setattr(auth, '_oauth_creds', loader)
    asyncio.run(oauth_creds(account='other@example.com', desktop=True, reauth=False))
    loader.assert_awaited_once_with(token_path=None, scopes=None, account='other@example.com',
                                    internal=False, desktop=True, reauth=False)

    path = auth.gws_config_dir()/'token.json'
    path.touch()
    asyncio.run(oauth_creds(scopes=[GM]))
    assert loader.await_args.kwargs['token_path'] == path
