from fastgws.core import FastGWS
from fastgws.transport import compose_request, render_path_template


def test_compose_request_handles_upload_and_media_download():
    api = FastGWS.from_fixture()
    getattr(api, "drive")
    drive_service = api._services["drive"].service
    drive_method = api.resolve_endpoint("drive.files.create")._method
    spec = compose_request(drive_service, drive_method, {"supportsAllDrives": True}, body={"name": "x"}, upload=b"abc", upload_content_type="text/plain")
    assert spec.url == "https://www.googleapis.com/upload/drive/v3/files"
    assert ("supportsAllDrives", "true") in spec.query
    assert ("uploadType", "multipart") in spec.query
    assert spec.data is not None

    getattr(api, "keep")
    keep_method = api.resolve_endpoint("keep.notes.get")._method
    keep_spec = compose_request(api._services["keep"].service, keep_method, {"name": "notes/abc"}, download=True)
    assert keep_spec.url == "https://keep.googleapis.com/v1/notes/abc"
    assert ("alt", "media") in keep_spec.query


def test_render_path_template_preserves_slashes_for_plus_params():
    assert render_path_template("v1/{+name}", {"name": "notes/abc"}) == "v1/notes/abc"
