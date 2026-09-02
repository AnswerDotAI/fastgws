"""Use fastgws to read and work with Google Workspace and Google APIs from Python. This skill exposes the base `GWSApi` client, OAuth credential loading, and generated Google API operations, and Workspace user administration. Use it when the task needs access to Gmail, Calendar, Drive, Docs, Sheets, Places, or another Google API published through Google's discovery documents.

# Authentication

Use `oauth_creds(account=...)` to load the standard token created by [`gclientid`](https://answerdotai.github.io/gclientid/); the function itself is gclientid's, re-exported here. Authorize or expand an account's grant with `gclientid-auth`, then load it by email address:

```sh
gclientid-auth me@example.com --preset google-apps
```

```python
creds = await oauth_creds(account='me@example.com')
```

Pass `scopes=` when the task wants fastgws to verify that the saved token includes a particular set. `token_path=` loads an authorized-user JSON file stored somewhere else. What happens when the token is missing, insufficient, or can no longer be refreshed is gclientid's decision: see "Automatic re-authorization" in the gclientid README, and the Gotchas below.

Access tokens refresh automatically during API calls (including after a 401), and the fresh token is saved back to the token file, so there is no need to re-run `oauth_creds` when a token expires.

To sign out, `await logout(account='me@example.com')` revokes the saved grant at Google and deletes the stored token (a no-op if none is saved).

Service accounts are available through `svc_acct_creds` for Google APIs that support them. Use them when the user has provided a local service account JSON file and the target API can be accessed without a browser-based user consent flow. For Workspace data owned by a user, service accounts usually need domain-wide delegation and a `subject` user; otherwise OAuth credentials are the safer default.

```python
creds = svc_acct_creds(scopes=['https://www.googleapis.com/auth/drive.readonly'],
                       subject='user@example.com')
```

# Creating clients

Create a Google API client with `GWSApi(service, creds=creds)`, where `service` is the discovery API name such as `'gmail'`, `'calendar'`, `'drive'`, `'docs'`, or `'sheets'`. Operations are grouped as attributes, so a Gmail messages call looks like `gmail.users.messages.list(...)`, and a Drive files call looks like `drive.files.list(...)`.

```python
gmail = GWSApi('gmail', creds=creds)
```

# Calling operations

Generated operations are awaitable methods. Pass parameters using the Python names shown by `doc(...)` or the method signature; fastgws maps them back to the Google API parameter names. Responses are returned as lightweight objects, so fields can be read with attributes or dictionary keys.

```python
msgs = await gmail.users.messages.list(user_id='me', max_results=10)
```

Use `operation.batch([...])` when a Google discovery service advertises HTTP batching. Each item is a dictionary of arguments for that same operation; results preserve order. The default chunk size is 50, and `return_exceptions=True` puts a structured `APIError` in a failed call's result position. fastgws retries transient ordinary requests and only the failed parts of a batch, including Google 403 rate-limit reasons, 429s, 5xx responses, and network failures.

```python
msgs = await gmail.users.messages.get.batch([
    dict(user_id='me', id=mid, format='minimal', fields='id,labelIds') for mid in ids
])
```

Google clients request gzip automatically. Use the global `fields=` parameter to avoid transferring fields the task does not need.

# Finding available methods

Use `doc(...)` on generated groups to see their operations, then use it on a specific operation to see its parameters. Top-level clients are less useful to inspect than their resource groups.

```python
doc(gmail.users.messages)
doc(gmail.users.messages.list)
```

If `doc` has been shadowed by another variable, use `pyskills.core.doc(...)` instead.

# Response objects

fastgws converts JSON responses into lightweight Python objects. Fields can usually be read as attributes or dictionary keys. Lists remain iterable, and nested dictionaries become nested objects.

```python
msgs = await gmail.users.messages.list(user_id='me', max_results=10)
msgs.messages[0].id
```

# Read before write

Prefer read-only scopes and read-only operations unless the user explicitly asks for a change. Some generated methods can send mail, delete files, modify calendar events, or change document contents. For destructive actions, inspect the operation docs first, state what will happen, and wait for explicit confirmation before calling it.

# Gmail notes

Use `user_id='me'` for the authenticated mailbox. Gmail search uses the same query syntax as the Gmail search box, so `q='from:someone@example.com newer_than:7d'` works with `users.messages.list`.

```python
msgs = await gmail.users.messages.list(user_id='me', q='is:unread', max_results=10)
```

# Drive notes

Use Drive search queries with `drive.files.list(q=...)`. Ask only for the fields needed when working with many files, and include `trashed=false` unless the task is specifically about deleted files.

```python
files = await drive.files.list(q="name contains 'report' and trashed=false", page_size=10)
```

A Drive method that accepts content has an upload twin. `drive.files.upload(media=..., name=...)` sends bytes, a path, or a file-like with the same metadata `files.create` takes; `drive.files.update_media(file_id=..., media=...)` replaces a file's content. Uploads use Google's resumable protocol; the content is read into memory and sent in one request, so very large files are bounded by available memory.

# Calendar notes

Use `calendar_id='primary'` for the authenticated user's main calendar. For event lists, prefer `single_events=True` and `order_by='startTime'` when reading a time window.

```python
events = await calendar.events.list(calendar_id='primary', single_events=True, order_by='startTime')
```

# Workspace administration

Use `WorkspaceAdmin(creds)` for user lifecycle work. Its credentials need `admin.directory.user` and `apps.licensing`. Creation, licence assignment/removal, suspension/restoration, and deletion are deliberately separate methods; inspect the domain's existing product and SKU before assigning a licence.

```python
admin = WorkspaceAdmin(creds)
user = await admin.create_user('new@example.com', 'New', 'User', password,
                               org_unit_path='/Internal')
await admin.assign_license(user.primaryEmail, sku_id)
```
# Gotchas

`oauth_creds` loads or refreshes stored credentials. When gclientid's store has `reauth = true` (the default on a machine where `gclientid` provisioned the client), a missing, insufficient, or unrefreshable token makes it run `gclientid-auth` in the configured browser and wait for the user; otherwise it raises an error naming that command, and the user must run it. Pass `reauth=` to force either behaviour.

Google APIs use many different parameter names. Inspect the specific operation with `doc(...)` before guessing. fastgws converts names to Python style, so `userId` becomes `user_id`, `maxResults` becomes `max_results`, and so on.

List operations expose `pages()`. The async iterator forwards each `nextPageToken` as `page_token` and stops after the final page.

Generated clients expose whatever the Google discovery document exposes. The presence of a method does not mean the saved credentials have the required scope.
"""

from pyskills.core import allow
from fastgws.auth import oauth_creds, logout, svc_acct_creds
from fastgws.core import GWSApi, GWSObject, GWSOpFunc
from fastgws.admin import WorkspaceAdmin

__all__ = ['GWSApi', 'GWSObject', 'oauth_creds', 'logout', 'svc_acct_creds', 'WorkspaceAdmin']

allow(GWSApi.__init__, svc_acct_creds, {GWSOpFunc: ['__call__', 'batch']}, WorkspaceAdmin.__init__, WorkspaceAdmin.create_user,
    WorkspaceAdmin.assign_license, WorkspaceAdmin.remove_license, WorkspaceAdmin.suspend_user, WorkspaceAdmin.delete_user)
