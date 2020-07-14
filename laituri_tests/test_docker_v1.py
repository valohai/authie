import subprocess
from unittest.mock import patch

import pytest

from laituri.docker.credential_manager import get_credential_manager
from laituri.docker.credential_manager.errors import DockerLoginFailed
from laituri_tests.mock_process import create_mock_popen, create_mock_process
from laituri_tests.mock_data import EXAMPLE_IMAGES

VALID_DOCKER_CREDENTIALS = {
    'type': 'docker',
    'version': '1',
    'username': 'edward',
    'password': 'scissors123'
}


@patch.dict(VALID_DOCKER_CREDENTIALS)
@pytest.mark.parametrize('image', EXAMPLE_IMAGES)
def test_login_with_valid_credentials(mocker, image: str):
    my_action = mocker.Mock()
    mock_popen = mocker.patch('subprocess.Popen', new_callable=create_mock_popen)
    with get_credential_manager(image=image, registry_credentials=VALID_DOCKER_CREDENTIALS):
        assert mock_popen.call_count == 1  # login
        my_action()
    assert mock_popen.call_count == 2  # login + logout
    my_action.assert_called_once_with()


@patch.dict(VALID_DOCKER_CREDENTIALS)
def test_login_timeout(mocker):
    my_action = mocker.Mock()
    image = EXAMPLE_IMAGES[0]

    def popen_mock(args, **kwargs):
        # force the login processes to raise TimeoutExpired
        if args[2] == 'login':
            mock_process = create_mock_process()
            mock_process.communicate.side_effect = subprocess.TimeoutExpired(cmd='docker login', timeout=30)
            return mock_process
        return create_mock_process()

    mocker.patch('subprocess.Popen', wraps=popen_mock)
    with pytest.raises(DockerLoginFailed):
        with get_credential_manager(image=image, registry_credentials=VALID_DOCKER_CREDENTIALS):
            my_action()
    my_action.assert_not_called()


@patch.dict(VALID_DOCKER_CREDENTIALS)
def test_login_error(mocker):
    my_action = mocker.Mock()
    image = EXAMPLE_IMAGES[0]

    # make the mock subprocess to report non-zero return code
    mock_popen = mocker.patch('subprocess.Popen')
    mock_process = create_mock_process(returncode=1)
    mock_popen.return_value = mock_process

    with pytest.raises(DockerLoginFailed):
        with get_credential_manager(image=image, registry_credentials=VALID_DOCKER_CREDENTIALS):
            my_action()
    my_action.assert_not_called()


@patch.dict(VALID_DOCKER_CREDENTIALS)
def test_that_logout_error_doesnt_crash(mocker):
    my_action = mocker.Mock()
    image = EXAMPLE_IMAGES[0]
    mocker.patch('subprocess.Popen', new_callable=create_mock_popen)

    def check_call_mock(args, **kwargs):
        # force logout processes to error out
        if args[2] == 'logout':
            raise subprocess.CalledProcessError(returncode=1, cmd='docker logout', output=b'')
        return create_mock_process()

    mock_check_call = mocker.patch('subprocess.check_call', wraps=check_call_mock)

    with get_credential_manager(image=image, registry_credentials=VALID_DOCKER_CREDENTIALS):
        my_action()
    assert mock_check_call.call_count == 1
    my_action.assert_called_once_with()


@patch.dict(VALID_DOCKER_CREDENTIALS)
@pytest.mark.parametrize('missing_value', ('type', 'version'))
def test_fallback_with_invalid_credential_configuration(mocker, missing_value):
    # when type or version is missing, we should fallback to dummy manager and do the action anyway, but with a warning
    del VALID_DOCKER_CREDENTIALS[missing_value]
    image = EXAMPLE_IMAGES[0]
    my_action = mocker.Mock()
    my_logging_callback = mocker.Mock()
    with get_credential_manager(image=image, registry_credentials=VALID_DOCKER_CREDENTIALS,
                                log_status=my_logging_callback):
        my_action()

    my_action.assert_called_once_with()
    assert 'Unable to parse' in my_logging_callback.call_args[0][0]


@patch.dict(VALID_DOCKER_CREDENTIALS)
def test_changing_settings(mocker):
    my_action = mocker.Mock()

    # accept all subprocess calls that use the default 'docker' command
    mocker.patch(
        'subprocess.Popen',
        wraps=lambda args, **kwargs: create_mock_process() if args[1] == 'docker' else None,
    )
    with get_credential_manager(image=EXAMPLE_IMAGES[0], registry_credentials=VALID_DOCKER_CREDENTIALS):
        my_action()
    my_action.call_count = 1

    # modify the settings and accept only subprocess calls that use the modified command
    custom_command = 'modified-docker'
    mocker.patch('laituri.settings.DOCKER_COMMAND', custom_command)
    mocker.patch(
        'subprocess.Popen',
        wraps=lambda args, **kwargs: create_mock_process() if args[1] == custom_command else None
    )
    with get_credential_manager(image=EXAMPLE_IMAGES[0], registry_credentials=VALID_DOCKER_CREDENTIALS):
        my_action()
    my_action.call_count = 2
