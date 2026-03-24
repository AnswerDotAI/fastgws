from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class ParamMeta:
    py_name: str
    api_name: str
    location: str
    required: bool
    repeated: bool
    type: str | None
    enum_values: list[str] = field(default_factory=list)
    description: str = ""
    default: str | None = None

    def to_dict(self): return asdict(self)


@dataclass
class MethodMeta:
    dotted_path: str
    api_dotted_path: str
    resource_path: str
    py_name: str
    api_name: str
    http_method: str
    path: str
    flat_path: str | None
    description: str
    path_params: list[ParamMeta]
    query_params: list[ParamMeta]
    request_schema_ref: str | None
    response_schema_ref: str | None
    scopes: list[str]
    supports_media_upload: bool
    media_upload_path: str | None
    supports_media_download: bool

    def to_dict(self):
        data = asdict(self)
        data["path_params"] = [o.to_dict() for o in self.path_params]
        data["query_params"] = [o.to_dict() for o in self.query_params]
        return data


@dataclass
class ServiceMeta:
    alias: str
    api_name: str
    version: str
    title: str
    description: str
    documentation_link: str | None
    root_url: str
    base_url: str | None
    service_path: str | None
    methods: list[MethodMeta]
    schemas: dict
    auth_scopes: dict[str, str] = field(default_factory=dict)

    def to_dict(self):
        data = asdict(self)
        data["methods"] = [o.to_dict() for o in self.methods]
        return data


def param_from_dict(data): return ParamMeta(**data)


def method_from_dict(data):
    data = dict(data, path_params=[param_from_dict(o) for o in data["path_params"]], query_params=[param_from_dict(o) for o in data["query_params"]])
    return MethodMeta(**data)


def service_from_dict(data): return ServiceMeta(**dict(data, methods=[method_from_dict(o) for o in data["methods"]]))
