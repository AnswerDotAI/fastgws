from fastcore.utils import *
from fastcore.xdg import xdg_config_home
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from pathlib import Path
from urllib.parse import quote
from pyskills.core import allow

import asyncio, json, httpx, shlex


__all__ = ['gws_config_dir', 'gclientid_token', 'token_has_scopes', 'oauth_creds', 'refresh_creds', 'logout', 'svc_acct_creds', 'token', 'auth_headers']

def gws_config_dir():
    "Default fastgws config directory."
    p = xdg_config_home()/'fastgws'
    p.mkdir(parents=True, exist_ok=True)
    return p

def gclientid_token(account, internal=False):
    "Standard gclientid authorized-user token path for `account`."
    name = quote(account.casefold(), safe='@._+-')
    suffix = '-internal' if internal else ''
    return xdg_config_home()/'gclientid'/f'oauth-token-{name}{suffix}.json'

def token_has_scopes(token_path, scopes):
    "Check whether an authorized-user token file includes all requested scopes."
    token_path = Path(token_path).expanduser()
    if not token_path.exists(): return False
    if scopes is None: return True
    saved = set(json.loads(token_path.read_text()).get('scopes', []))
    return set(scopes).issubset(saved)

def _save_creds(creds, token_path):
    token_path = Path(token_path).expanduser()
    token_path.parent.mkdir(parents=True, exist_ok=True)
    account = json.loads(token_path.read_text()).get('account') if token_path.exists() else None
    data = json.loads(creds.to_json())
    if account: data['account'] = account
    token_path.write_text(json.dumps(data))
    token_path.chmod(0o600)
    creds.token_path = token_path
    return creds

def _reauth_cmd(creds):
    "Command that recreates the gclientid grant represented by `creds`."
    cmd = ['gclientid-auth']
    token_path = getattr(creds, 'token_path', None)
    if token_path and Path(token_path).stem.endswith('-internal'): cmd.append('--internal')
    if creds.account: cmd += ['--account', creds.account]
    return shlex.join(cmd)

def _refresh_error(creds, err):
    "Explain a Google refresh failure and how to recover."
    cmd = _reauth_cmd(creds)
    if 'Reauthentication is needed' in str(err):
        account = f' for {creds.account}' if creds.account else ''
        return ValueError(f'Google Cloud session expired{account}; run `{cmd}` to reauthenticate')
    return ValueError(f'Token refresh failed; run `{cmd}` to reauthorize')

@allow
async def oauth_creds(token_path=None, scopes=None, account=None, internal=False):
    """OAuth creds from a token file, or gclientid's standard path when `account` is supplied.

    Pass `internal=True` to use gclientid's separately stored Internal OAuth profile.

    `@allow` is applied at definition so every `from fastgws.auth import oauth_creds` copy is the sandbox-tracked wrapper:
    an expired token is refreshed on a worker thread, where only a tracked call's context survives the audit."""
    if account and token_path: raise ValueError('Pass either `account` or `token_path`, not both')
    if not account and not token_path: raise ValueError('Pass `account` or `token_path`')
    token_path = Path(token_path).expanduser() if token_path else gclientid_token(account, internal)

    creds = Credentials.from_authorized_user_file(str(token_path)) if token_has_scopes(token_path, scopes) else None
    if creds: creds.token_path = token_path
    if creds and creds.valid: return creds
    if creds and creds.expired and creds.refresh_token: return await refresh_creds(creds)
    raise ValueError(f'Missing or invalid token: {token_path}; authorize it with gclientid-auth')

async def refresh_creds(creds, token_path=None):
    "Refresh `creds` without blocking the event loop, saving to `token_path` (default: the file they were loaded from)."
    try: await asyncio.to_thread(creds.refresh, Request())
    except RefreshError as e: raise _refresh_error(creds, e) from e
    token_path = ifnone(token_path, getattr(creds, 'token_path', None))
    if token_path: _save_creds(creds, token_path)
    return creds

async def logout(token_path=None, account=None, internal=False):
    "Revoke and remove a default or Internal token selected by `account` or `token_path`; no-op if it does not exist."
    if account and token_path: raise ValueError('Pass either `account` or `token_path`, not both')
    if not account and not token_path: raise ValueError('Pass `account` or `token_path`')
    token_path = Path(token_path).expanduser() if token_path else gclientid_token(account, internal)
    if not token_path.exists(): return
    tok = json.loads(token_path.read_text())
    tok = tok.get('refresh_token') or tok.get('token')
    if tok:
        async with httpx.AsyncClient(timeout=10) as c:
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
