"""Use fastgws to read and work with Google Workspace and Google APIs from Python. This skill exposes the base `GWSApi` client, OAuth credential loading, and generated Google API operations. Use it when the task needs access to Gmail, Calendar, Drive, Docs, Sheets, Places, or another Google API published through Google's discovery documents.

# Authentication

Use `oauth_creds` to load Google OAuth credentials for the scopes needed by the task. Agents should normally call it with `interactive=False`, which means only previously authorized tokens can be used. If a new scope is needed, the user should run the interactive OAuth step manually in a code cell, then the agent can load the saved token afterward.

If `interactive=False` fails with a missing or invalid token error, explain that the requested scope has not been authorized yet. Ask the user to run the same call manually without `interactive=False`, for example:

```python
creds = oauth_creds(scopes=['https://www.googleapis.com/auth/gmail.readonly'],
                    redirect_uri='https://oauth.appapis.org/redirect')
```

After the user completes the OAuth flow, load the credentials with `interactive=False` before making API calls.

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

# Calendar notes

Use `calendar_id='primary'` for the authenticated user's main calendar. For event lists, prefer `single_events=True` and `order_by='startTime'` when reading a time window.

```python
events = await calendar.events.list(calendar_id='primary', single_events=True, order_by='startTime')
```

# Gotchas

`oauth_creds(..., interactive=True)` may display an authorization link but fail to collect the pasted code inside agent tool calls. Use `interactive=False` from the agent. If new scopes are needed, ask the user to run the interactive OAuth call manually in a code cell.

Google APIs use many different parameter names. Inspect the specific operation with `doc(...)` before guessing. fastgws converts names to Python style, so `userId` becomes `user_id`, `maxResults` becomes `max_results`, and so on.

Some list responses are paginated. If the response includes `nextPageToken`, pass it back as `page_token` to fetch the next page.

Generated clients expose whatever the Google discovery document exposes. The presence of a method does not mean the saved credentials have the required scope.
"""

from pyskills.core import allow
from fastgws.auth import oauth_creds, svc_acct_creds
from fastgws.core import GWSApi, GWSObject, GWSOpFunc

__all__ = ['GWSApi', 'GWSObject', 'oauth_creds', 'svc_acct_creds']

allow(GWSApi.__init__, oauth_creds, svc_acct_creds, {GWSOpFunc: ['__call__']})

