from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from importlib import import_module
from inspect import Parameter, Signature

from .auth import default_credentials, load_authorized_user, load_service_account, login_local
from .errors import ValidationError
from .generated.registry import REGISTRY
from .models import service_from_dict
from .schema import build_method_schema, resolve_schema_refs, validate_method_call
from .transport import RequestsTransport, compose_request


@dataclass
class _TreeNode:
    py_name: str
    api_name: str
    groups: dict[str, "_TreeNode"] = field(default_factory=dict)
    group_aliases: dict[str, str] = field(default_factory=dict)
    methods: dict[str, object] = field(default_factory=dict)
    method_aliases: dict[str, str] = field(default_factory=dict)


class FastGWS:
    def __init__(self, credentials=None, transport=None, validate=True):
        self.credentials = credentials
        self.transport = transport or RequestsTransport()
        self.validate = validate
        self._services = {}

    @classmethod
    def from_fixture(cls, *_args, **kwargs): return cls(credentials=None, **kwargs)

    @classmethod
    def from_service_account(cls, path, scopes, **kwargs):
        return cls(credentials=load_service_account(path, scopes=scopes), **kwargs)

    @classmethod
    def from_authorized_user(cls, path, scopes, **kwargs):
        return cls(credentials=load_authorized_user(path, scopes=scopes), **kwargs)

    @classmethod
    def login_local(cls, path, scopes, **kwargs): return cls(credentials=login_local(path, scopes=scopes), **kwargs)

    def _credentials_for(self, service=None):
        if self.credentials is not None: return self.credentials
        scopes = sorted(service.auth_scopes) if service and service.auth_scopes else None
        return default_credentials(scopes=scopes)

    def __dir__(self): return sorted(set(super().__dir__() + list(REGISTRY)))

    def _repr_markdown_(self): return "\n".join(f"- `{name}`: {meta['description']}" for name, meta in sorted(REGISTRY.items()))

    def __getattr__(self, name):
        if name in REGISTRY:
            if name not in self._services: self._services[name] = _ServiceRuntime(self, _load_service(name))
            return self._services[name].group
        raise AttributeError(name)

    def resolve_endpoint(self, dotted_path):
        parts = dotted_path.split(".")
        if not parts or parts[0] not in REGISTRY: raise ValidationError(f"unknown service: {parts[0] if parts else dotted_path}")
        target = getattr(self, parts[0])
        for part in parts[1:]: target = getattr(target, part)
        return target

    def schema(self, dotted_path, resolve_refs=False):
        parts = dotted_path.split(".")
        if len(parts) < 2: raise ValidationError(f"invalid schema path: {dotted_path}")
        service = _load_service(parts[0])
        if len(parts) == 2 and parts[1] in service.schemas:
            schema = service.schemas[parts[1]]
            return resolve_schema_refs(service, schema) if resolve_refs else schema
        method = self.resolve_endpoint(dotted_path)
        return method.get_schema(resolve_refs=resolve_refs)


class _ServiceRuntime:
    def __init__(self, root, service):
        self.root, self.service = root, service
        self.tree = _build_tree(service)
        self.group = _GWSGroup(root, service, self.tree, service.alias, service.alias)


class _GWSGroup:
    def __init__(self, root, service, node, py_path, api_path):
        self._root, self._service, self._node = root, service, node
        self._py_path, self._api_path = py_path, api_path
        self._cache = {}

    def __dir__(self):
        return sorted(set(list(self._node.groups) + list(self._node.methods) + list(self._node.group_aliases) + list(self._node.method_aliases)))

    def _repr_markdown_(self):
        lines = [f"### `{self._py_path}`", ""]
        for name in sorted(self._node.groups): lines.append(f"- `{name}`/")
        for name in sorted(self._node.methods): lines.append(f"- `{name}`{_method_signature(self._node.methods[name])}")
        return "\n".join(lines)

    def __getattr__(self, name):
        target = name
        if target in self._node.group_aliases: target = self._node.group_aliases[target]
        if target in self._node.groups:
            if target not in self._cache:
                child = self._node.groups[target]
                api_name = child.api_name
                self._cache[target] = _GWSGroup(self._root, self._service, child, f"{self._py_path}.{target}", f"{self._api_path}.{api_name}")
            return self._cache[target]
        if target in self._node.method_aliases: target = self._node.method_aliases[target]
        if target in self._node.methods:
            if target not in self._cache: self._cache[target] = _GWSMethod(self._root, self._service, self._node.methods[target])
            return self._cache[target]
        raise AttributeError(name)


class _GWSMethod:
    def __init__(self, root, service, method):
        self._root, self._service, self._method = root, service, method
        self.__doc__ = _method_doc(method)
        self.signature = _method_signature(method)

    @property
    def __signature__(self): return self.signature

    def __call__(self, *args, **kwargs):
        kwargs = _bind_args(self._method, args, kwargs)
        values, body, upload, upload_content_type, download, do_validate = _split_kwargs(self._method, kwargs)
        if do_validate and self._root.validate: validate_method_call(self._service, self._method, values, body)
        api_values = _to_api_values(self._method, values)
        spec = compose_request(self._service, self._method, api_values, body=body, upload=upload, upload_content_type=upload_content_type, download=download)
        return self._root.transport.execute(spec, credentials=self._root._credentials_for(self._service))

    def __repr__(self): return f"{self._method.dotted_path}{self.signature}"

    def _repr_markdown_(self): return f"`{self._method.dotted_path}{self.signature}`"

    def get_schema(self, resolve_refs=False): return build_method_schema(self._service, self._method, resolve_refs=resolve_refs)

    @property
    def schema(self): return self.get_schema()

    def pages(self, **kwargs):
        token_param = next((p.py_name for p in self._method.query_params if p.api_name == "pageToken"), None)
        while True:
            page = self(**kwargs)
            yield page
            token = _page_value(page, "nextPageToken")
            if not token or not token_param: break
            kwargs[token_param] = token

    def items(self, **kwargs):
        for page in self.pages(**kwargs):
            for item in _page_items(page): yield item


