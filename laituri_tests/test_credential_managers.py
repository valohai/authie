import subprocess
from unittest.mock import patch

import pytest

from laituri.docker.credential_manager import get_credential_manager
from laituri.docker.credential_manager.errors import DockerLoginFailed

from .mock_process import create_mock_popen, create_mock_process

example_images = (
    'docker.io/owner/project:tag',
    'docker.io/owner/project',
    'owner/project:tag',
    'owner/project',
    'example.com/owner/project:tag',
    'example.com/owner/project',
)
example_credentials = {
    'type': 'docker',
    'version': '1',
    'username': 'edward',
    'password': 'scissors123'
}


@pytest.mark.parametrize('image', example_images)
def test_that_context_manager_triggers_the_action_regardless_of_image_validity(mocker, image: str):
    my_action = mocker.Mock()
    with get_credential_manager(image=image):
        my_action()
    my_action.assert_called_once_with()


@patch.dict(example_credentials)
@pytest.mark.parametrize('image', example_images)
def test_login_with_valid_credentials(mocker, image: str):
    my_action = mocker.Mock()
    mock_popen = mocker.patch('subprocess.Popen', new_callable=create_mock_popen)
    with get_credential_manager(image=image, registry_credentials=example_credentials):
        assert mock_popen.call_count == 1  # login
        my_action()
    assert mock_popen.call_count == 2  # login + logout
    my_action.assert_called_once_with()


@patch.dict(example_credentials)
def test_login_timeout(mocker):
    my_action = mocker.Mock()
    image = example_images[0]

    def popen_mock(args, **kwargs):
        # force the login processes to raise TimeoutExpired
        if args[2] == 'login':
            mock_process = create_mock_process()
            mock_process.communicate.side_effect = subprocess.TimeoutExpired(cmd='docker login', timeout=30)
            return mock_process
        return create_mock_process()

    mocker.patch('subprocess.Popen', wraps=popen_mock)
    with pytest.raises(DockerLoginFailed):
        with get_credential_manager(image=image, registry_credentials=example_credentials):
            my_action()
    my_action.assert_not_called()


@patch.dict(example_credentials)
def test_login_error(mocker):
    my_action = mocker.Mock()
    image = example_images[0]

    # make the mock subprocess to report non-zero return code
    mock_popen = mocker.patch('subprocess.Popen')
    mock_process = create_mock_process(returncode=1)
    mock_popen.return_value = mock_process

    with pytest.raises(DockerLoginFailed):
        with get_credential_manager(image=image, registry_credentials=example_credentials):
            my_action()
    my_action.assert_not_called()


@patch.dict(example_credentials)
def test_that_logout_error_doesnt_crash(mocker):
    my_action = mocker.Mock()
    image = example_images[0]
    mocker.patch('subprocess.Popen', new_callable=create_mock_popen)

    def check_call_mock(args, **kwargs):
        # force logout processes to error out
        if args[2] == 'logout':
            raise subprocess.CalledProcessError(returncode=1, cmd='docker logout', output=b'')
        return create_mock_process()

    mock_check_call = mocker.patch('subprocess.check_call', wraps=check_call_mock)

    with get_credential_manager(image=image, registry_credentials=example_credentials):
        my_action()
    assert mock_check_call.call_count == 1
    my_action.assert_called_once_with()


@patch.dict(example_credentials)
@pytest.mark.parametrize('missing_value', ('type', 'version'))
def test_fallback_with_invalid_credential_configuration(mocker, missing_value):
    # when type or version is missing, we should fallback to dummy manager and do the action anyway, but with a warning
    del example_credentials[missing_value]
    image = example_images[0]
    my_action = mocker.Mock()
    my_logging_callback = mocker.Mock()
    with get_credential_manager(image=image, registry_credentials=example_credentials, log_status=my_logging_callback):
        my_action()

    my_action.assert_called_once_with()
    assert 'Unable to parse' in my_logging_callback.call_args[0][0]
