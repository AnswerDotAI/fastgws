"""Use fastgws to read and work with Google Workspace and Google APIs from Python. This skill exposes the base `GWSApi` client, OAuth credential loading, and generated Google API operations, and Workspace user administration. Use it when the task needs access to Gmail, Calendar, Drive, Docs, Sheets, Places, or another Google API published through Google's discovery documents.

# Credentials

`oauth_creds` (gclientid's, re-exported) loads the token `gclientid-auth` stored for an account: authorise or widen a grant in the shell with `gclientid-auth me@example.com --preset google-apps`, then `creds = await oauth_creds(account='me@example.com')`.

`scopes=` checks the token covers the task. If the token is missing, lacks those scopes, or can't refresh, gclientid follows its stored `reauth` setting: on (default where gclientid provisioned the client) runs `gclientid-auth` in the configured browser and waits for the user; off raises an error naming `gclientid-auth` for the user to run. `reauth=` overrides; see "Automatic re-authorization" in the gclientid README. Expired access tokens need no reload: fastgws refreshes during calls (including after a 401) and saves back to the token file. `logout` revokes a grant and deletes its token.

`svc_acct_creds`: when the user supplies a service account JSON and the API needs no browser consent. For user-owned Workspace data a service account usually needs domain-wide delegation plus `subject=`; otherwise OAuth is the safer default.

# Clients and calls

`GWSApi('gmail', creds=creds)` builds a client from the service's discovery document, fetched on creation. Resources are attribute groups (`await gmail.users.messages.list(...)`); `doc()` a resource group for its operations, then an operation for its params (the top-level client shows less). Operations are awaitable and take Python-style names (`userId`→`user_id`); check `doc()` rather than guessing. Responses are `GWSObject`s: fields as attributes or keys, nested dicts as nested objects.

Requests ask for gzip; Google's `fields=` trims responses. Transient failures (rate-limit 403s, 429s, 5xx, network errors) are retried. `op.pages()` iterates a list operation's pages. Where the service advertises HTTP batching, `op.batch([...])` runs many calls of one operation, one dict of args each, results in order:

    msgs = await gmail.users.messages.get.batch([
        dict(user_id='me', id=mid, format='minimal', fields='id,labelIds') for mid in ids])

Drive methods taking content have upload twins: `drive.files.upload` for `files.create`, `<name>_media` for the rest (e.g. `drive.files.update_media`). They use Google's resumable protocol but send the whole content from memory in one request, so memory caps upload size.

Google conventions: Gmail `user_id='me'` = signed-in mailbox, `q=` = Gmail search syntax; Drive `q=` = Drive query syntax, add `trashed=false` unless the task is about deleted files; Calendar `calendar_id='primary'` = main calendar, and time-window reads want `single_events=True, order_by='startTime'`.

# Workspace administration

`WorkspaceAdmin(creds)` manages the user lifecycle via separate methods: `create_user`, `assign_license`/`remove_license`, `suspend_user` (`suspended=False` restores), `delete_user`. Check the domain's existing product and SKU before assigning a licence. These are writes, so the skill doesn't allow them in sandboxed hosts.

# Read before write

Prefer read-only scopes and operations unless the user asks for a change. Generated methods can send mail, delete files, modify events, and change documents. Before anything destructive: read the operation's docs, state the effect, wait for explicit confirmation. A client exposes every method in the discovery document, whether or not the credentials have its scope.
"""

from pyskills.core import allow
from fastgws.auth import oauth_creds, logout, svc_acct_creds
from fastgws.core import GWSApi, GWSObject, GWSOpFunc
from fastgws.admin import WorkspaceAdmin

__all__ = ['GWSApi', 'GWSObject', 'oauth_creds', 'logout', 'svc_acct_creds', 'WorkspaceAdmin']

allow(GWSApi.__init__, svc_acct_creds, {GWSOpFunc: ['__call__', 'batch', 'pages']})
