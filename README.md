# fastgws

`fastgws` is a discovery-driven Google Workspace client for Python and a thin CLI built on the same runtime.

It is designed around:

- lazy service/resource/method discovery
- generated method signatures and docs
- practical schema inspection and validation
- a simple CLI for calling the same endpoints from the shell

## Install

```bash
pip install fastgws
```

For local development in this repo:

```bash
pip install -e .[dev]
python -m fastgws.build all
```

## Quick Start

Python:

```python
from fastgws import FastGWS

api = FastGWS()
res = api.drive.files.list(page_size=5)

for f in getattr(res, "files", []):
    print(f.id, getattr(f, "name", None))
```

CLI:

```bash
fastgws services
fastgws drive.files.list --page_size 5
```

## Authentication

`fastgws` supports three main auth paths:

- OAuth user login for the CLI and local Python usage
- Google Application Default Credentials (ADC)
- service account credentials for Python

### OAuth User Login For The CLI

This is the easiest way to get started locally if you want `fastgws` to manage user credentials for you.

1. Create a Google Cloud OAuth client of type `Desktop app`.
2. Download the client JSON from Google Cloud Console.
3. Run:

```bash
fastgws auth login \
  --client-secret /path/to/client_secret.json \
  --scopes https://www.googleapis.com/auth/drive.readonly
```

This opens a local browser flow and saves:

- `~/.config/fastgws/client_secret.json`
- `~/.config/fastgws/credentials.json`

After that, normal CLI and Python calls can use the saved user credentials automatically:

```bash
fastgws drive.files.list --page_size 5
```

You can pass multiple scopes as a comma-separated list:

```bash
fastgws auth login \
  --client-secret /path/to/client_secret.json \
  --scopes https://www.googleapis.com/auth/drive.readonly,https://www.googleapis.com/auth/gmail.readonly
```

### Application Default Credentials

`FastGWS()` uses ADC when explicit credentials were not passed and no saved `fastgws` OAuth credentials exist.

Typical ADC options:

```bash
gcloud auth application-default login
```

or:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

Then:

```python
from fastgws import FastGWS

api = FastGWS()
```

### Python Auth Helpers

Explicit service account credentials:

```python
from fastgws import FastGWS

api = FastGWS.from_service_account(
    "/path/to/service-account.json",
    scopes=["https://www.googleapis.com/auth/drive.readonly"],
)
```

Explicit authorized-user credentials:

```python
from fastgws import FastGWS

api = FastGWS.from_authorized_user(
    "/path/to/credentials.json",
    scopes=["https://www.googleapis.com/auth/drive.readonly"],
)
```

Run a local browser OAuth flow directly from Python:

```python
from fastgws import FastGWS

api = FastGWS.login_local(
    "/path/to/client_secret.json",
    scopes=["https://www.googleapis.com/auth/drive.readonly"],
)
```

### Auth File Locations

By default, the CLI stores local auth state under `~/.config/fastgws`.

You can override those locations with:

- `FASTGWS_CONFIG_DIR`
- `FASTGWS_CLIENT_SECRET_FILE`
- `FASTGWS_CREDENTIALS_FILE`

## Python API

### Create A Client

```python
from fastgws import FastGWS

api = FastGWS()
```

Service shortcut clients are also available:

```python
from fastgws import Drive, Gmail, Sheets

drive = Drive()
gmail = Gmail()
sheets = Sheets()
```

### Discover The Surface

The runtime is lazy and notebook-friendly:

```python
from fastgws import FastGWS
import inspect

api = FastGWS()

dir(api)
dir(api.drive)
dir(api.drive.files)
inspect.signature(api.drive.files.list)
print(api.drive.files.list.__doc__)
```

### Make Calls

List files:

```python
from fastgws import FastGWS

api = FastGWS()
res = api.drive.files.list(page_size=5)
print(res)
```

Search by file name:

```python
res = api.drive.files.list(
    page_size=5,
    q="name contains 'report' and trashed = false",
)
```

