from pathlib import Path

from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials

from fastgws.auth import gclientid_token, _refresh_error


def test_internal_gclientid_token():
    assert gclientid_token('J@Answer.AI').name == 'oauth-token-j@answer.ai.json'
    assert gclientid_token('J@Answer.AI', internal=True).name == 'oauth-token-j@answer.ai-internal.json'


def test_cloud_session_expiry_message():
    creds = Credentials(token='expired', account='j@answer.ai')
    creds.token_path = Path('oauth-token-j@answer.ai-internal.json')
    err = _refresh_error(creds, RefreshError('Reauthentication is needed.'))
    assert str(err) == ('Google Cloud session expired for j@answer.ai; run '
        '`gclientid-auth --internal --account j@answer.ai` to reauthenticate')
