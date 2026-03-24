from fastgws.build.manifest import fixture_path, load_manifest
from fastgws.build.normalize import load_fixture_doc, normalize_service


def test_normalize_drive_and_gmail_methods():
    entries = {o.alias: o for o in load_manifest()}
    drive = normalize_service(entries["drive"], load_fixture_doc(fixture_path(entries["drive"])))
    gmail = normalize_service(entries["gmail"], load_fixture_doc(fixture_path(entries["gmail"])))
    methods = {o.dotted_path for o in drive.methods}
    assert "drive.files.list" in methods
    assert "drive.files.create" in methods
    assert "drive.permissions.create" in methods
    gmail_methods = {o.dotted_path for o in gmail.methods}
    assert "gmail.users.messages.get" in gmail_methods
    assert "gmail.users.messages.send" in gmail_methods


def test_normalize_names_to_snake_case():
    entry = next(o for o in load_manifest() if o.alias == "sheets")
    service = normalize_service(entry, load_fixture_doc(fixture_path(entry)))
    method = next(o for o in service.methods if o.dotted_path == "sheets.spreadsheets.values.update")
    names = {o.py_name for o in method.query_params}
    assert "value_input_option" in names
