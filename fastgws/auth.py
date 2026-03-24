from __future__ import annotations

from pathlib import Path
import json, os, shutil

from google.auth import default as google_auth_default
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials as UserCredentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow

from .errors import ValidationError


def config_dir():
    path = Path(os.getenv("FASTGWS_CONFIG_DIR", Path.home() / ".config" / "fastgws"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def credentials_path(): return Path(os.getenv("FASTGWS_CREDENTIALS_FILE", config_dir() / "credentials.json"))


def client_secret_path(): return Path(os.getenv("FASTGWS_CLIENT_SECRET_FILE", config_dir() / "client_secret.json"))


def local_credentials(scopes=None):
    path = credentials_path()
    if not path.exists(): return None
    return load_authorized_user(path)


def default_credentials(scopes=None):
    creds = local_credentials(scopes=scopes)
    if creds is not None: return creds
    creds, _ = google_auth_default(scopes=scopes)
    return creds


def load_service_account(path, scopes=None): return ServiceAccountCredentials.from_service_account_file(path, scopes=scopes)


def load_authorized_user(path, scopes=None):
    creds = UserCredentials.from_authorized_user_file(path, scopes=scopes)
    if scopes and getattr(creds, "requires_scopes", False): creds = creds.with_scopes(scopes)
    return creds


def login_local(path, scopes): return InstalledAppFlow.from_client_secrets_file(path, scopes=scopes).run_local_server(port=0)


def save_authorized_user(creds, path=None):
    path = Path(path or credentials_path())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_pretty_json(creds.to_json()))
    _chmod_private(path)
    return path


def save_client_secret(src, dst=None):
    src, dst = Path(src), Path(dst or client_secret_path())
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    _chmod_private(dst)
    return dst


def resolve_client_secret(path=None):
    path = Path(path or client_secret_path())
    if not path.exists(): raise ValidationError(f"OAuth client secret file not found: {path}")
    return path


def parse_scopes(value=None):
    raw = value or "https://www.googleapis.com/auth/drive.readonly"
    scopes = [o.strip() for o in raw.split(",") if o.strip()]
    if not scopes: raise ValidationError("at least one OAuth scope is required")
    return scopes


def login_and_save(*, client_secret=None, scopes=None):
    secret = resolve_client_secret(client_secret)
    creds = login_local(secret, parse_scopes(scopes))
    saved_secret = save_client_secret(secret)
    saved_creds = save_authorized_user(creds)
    return creds, saved_secret, saved_creds


def apply_credentials(credentials, method, url, headers):
    if credentials is None: return headers
    request = Request()
    if hasattr(credentials, "before_request"): credentials.before_request(request, method, url, headers)
    elif hasattr(credentials, "apply"): credentials.apply(headers)
    return headers


def _pretty_json(value):
    if isinstance(value, str): return json.dumps(json.loads(value), indent=2, sort_keys=True) + "\n"
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def _chmod_private(path):
    if os.name != "posix": return
    path.chmod(0o600)
