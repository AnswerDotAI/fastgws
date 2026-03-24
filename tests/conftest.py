from __future__ import annotations

import pytest

from fastgws.build import build_all
from fastgws.helpers import project_root


@pytest.fixture(scope="session", autouse=True)
def _build_generated():
    build_all()
    return True


@pytest.fixture(scope="session")
def root(): return project_root()


@pytest.fixture(scope="session")
def fixtures_dir(root): return root / "tests" / "fixtures" / "discovery"


@pytest.fixture
def tmp_download(tmp_path): return tmp_path / "download.bin"
