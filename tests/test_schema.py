import pytest

from fastgws.core import FastGWS
from fastgws.errors import ValidationError


def test_validation_and_schema_resolution():
    api = FastGWS.from_fixture()
    method = api.resolve_endpoint("drive.files.create")
    schema = api.schema("drive.files.create", resolve_refs=True)
    assert schema["requestBody"]["schema"]["type"] == "object"
    with pytest.raises(ValidationError): method(body={"name": "x"}, not_a_param=1)


def test_nested_body_validation():
    api = FastGWS.from_fixture(transport=None)
    method = api.resolve_endpoint("gmail.users.messages.send")
    with pytest.raises(ValidationError): method(user_id="me", body="not a dict", validate=True)