Search indexed content:

```python
res = api.drive.files.list(
    page_size=5,
    q="fullText contains 'quarterly forecast' and trashed = false",
)
```

Positional path parameters also work:

```python
file = api.drive.files.get("FILE_ID")
```

### Pagination

Use `.pages()` to follow `nextPageToken`:

```python
for page in api.drive.files.list.pages(page_size=100):
    print(page)
```

Use `.items()` to iterate the main item collection:

```python
for item in api.drive.files.list.items(page_size=100):
    print(item.id, getattr(item, "name", None))
```

### Schema Inspection

Each method exposes a schema view:

```python
schema = api.drive.files.create.schema
print(schema)
```

You can also inspect schemas by dotted path:

```python
api.schema("drive.files.create")
api.schema("drive.files.create", resolve_refs=True)
api.schema("drive.File", resolve_refs=True)
```

### Request Validation

`fastgws` validates known parameters and request bodies before sending requests.

Validation catches:

- missing required params
- unknown params
- simple scalar type mismatches
- enum violations
- nested request body shape errors where schema data is available

Disable validation for a single call:

```python
api.drive.files.list(page_size=5, validate=False)
```

Disable it for the whole client:

```python
api = FastGWS(validate=False)
```

### Downloads

For binary downloads, pass `download=True` to get bytes back:

```python
data = api.drive.files.get("FILE_ID", download=True)
print(type(data), len(data))
```

Or pass a path to write the response directly:

```python
api.drive.files.get("FILE_ID", download="out.bin")
```

### Uploads

For media upload methods, pass `upload=` with a file path or raw bytes.

Media-only upload:

```python
api.drive.files.create(upload="/path/to/report.pdf")
```

Multipart upload with metadata:

```python
api.drive.files.create(
    body={"name": "report.pdf"},
    upload="/path/to/report.pdf",
    upload_content_type="application/pdf",
)
```

## CLI

The CLI is a thin layer over the same generated runtime as the Python API.

### List Services

```bash
fastgws services
```

### Show Schema

```bash
fastgws schema drive.files.create
fastgws schema drive.files.create --resolve-refs
```

### Show Generated Docs For An Endpoint

```bash
fastgws docs drive.files.list
```

### Show Endpoint Help

```bash
fastgws drive.files.list --help
```

### Call Endpoints

List Drive files:

```bash
fastgws drive.files.list --page_size 5
```

Get a single file by ID:

```bash
fastgws drive.files.get FILE_ID
```

Use a query:

```bash
fastgws drive.files.list \
  --page_size 5 \
  --q "name contains 'report' and trashed = false"
```

Call Gmail:

```bash
fastgws gmail.users.messages.list --user_id me --max_results 10
```

### CLI Output

- JSON responses print as formatted JSON
- non-JSON responses print raw values
- endpoint help prints the generated signature and docstring

## Development

### Build Generated Metadata

```bash
python -m fastgws.build all
```

Generated outputs are written to:

- `fastgws/generated/`
- `docs/api/`

### Test And Style

```bash
python -m pytest -q
chkstyle fastgws tests --skip-folder-re generated
```

### Generated Drift Check

```bash
python -m fastgws.build.check
```

## Current Scope

The current implementation focuses on:

- discovery-driven service metadata
- runtime-generated method signatures and docs
- schema inspection and practical request validation
- media upload and download helpers
- OAuth login for the CLI
- ADC and explicit credentials for Python

It does not yet aim to provide:

- handwritten high-level convenience wrappers for each API
- resumable upload flows
- async transport
- first-class typed request and response model generation

## Versioning

Version lives in `fastgws/__init__.py` as `__version__`.

Bump it with:

```bash
ship_bump --part 2
ship_bump --part 1
ship_bump --part 0
```

## Release

1. Ensure GitHub issues are labeled with `bug`, `enhancement`, or `breaking`.
2. Run:

```bash
ship_release_gh
ship_pypi
```
