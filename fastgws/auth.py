from fastcore.utils import *
from fastcore.xdg import xdg_config_home
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import asyncio, json, os, sys, httpx


__all__ = ['gws_config_dir', 'token_has_scopes', 'listen_for_code', 'oauth_creds', 'refresh_creds', 'logout', 'svc_acct_creds', 'token', 'auth_headers']

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
            self.send_response(200); self.end_headers()
            self.wfile.write(b'Auth complete, you can close this tab.')
        def log_message(self, *a): pass
    with HTTPServer(('', port), Handler) as srv: srv.handle_request()
    return code

async def oauth_creds(creds_path=None, token_path=None, scopes=None,
                      interactive=True, redirect_uri=None, listen=False, port=0, open_url=print):
    "OAuth creds from config-dir `credentials.json`/`token.json` for `scopes`."
    if scopes is None: raise ValueError('`scopes` is required')
    cfg = gws_config_dir()
    creds_path = Path(ifnone(creds_path, cfg/'credentials.json'))
    token_path = Path(ifnone(token_path, cfg/'token.json'))

    if token_path.exists() and not token_has_scopes(token_path, scopes): token_path.unlink()
    creds = Credentials.from_authorized_user_file(str(token_path), scopes) if token_path.exists() else None
    if creds: creds.token_path = token_path
    if creds and creds.valid: return creds
    if creds and creds.expired and creds.refresh_token: return await refresh_creds(creds)

    if not interactive: raise ValueError('Missing or invalid token, and `interactive=False`')
        
    flow = Flow.from_client_secrets_file(str(creds_path), scopes=scopes)
    flow.redirect_uri = ifnone(redirect_uri, 'http://localhost/')
    auth_url, _ = flow.authorization_url(access_type='offline', prompt='consent')
    await maybe_await(open_url(auth_url))

    code = listen_for_code(port) if listen else input("Paste the code: ")
    flow.fetch_token(code=code)
    creds = flow.credentials
    creds.token_path = token_path

    token_path.write_text(creds.to_json())
    return creds

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
