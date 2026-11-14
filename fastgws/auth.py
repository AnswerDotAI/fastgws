from fastcore.utils import *
from fastcore.xdg import xdg_config_home
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from pathlib import Path
from datetime import datetime, timezone
from google.oauth2.credentials import Credentials
import asyncio
import httpx2

from gclientid.creds import logout, oauth_creds as _oauth_creds, refresh_creds, token_has_scopes
from pyskills.core import allow


__all__ = ['gws_config_dir', 'in_solveit', 'solveit_creds', 'SolveitCredentials', 'token_has_scopes', 'oauth_creds', 'refresh_creds', 'logout', 'svc_acct_creds', 'token', 'auth_headers']

def gws_config_dir():
    "Default fastgws config directory."
    p = xdg_config_home()/'fastgws'
    p.mkdir(parents=True, exist_ok=True)
    return p

def in_solveit():
    "Whether this process has an owner key and a solve-lp URL."
    return bool(os.environ.get('AAI_USER_KEY') and os.environ.get('SOLVELP_URL'))

class SolveitCredentials(Credentials):
    "Short-lived Google credentials for the Gmail account connected in solve-lp."
    def __init__(self, scopes=None):
        super().__init__(token=None, scopes=scopes)
        self.email = None

    def refresh(self, request):
        url = os.environ['SOLVELP_URL'].rstrip('/') + '/gmail_token'
        res = httpx2.post(url, headers={'Authorization': os.environ['AAI_USER_KEY']})
        if res.status_code == 404:
            data = res.json()
            url = data.get('connect_url', 'your solve-lp dashboard')
            raise ValueError(f"No Gmail account connected. Connect Gmail at {url}")
        res.raise_for_status()
        data = res.json()
        missing = set(self.scopes or []) - set(data['scopes'])
        if missing: raise ValueError(f'Connected account lacks {sorted(missing)}. Please reconnect Gmail in solve-lp.')
        self.token,self.email = data['access_token'],data['email']
        expiry = datetime.fromisoformat(data['expiry'])
        self.expiry = expiry.astimezone(timezone.utc).replace(tzinfo=None) if expiry.tzinfo else expiry

def solveit_creds(scopes=None):
    "Get credentials for the connected Gmail account, checking the requested scopes."
    if not in_solveit(): raise ValueError('SolveIt credentials require AAI_USER_KEY and SOLVELP_URL')
    creds = SolveitCredentials(scopes)
    creds.refresh(None)
    return creds

@allow
async def oauth_creds(token_path=None, scopes=None, account=None, internal=False, desktop=False, reauth=None):
    "Use the dashboard Gmail connection in SolveIt, or load a token file or named account via gclientid."
    if token_path is None and account is None and not internal and not desktop and in_solveit():
        cfg = gws_config_dir()
        if (cfg/'token.json').is_file(): token_path = cfg/'token.json'
        elif not (cfg/'credentials.json').exists(): return await asyncio.to_thread(solveit_creds, scopes)
    return await _oauth_creds(token_path=token_path, scopes=scopes, account=account,
                              internal=internal, desktop=desktop, reauth=reauth)

def svc_acct_creds(sa_path=None, scopes=None, subject=None):
    "Service account creds for the required `scopes`, from config-dir `service_account.json` or `sa_path`, optionally delegated to `subject`."
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
