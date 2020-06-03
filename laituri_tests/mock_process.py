from typing import ByteString
from unittest.mock import Mock


def create_mock_popen():
    """Create a general mock Popen function that succeeds on all known subprocess calls."""

    def popen_mock(args, **kwargs):
        # make all known call types automatically succeed
        if args[1] == 'docker' and (args[2] == 'login' or args[2] == 'logout'):
            return create_mock_process()
        raise NotImplementedError('not sure how to mock this process')

    mock = Mock(wraps=popen_mock)
    return mock


def create_mock_process(
    returncode: int = 0,
    stdout: ByteString = b'success',
    stderr: ByteString = b'',
):
    """
    Create a mock Popen process for later inspection.

    Defaults to a successfully ran process.

    :param returncode: what the process will return
    :param stdout: what the process will write to STDOUT
    :param stderr: what the process will write to STDERR
    :return: the mock
    """
    mock = Mock()
    mock.poll = returncode
    mock.wait = lambda: None
    mock.kill = lambda: None
    mock.__enter__ = Mock(return_value=mock)
    mock.__exit__ = Mock()
    mock.returncode = returncode
    mock.communicate = Mock(return_value=(stdout, stderr))
    return mock
