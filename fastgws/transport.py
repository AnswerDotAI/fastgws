from __future__ import annotations

from dataclasses import dataclass, field
from mimetypes import guess_type
from pathlib import Path
from urllib.parse import quote
import json, re

import requests

from .auth import apply_credentials
from .errors import APIError, ValidationError
from .helpers import dict_to_obj


Query = list


@dataclass
class RequestSpec:
    http_method: str
    url: str
    query: Query = field(default_factory=list)
    headers: dict[str, str] = field(default_factory=dict)
    json_body: dict | list | None = None
    data: bytes | None = None
    download: str | bool | None = None


def compose_request(service, method, api_values, *, body=None, upload=None, upload_content_type=None, download=None):
    path_template = _select_path_template(method)
    base = _upload_base(service, method) if upload else _base_url(service)
    path = _render_path(path_template if not upload else method.media_upload_path, api_values)
    url = _join_url(base, path)
    query = _build_query(method, api_values)
    headers = {}
    data = None
    json_body = body
    if upload:
        content, content_type = _load_upload(upload, upload_content_type)
        if body is None:
            data = content
            query.append(("uploadType", "media"))
            headers["Content-Type"] = content_type
            json_body = None
        else:
            data, boundary = _multipart_body(body, content, content_type)
            query.append(("uploadType", "multipart"))
            headers["Content-Type"] = f"multipart/related; boundary={boundary}"
            json_body = None
    if download is not None: query.append(("alt", "media"))
    return RequestSpec(method.http_method, url, query=query, headers=headers, json_body=json_body, data=data, download=download)


def render_path_template(path_template, values): return _render_path(path_template, values)


def _base_url(service): return service.base_url or _join_url(service.root_url, service.service_path or "")


def _upload_base(service, method):
    if not method.media_upload_path: raise ValidationError("method supports media upload but has no upload path")
    return service.root_url.rstrip("/")


def _join_url(base, path):
    base = base.rstrip("/")
    path = (path or "").lstrip("/")
    return f"{base}/{path}" if path else base


def _select_path_template(method):
    if not method.flat_path: return method.path
    names = {p.api_name for p in method.path_params}
    tokens = set(_template_names(method.flat_path))
    return method.flat_path if names.issubset(tokens) else method.path


def _template_names(path): return [token.lstrip("+") for token in re.findall(r"\{([^}]+)\}", path)]


def _render_path(path_template, values):
    def repl(match):
        token = match.group(1)
        plus = token.startswith("+")
        name = token[1:] if plus else token
        if name not in values: return match.group(0)
        value = str(values[name])
        return quote(value, safe="/") if plus else quote(value, safe="")

    return re.sub(r"\{([^}]+)\}", repl, path_template)


def _build_query(method, api_values):
    params = []
    repeated = {p.api_name for p in method.query_params if p.repeated}
    known = {p.api_name for p in method.query_params}
    for key in sorted(known):
        if key not in api_values or api_values[key] is None: continue
        value = api_values[key]
        if key in repeated:
            if not isinstance(value, (list, tuple)): raise ValidationError(f"{key} must be a list")
            params.extend((key, _stringify(item)) for item in value)
        else: params.append((key, _stringify(value)))
    return params


def _stringify(value):
    if isinstance(value, bool): return "true" if value else "false"
    if isinstance(value, (dict, list)): return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def _load_upload(upload, content_type=None):
    if isinstance(upload, bytes): return upload, content_type or "application/octet-stream"
    path = Path(upload)
    return path.read_bytes(), content_type or guess_type(path.name)[0] or "application/octet-stream"


def _multipart_body(metadata, content, content_type):
    boundary = "fastgws_boundary"
    meta = json.dumps(metadata or {}, sort_keys=True)
    body = b"".join([
        f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{meta}\r\n".encode(),
        f"--{boundary}\r\nContent-Type: {content_type}\r\n\r\n".encode(),
        content,
        f"\r\n--{boundary}--\r\n".encode()])
    return body, boundary


class RequestsTransport:
    def __init__(self, session=None): self.session = session or requests.Session()

    def execute(self, spec: RequestSpec, *, credentials=None):
        headers = dict(spec.headers)
        apply_credentials(credentials, spec.http_method, spec.url, headers)
        response = self.session.request(spec.http_method, spec.url, params=spec.query, headers=headers, json=spec.json_body, data=spec.data)
        if not response.ok:
            msg = f"{spec.http_method} {spec.url} failed with HTTP {response.status_code}"
            status, method, url = response.status_code, spec.http_method, spec.url
            raise APIError(msg, status_code=status, method=method, url=url, body=response.text)
        if spec.download is True: return response.content
        if spec.download:
            path = Path(spec.download)
            path.write_bytes(response.content)
            return path
        content_type = response.headers.get("content-type", "")
        if "json" in content_type: return dict_to_obj(response.json())
        return response.content
