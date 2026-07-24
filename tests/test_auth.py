import json, threading, pytest
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from fastgws.auth import SolveitCredentials, solveit_creds, in_solveit

GM = 'https://www.googleapis.com/auth/gmail.modify'

def mk_broker(resp, status=200):
    class H(BaseHTTPRequestHandler):
        def do_POST(self):
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

def test_solveit_creds(monkeypatch):
    monkeypatch.delenv('AAI_USER_KEY', raising=False)
    assert not in_solveit()
    with pytest.raises(ValueError): solveit_creds([GM])

    expiry = (datetime.now(timezone.utc) + timedelta(seconds=3599)).isoformat()
    srv = mk_broker(dict(access_token='at-1', expiry=expiry, email='eg@answer.ai', scopes=[GM]))
    _use(monkeypatch, srv)
    creds = solveit_creds([GM])
    assert creds.valid and creds.token == 'at-1' and creds.email == 'eg@answer.ai'
    assert creds.expiry.tzinfo is None  # google-auth requires naive UTC expiry
    with pytest.raises(ValueError, match='reconnect'): solveit_creds([GM, GM + '.extra'])
    srv.shutdown()

    srv = mk_broker(dict(error='not_connected', connect_url='https://solve.it.com/dashboard'), status=404)
    _use(monkeypatch, srv)
    with pytest.raises(ValueError, match='dashboard'): solveit_creds([GM])
    srv.shutdown()
