from typing import Optional

from requests import RequestException, Response


class DockerLoginFailed(Exception):
    """We failed to login to Docker from some reason."""

    pass


class InvalidDockerCommand(Exception):
    """The Docker command is misconfigured."""


class CallbackFailed(Exception):
    """
    Calling a registry credentials callback failed.
    """

    def get_callback_response(self) -> Optional[Response]:
        """
        Attempt to reach into the inner exception to get the response object returned by the callback.
        """
        if isinstance(self.__cause__, RequestException):
            response = self.__cause__.response
            if isinstance(response, Response):
                return response
        return None
