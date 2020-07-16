import pytest
from unittest.mock import patch

import requests

from laituri.docker.credential_manager import get_credential_manager
from laituri_tests.mock_data import EXAMPLE_IMAGES
from laituri_tests.mock_process import create_mock_popen
from .test_docker_v1 import VALID_DOCKER_CREDENTIALS

VALID_CALLBACK_CREDENTIALS = {
    'version': 1,
    'type': 'registry-credentials-callback',
    'url': 'https://example.com/?name=erkki',
}
VALID_CALLBACK_RESPONSE = VALID_DOCKER_CREDENTIALS


@patch.dict(VALID_CALLBACK_CREDENTIALS)
@pytest.mark.parametrize('image', EXAMPLE_IMAGES)
def test_callback_retry(mocker, requests_mock, image: str):
    requests_mock.post(
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
    with get_credential_manager(image=image, registry_credentials=VALID_CALLBACK_CREDENTIALS):
        my_action()
    assert mock_popen.call_count == 2  # login + logout
    my_action.assert_called_once_with()
