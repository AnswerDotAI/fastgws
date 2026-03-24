# fastgws

A modern Python package scaffolded by **fastship**.

## Development

```bash
pip install -e .[dev]
```

## Versioning

Version lives in `fastgws/__init__.py` as `__version__`.
Bump it with:

```bash
ship_bump --part 2   # patch
ship_bump --part 1   # minor
ship_bump --part 0   # major
```

## Release

1) Ensure your GitHub issues are labeled (`bug`, `enhancement`, `breaking`).
2) Run:

```bash
ship_release_gh
ship_pypi
```
