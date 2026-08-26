from fastcore.utils import *
from fastcore.xdg import xdg_config_home
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import Flow
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote
from pyskills.core import allow

import asyncio, json, httpx


__all__ = ['gws_config_dir', 'token_has_scopes', 'listen_for_code', 'auth_url', 'finish_auth', 'oauth_creds', 'refresh_creds', 'logout', 'svc_acct_creds', 'token', 'auth_headers']

def gws_config_dir():
    "Default fastgws config directory."
    p = xdg_config_home()/'fastgws'
    p.mkdir(parents=True, exist_ok=True)
    return p

def token_has_scopes(token_path, scopes):
    "Check whether an authorized-user token file includes all requested scopes."
    token_path = Path(token_path)
    if not token_path.exists(): return False
    saved = set(json.loads(token_path.read_text()).get('scopes', []))
    return set(scopes).issubset(saved)

def listen_for_code(port):
    "Run a one-shot local server on `port` to catch the OAuth redirect, then return fetched creds"
    code = None
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal code
            code = parse_qs(urlparse(self.path).query).get('code', [None])[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Auth complete, you can close this tab.')
        def log_message(self, *a): pass
    with HTTPServer(('', port), Handler) as srv: srv.handle_request()
    return code

_flow = None

@allow
def auth_url(creds_path=None, scopes=None, redirect_uri=None, token_path=None):
    "Start an interactive OAuth flow, returning the URL for the user to visit; complete with `finish_auth`."
    global _flow
    if scopes is None: raise ValueError('`scopes` is required')
    creds_path = Path(ifnone(creds_path, gws_config_dir()/'credentials.json'))
    token_path = Path(ifnone(token_path, gws_config_dir()/'token.json'))
    if token_path.exists(): scopes = sorted(set(scopes) | set(json.loads(token_path.read_text()).get('scopes', [])))
    _flow = Flow.from_client_secrets_file(str(creds_path), scopes=scopes)
    _flow.redirect_uri = redirect_uri or first(_flow.client_config.get('redirect_uris', ()))
    if not _flow.redirect_uri: raise ValueError('No `redirect_uri` given, and no `redirect_uris` in credentials.json')
    url, _ = _flow.authorization_url(access_type='offline', prompt='consent')
    return url

@allow
def finish_auth(code, token_path=None):
    "Exchange the code (or full redirect URL) pasted by the user for creds, saved to `token_path`."
    if _flow is None: raise ValueError('No auth flow in progress; call `auth_url` first')
    code = code.strip()
    if code.startswith('http'): code = parse_qs(urlparse(code).query)['code'][0]
    _flow.fetch_token(code=unquote(code))
    creds = _flow.credentials
    creds.token_path = Path(ifnone(token_path, gws_config_dir()/'token.json'))
    creds.token_path.write_text(creds.to_json())
    return creds

@allow
async def oauth_creds(creds_path=None, token_path=None, scopes=None,
    interactive=True, redirect_uri=None, listen=False, port=0, open_url=print):
    """OAuth creds from config-dir `credentials.json`/`token.json` for `scopes`.

    `@allow` is applied at definition so every `from fastgws.auth import oauth_creds` copy is the sandbox-tracked wrapper:
    an expired token is refreshed on a worker thread, where only a tracked call's context survives the audit."""
    if scopes is None: raise ValueError('`scopes` is required')
    cfg = gws_config_dir()
    creds_path = Path(ifnone(creds_path, cfg/'credentials.json'))
    token_path = Path(ifnone(token_path, cfg/'token.json'))

    creds = Credentials.from_authorized_user_file(str(token_path)) if token_has_scopes(token_path, scopes) else None
    if creds: creds.token_path = token_path
    if creds and creds.valid: return creds
    if creds and creds.expired and creds.refresh_token: return await refresh_creds(creds)

    if not interactive: raise ValueError('Missing or invalid token, and `interactive=False`')

    url = auth_url(creds_path, scopes=scopes, redirect_uri=redirect_uri, token_path=token_path)
    await maybe_await(open_url(url))
    code = listen_for_code(port) if listen else input("Paste the code: ")
    return finish_auth(code, token_path)

async def refresh_creds(creds, token_path=None):
    "Refresh `creds` without blocking the event loop, saving to `token_path` (default: the file they were loaded from)."
    try: await asyncio.to_thread(creds.refresh, Request())
    except RefreshError as e: raise ValueError('Token refresh failed; re-run `oauth_creds` to re-authorize') from e
    token_path = ifnone(token_path, getattr(creds, 'token_path', None))
    if token_path: Path(token_path).write_text(creds.to_json())
    return creds

async def logout(token_path=None):
    "Revoke the saved OAuth grant at Google and remove `token_path`; no-op if no token is saved."
    token_path = Path(ifnone(token_path, gws_config_dir()/'token.json'))
    if not token_path.exists(): return
    tok = json.loads(token_path.read_text())
    tok = tok.get('refresh_token') or tok.get('token')
    if tok:
        async with httpx.AsyncClient() as c:
            r = await c.post('https://oauth2.googleapis.com/revoke', data={'token': tok})
            if r.status_code != 400: r.raise_for_status()
    token_path.unlink()

def svc_acct_creds(sa_path=None, scopes=None, subject=None):
    "Service account creds from config-dir `service_account.json`, optionally delegated to `subject`."
    if scopes is None: raise ValueError('`scopes` is required')
    sa_path = Path(ifnone(sa_path, gws_config_dir()/'service_account.json'))
    creds = service_account.Credentials.from_service_account_file(str(sa_path), scopes=scopes)
    return creds.with_subject(subject) if subject else creds

def token(creds):
    "Return a fresh bearer token from google-auth credentials."
    if not creds.valid: creds.refresh(Request())
    return creds.token

def auth_headers(creds=None, token_=None):
    "Return Authorization headers from creds or a raw token."
    token_ = token_ or token(creds)
    return {'Authorization': f'Bearer {token_}'}
