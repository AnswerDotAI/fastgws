import inspect

from fastgws.core import FastGWS


def test_runtime_tree_and_repr():
    api = FastGWS.from_fixture()
    assert "drive" in dir(api)
    assert "files" in dir(api.drive)
    assert "list" in dir(api.drive.files)
    assert "messages" in dir(api.gmail.users)
    assert "list" in api.drive.files._repr_markdown_()


def test_generated_signature_and_schema_property():
    api = FastGWS.from_fixture()
    sig = inspect.signature(api.sheets.spreadsheets.values.update)
    text = str(sig)
    assert "spreadsheet_id" in text
    assert "range" in text
    assert "value_input_option" in text
    assert "body=None" in text
    schema = api.drive.files.create.schema
    assert schema["requestBody"]["schemaRef"] == "File"
