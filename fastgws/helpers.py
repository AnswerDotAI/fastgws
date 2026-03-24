from __future__ import annotations

from collections.abc import Mapping
from keyword import iskeyword
from pathlib import Path
import json, re

_rx1 = re.compile(r"(.)([A-Z][a-z]+)")
_rx2 = re.compile(r"([a-z0-9])([A-Z])")
_unsafe = re.compile(r"[^0-9a-zA-Z_]")


class AttrDict(dict):
    def __getattr__(self, key):
        try: return self[key]
        except KeyError as exc: raise AttributeError(key) from exc

    def __setattr__(self, key, value): self[key] = value

    def __dir__(self):
        keys = [k for k in self if isinstance(k, str) and k.isidentifier()]
        return sorted(set(super().__dir__() + keys))


def dict_to_obj(value):
    if isinstance(value, Mapping): return AttrDict({k: dict_to_obj(v) for k, v in value.items()})
    if isinstance(value, list): return [dict_to_obj(v) for v in value]
    return value


def to_snake(name: str) -> str:
    name = name.replace("-", "_").replace(".", "_")
    name = _rx1.sub(r"\1_\2", name)
    name = _rx2.sub(r"\1_\2", name)
    name = _unsafe.sub("_", name).strip("_").lower() or "value"
    if name[0].isdigit(): name = f"n_{name}"
    if iskeyword(name): name = f"{name}_"
    return name


def unique_name(name: str, seen: set[str]) -> str:
    base = name
    idx = 2
    while name in seen:
        name = f"{base}_{idx}"
        idx += 1
    seen.add(name)
    return name


def title_case(name: str) -> str: return "".join(part.capitalize() for part in name.split("_"))


def project_root(start: str | Path | None = None) -> Path:
    path = Path(start or __file__).resolve()
    for parent in [path] + list(path.parents):
        if (parent / "pyproject.toml").exists(): return parent
    raise FileNotFoundError("pyproject.toml not found")


def compact_json(value) -> str: return json.dumps(value, sort_keys=True, separators=(",", ":"))


def parse_cli_value(value: str):
    lower = value.lower()
    if lower in {"true", "false", "null"}: return json.loads(lower)
    if value.startswith(("{", "[")) or value.startswith('"'):
        try: return json.loads(value)
        except json.JSONDecodeError: return value
    if re.fullmatch(r"-?\d+", value): return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value): return float(value)
    return value
