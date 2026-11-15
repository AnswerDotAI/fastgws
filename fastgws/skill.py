# NB: this file is designed for an LLM reader, not a human. Add it to your LLM's context and ask it to explain.
"""Use fastgws to read and work with Google Workspace and Google APIs from Python, including Workspace user administration. Use it when the task needs access to Gmail, Calendar, Drive, Docs, Sheets, Places, or another Google API published through Google's discovery documents.

notation: /why

## Credentials

- `creds = await oauth_creds(account='me@example.com')`; new or wider grant first: shell `gclientid-auth me@example.com --preset google-apps`; `scopes=`, `reauth=`, token files: `doc(oauth_creds)`
- stored `reauth` setting: on by default where gclientid provisioned the client; off: error naming `gclientid-auth` for the user to run; details: gclientid README, "Automatic re-authorization"
- expired access token: refreshed during calls, after a 401 too, and saved to the token file; no reload needed
- service account (`doc(svc_acct_creds)`): when the user supplies a service-account JSON and the API needs no browser consent; user-owned Workspace data usually also needs domain-wide delegation, `subject=`; otherwise OAuth is the safer default

## Calls

- `gmail = GWSApi('gmail', creds=creds)`; a resource group's ops: `doc(gmail.users.messages)`; an op's params, with Google's notes (`user_id='me'`, `q` syntax, `fields`): `doc(gmail.users.messages.list)`    /top-level client shows less
- other auth (`token`, `api_key`), API version: `doc(GWSApi)`
- responses: `GWSObject`, nested dicts too; transient failures (rate-limit 403s, 429s, 5xx, network errors): retried
- list op: `op.pages()`; many calls of one op: `op.batch(calls)`; `doc()` each
- Drive content: `drive.files.upload` for `files.create`, `<name>_media` for the rest (e.g. `drive.files.update_media`); resumable protocol, but whole content sent from memory in one request: memory caps upload size

## Google conventions the op docs lack

- Drive `q`: add `trashed=false` unless the task is about deleted files
- Calendar time-window reads: pass `single_events=True, order_by='startTime'`

## Writes

- prefer read-only scopes and ops unless the user asks for a change    /a client exposes every discovery method, scope or not: generated methods can send mail, delete files, change events and documents
- before anything destructive: read the op's docs, state the effect, wait for explicit confirmation
- `WorkspaceAdmin` (methods, scopes: `doc(WorkspaceAdmin)`): check the domain's existing product and SKU before assigning a licence; writes: not allowed in sandboxed hosts
"""

from pyskills.core import allow
from fastgws.auth import oauth_creds, logout, svc_acct_creds
from fastgws.core import GWSApi, GWSObject, GWSOpFunc
from fastgws.admin import WorkspaceAdmin

__all__ = ['GWSApi', 'GWSObject', 'oauth_creds', 'logout', 'svc_acct_creds', 'WorkspaceAdmin']

allow(GWSApi.__init__, svc_acct_creds, {GWSOpFunc: ['__call__', 'batch', 'pages']})
