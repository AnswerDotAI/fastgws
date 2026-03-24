from fastgws.build import build_all, check_generated
from fastgws.build.manifest import fixture_path, load_manifest


def test_manifest_and_fixtures_exist():
    manifest = load_manifest()
    assert [o.alias for o in manifest][:4] == ["drive", "gmail", "sheets", "keep"]
    for entry in manifest: assert fixture_path(entry).exists()


def test_build_outputs_exist():
    services = build_all()
    assert services
    check_generated()
