from __future__ import annotations

import json, sys

from .auth import login_and_save, parse_scopes
from .core import FastGWS
from .errors import ValidationError
from .generated.registry import REGISTRY
from .helpers import parse_cli_value


def main(argv=None):
    argv = list(argv or sys.argv[1:])
    api = FastGWS()
    if not argv:
        print("usage: fastgws <services|schema|docs|endpoint>")
        return 0
    cmd = argv.pop(0)
    if cmd == "auth": return _auth_main(argv)
    if cmd == "services":
        for name, meta in sorted(REGISTRY.items()): print(f"{name}\t{meta['description']}")
        return 0
    if cmd == "schema":
        print(json.dumps(api.schema(argv[0], resolve_refs="--resolve-refs" in argv[1:]), indent=2, sort_keys=True))
        return 0
    if cmd == "docs":
        target = api.resolve_endpoint(argv[0])
        print(target.__doc__)
        return 0
    target = api.resolve_endpoint(cmd)
    pos, kw = _parse_args(argv)
    if kw.pop("help", False):
        print(f"{cmd}{target.signature}")
        print(target.__doc__)
        return 0
    result = target(*pos, **kw)
    if isinstance(result, (dict, list)): print(json.dumps(result, indent=2, sort_keys=True))
    else: print(result)
    return 0


def _parse_args(argv):
    pos, kw = [], {}
    idx = 0
    while idx < len(argv):
        item = argv[idx]
        if item.startswith("--"):
            key = item[2:]
            if idx + 1 < len(argv) and not argv[idx + 1].startswith("--"):
                idx += 1
                kw[key] = parse_cli_value(argv[idx])
            else: kw[key] = True
        else: pos.append(parse_cli_value(item))
        idx += 1
    return pos, kw


def _auth_main(argv):
    if not argv: raise ValidationError("usage: fastgws auth login [--client-secret PATH] [--scopes scope1,scope2]")
    cmd = argv.pop(0)
    if cmd != "login": raise ValidationError(f"unknown auth command: {cmd}")
    _pos, kw = _parse_args(argv)
    _creds, secret_path, creds_path = login_and_save(client_secret=kw.get("client-secret"), scopes=kw.get("scopes"))
    data = dict(status="success", client_secret_file=str(secret_path), credentials_file=str(creds_path), scopes=parse_scopes(kw.get("scopes")), type="authorized_user")
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__": raise SystemExit(main())
