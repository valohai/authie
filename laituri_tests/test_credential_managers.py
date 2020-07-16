from typing import Dict
from unittest.mock import patch

import pytest

from laituri.docker.credential_manager import get_credential_manager
from laituri_tests.mock_data import EXAMPLE_IMAGES
from laituri_tests.mock_process import create_mock_popen
from laituri_tests.test_docker_v1 import VALID_DOCKER_CREDENTIALS
from laituri_tests.test_registry_credentials_callback_v1 import VALID_CALLBACK_CREDENTIALS, VALID_CALLBACK_RESPONSE


@pytest.mark.parametrize('image', EXAMPLE_IMAGES)
def test_that_context_manager_triggers_the_action_regardless_of_image_validity(mocker, image: str):
    my_action = mocker.Mock()
    with get_credential_manager(image=image):
        my_action()
    my_action.assert_called_once_with()


@patch.dict(VALID_DOCKER_CREDENTIALS)
@pytest.mark.parametrize('image', EXAMPLE_IMAGES)
@pytest.mark.parametrize('credentials', (VALID_DOCKER_CREDENTIALS, VALID_CALLBACK_CREDENTIALS))
def test_login_with_valid_credentials(mocker, requests_mock, image: str, credentials: Dict):
    # smoke test for all credential types
    my_action = mocker.Mock()
    mock_popen = mocker.patch('subprocess.Popen', new_callable=create_mock_popen)
    if credentials == VALID_CALLBACK_CREDENTIALS:
        requests_mock.post(VALID_CALLBACK_CREDENTIALS['url'], json=VALID_CALLBACK_RESPONSE)
    with get_credential_manager(image=image, registry_credentials=credentials):
        assert mock_popen.call_count == 1  # login
        my_action()
    assert mock_popen.call_count == 2  # login + logout
    my_action.assert_called_once_with()