class _SingleServiceClient:
    alias = ""

    def __init__(self, **kwargs):
        self._root = FastGWS(**kwargs)
        self._group = getattr(self._root, self.alias)

    def __dir__(self): return dir(self._group)

    def _repr_markdown_(self): return self._group._repr_markdown_()

    def __getattr__(self, name): return getattr(self._group, name)


class Drive(_SingleServiceClient):
    alias = "drive"


class Gmail(_SingleServiceClient):
    alias = "gmail"


class Sheets(_SingleServiceClient):
    alias = "sheets"


class Keep(_SingleServiceClient):
    alias = "keep"


def _load_service(alias):
    module = import_module(REGISTRY[alias]["module"])
    return service_from_dict(module.SERVICE)


def _build_tree(service):
    root = _TreeNode(service.alias, service.alias)
    for method in service.methods:
        py_parts = method.dotted_path.split(".")[1:]
        api_parts = method.api_dotted_path.split(".")[1:]
        node = root
        for py_name, api_name in zip(py_parts[:-1], api_parts[:-1]):
            node.group_aliases[api_name] = py_name
            node = node.groups.setdefault(py_name, _TreeNode(py_name, api_name))
        node.method_aliases[api_parts[-1]] = py_parts[-1]
        node.methods[py_parts[-1]] = method
    return root


def _method_signature(method):
    params = []
    for param in method.path_params + [o for o in method.query_params if o.required]:
        params.append(Parameter(param.py_name, Parameter.POSITIONAL_OR_KEYWORD, annotation=_annotation(param.type)))
    for param in [o for o in method.query_params if not o.required]:
        params.append(Parameter(param.py_name, Parameter.POSITIONAL_OR_KEYWORD, annotation=_annotation(param.type), default=None))
    if method.request_schema_ref: params.append(Parameter("body", Parameter.POSITIONAL_OR_KEYWORD, default=None))
    if method.supports_media_upload:
        params.append(Parameter("upload", Parameter.POSITIONAL_OR_KEYWORD, default=None))
        params.append(Parameter("upload_content_type", Parameter.POSITIONAL_OR_KEYWORD, default=None))
    if method.supports_media_download: params.append(Parameter("download", Parameter.POSITIONAL_OR_KEYWORD, default=None))
    params.append(Parameter("validate", Parameter.POSITIONAL_OR_KEYWORD, default=True))
    return Signature(params)


def _annotation(schema_type):
    return dict(string=str, integer=int, number=float, boolean=bool, array=list, object=dict).get(schema_type, str)


def _method_doc(method):
    lines = [method.description or method.dotted_path]
    params = method.path_params + method.query_params
    if params:
        lines += ["", "Parameters:"]
        for param in params:
            req = "required" if param.required else "optional"
            lines.append(f"  {param.py_name}: {req}. {param.description}".rstrip())
    if method.request_schema_ref: lines.append(f"  body: optional request body ({method.request_schema_ref})")
    return "\n".join(lines)


def _bind_args(method, args, kwargs):
    order = [p.py_name for p in method.path_params + method.query_params]
    if method.request_schema_ref: order.append("body")
    if method.supports_media_upload: order += ["upload", "upload_content_type"]
    if method.supports_media_download: order.append("download")
    order.append("validate")
    kwargs = dict(kwargs)
    for key, value in zip(order, args): kwargs.setdefault(key, value)
    aliases = {p.api_name: p.py_name for p in method.path_params + method.query_params}
    for old, new in list(aliases.items()):
        if old in kwargs and new not in kwargs: kwargs[new] = kwargs.pop(old)
    return kwargs


def _split_kwargs(method, kwargs):
    values = {}
    allowed = {p.py_name for p in method.path_params + method.query_params}
    for key in list(kwargs):
        if key in allowed: values[key] = kwargs.pop(key)
    body = kwargs.pop("body", None)
    upload = kwargs.pop("upload", None)
    upload_content_type = kwargs.pop("upload_content_type", None)
    download = kwargs.pop("download", None)
    do_validate = kwargs.pop("validate", True)
    if kwargs: raise ValidationError(f"unknown parameters: {', '.join(sorted(kwargs))}")
    return values, body, upload, upload_content_type, download, do_validate


def _to_api_values(method, values):
    mapping = OrderedDict()
    for param in method.path_params + method.query_params:
        if param.py_name in values: mapping[param.api_name] = values[param.py_name]
    return mapping


def _page_items(page):
    if isinstance(page, dict): keys = page.keys()
    else: keys = dir(page)
    for key in keys:
        if key.startswith("_") or key in {"kind", "etag", "nextPageToken"}: continue
        value = _page_value(page, key)
        if isinstance(value, list): return value
    return []


def _page_value(page, key):
    if isinstance(page, dict): return page.get(key)
    return getattr(page, key, None)
