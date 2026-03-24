from __future__ import annotations

from copy import deepcopy

from .errors import ValidationError

_simple_types = dict(string=str, integer=int, number=(int, float), boolean=bool, array=list, object=dict)


def build_method_schema(service, method, *, resolve_refs=False):
    params = {p.api_name: _param_json(p) for p in method.path_params + method.query_params}
    data = dict(httpMethod=method.http_method, path=method.path, description=method.description, parameters=params, scopes=method.scopes)
    if method.request_schema_ref:
        data["requestBody"] = {"schemaRef": method.request_schema_ref, "schema": _schema_json(service.schemas.get(method.request_schema_ref))}
    if method.response_schema_ref:
        data["response"] = {"schemaRef": method.response_schema_ref, "schema": _schema_json(service.schemas.get(method.response_schema_ref))}
    return resolve_schema_refs(service, data) if resolve_refs else data


def resolve_schema_refs(service, value): return _resolve_refs(deepcopy(value), service.schemas, set())


def validate_method_call(service, method, values, body):
    params = method.path_params + method.query_params
    seen = {p.py_name for p in params}
    for param in params:
        if param.required and param.py_name not in values: raise ValidationError(f"missing required parameter: {param.py_name}")
        if param.py_name in values: _validate_param(values[param.py_name], param)
    unknown = set(values) - seen
    if unknown: raise ValidationError(f"unknown parameters: {', '.join(sorted(unknown))}")
    if method.request_schema_ref and body is not None: _validate_schema_value(body, {"$ref": method.request_schema_ref}, service.schemas, "$")


def _param_json(param):
    data = dict(type=param.type or "string", required=param.required, location=param.location)
    if param.description: data["description"] = param.description
    if param.enum_values: data["enum"] = list(param.enum_values)
    if param.default is not None: data["default"] = param.default
    if param.repeated: data["repeated"] = True
    return data


def _schema_json(schema): return deepcopy(schema or {})


def _resolve_refs(value, schemas, seen):
    if isinstance(value, dict):
        ref = value.get("$ref")
        if ref and ref not in seen and ref in schemas:
            seen.add(ref)
            resolved = _resolve_refs(deepcopy(schemas[ref]), schemas, seen)
            merged = {**resolved, **{k: _resolve_refs(v, schemas, seen) for k, v in value.items() if k != "$ref"}}
            seen.remove(ref)
            return merged
        return {k: _resolve_refs(v, schemas, seen) for k, v in value.items()}
    if isinstance(value, list): return [_resolve_refs(v, schemas, seen) for v in value]
    return value


def _validate_param(value, param):
    if value is None: return
    if param.repeated:
        if not isinstance(value, (list, tuple)): raise ValidationError(f"{param.py_name} must be a list")
        for item in value: _validate_scalar(item, param.type, param.enum_values, param.py_name)
        return
    _validate_scalar(value, param.type, param.enum_values, param.py_name)


def _validate_scalar(value, schema_type, enum_values, path):
    py_type = _simple_types.get(schema_type or "string")
    if py_type and not isinstance(value, py_type): raise ValidationError(f"{path} must be {schema_type}")
    if enum_values and value not in enum_values: raise ValidationError(f"{path} must be one of {', '.join(enum_values)}")


def _validate_schema_value(value, schema, schemas, path):
    if "$ref" in schema:
        target = schemas.get(schema["$ref"])
        if target is None: raise ValidationError(f"{path}: unknown schema ref {schema['$ref']}")
        return _validate_schema_value(value, target, schemas, path)
    schema_type = schema.get("type")
    if schema_type in _simple_types and not isinstance(value, _simple_types[schema_type]):
        raise ValidationError(f"{path} must be {schema_type}")
    if schema.get("enum") and value not in schema["enum"]:
        raise ValidationError(f"{path} must be one of {', '.join(schema['enum'])}")
    if schema_type == "array":
        item_schema = schema.get("items", {})
        for idx, item in enumerate(value): _validate_schema_value(item, item_schema, schemas, f"{path}[{idx}]")
        return
    props = schema.get("properties", {})
    required = schema.get("required", [])
    if schema_type == "object" or props:
        if not isinstance(value, dict): raise ValidationError(f"{path} must be object")
        for key in required:
            if key not in value: raise ValidationError(f"{path}.{key} is required")
        additional = schema.get("additionalProperties")
        for key, item in value.items():
            if key in props: _validate_schema_value(item, props[key], schemas, f"{path}.{key}")
            elif additional: _validate_schema_value(item, additional, schemas, f"{path}.{key}")
            elif props: raise ValidationError(f"{path}.{key} is not allowed")
