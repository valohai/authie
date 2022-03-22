from typing import Any, Dict

import pytest
import requests

from laituri.docker.credential_manager import get_credential_manager
from laituri_tests.mock_data import EXAMPLE_IMAGES
from laituri_tests.mock_process import create_mock_popen

from .test_docker_v1 import VALID_DOCKER_CREDENTIALS

VALID_CALLBACK_CREDENTIALS: Dict[str, Any] = {
    'version': 1,
    'type': 'registry-credentials-callback',
    'url': 'https://example.com/?name=erkki',
}
VALID_CALLBACK_RESPONSE = VALID_DOCKER_CREDENTIALS


@pytest.mark.parametrize('image', EXAMPLE_IMAGES)
@pytest.mark.parametrize('with_header', (False, True))
def test_callback_retry(mocker, requests_mock, with_header: bool, image: str):
    registry_credentials = VALID_CALLBACK_CREDENTIALS.copy()
    if with_header:
        registry_credentials['headers'] = {
            'x-hello': 'there',
            '': 0,
        }
    rh = requests_mock.post(
        VALID_CALLBACK_CREDENTIALS['url'],
        [
            {'status_code': 404},
            {'status_code': 500},
            {'exc': requests.exceptions.ConnectTimeout},
            {'status_code': 200},  # no JSON
            {'status_code': 200, 'json': VALID_CALLBACK_RESPONSE}
        ]
    )
    mock_popen = mocker.patch('subprocess.Popen', new_callable=create_mock_popen)
    mocker.patch('time.sleep')  # removes retry delays for testing
    my_action = mocker.Mock()
    with get_credential_manager(image=image, registry_credentials=registry_credentials):
        my_action()
    assert mock_popen.call_count == 2  # login + logout
    my_action.assert_called_once_with()
    headers = rh.request_history[-1].headers
    assert 'laituri/' in headers['user-agent']
    assert ('x-hello' in headers) == with_header
