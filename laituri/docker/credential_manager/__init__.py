from typing import Optional

from laituri.docker.credential_manager.credential_managers import credential_managers
from laituri.docker.credential_manager.dummy import get_dummy_credential_manager
from laituri.types import CredentialManager, LogStatusCallable, RegistryCredentialsDict


def _noop_log_status(message: str) -> None:
    pass  # pragma: nocover


def get_credential_manager(
    *,
    image: str,
    registry_credentials: Optional[RegistryCredentialsDict] = None,
    log_status: LogStatusCallable = _noop_log_status,
    auth_tries: int = 5,
) -> CredentialManager:
    """
    Get a credential context manager object based on the registry credentials dictionary passed in.

    If registry credentials are missing or incomplete, will still trigger the wrapped action.
    If registry credentials are invalid, raises DockerLoginFailed.

    :param image: full Docker image name, including the registry domain and tag if applicable
    :param registry_credentials: optional {type, version, username, password} dict for registry login
    :param log_status: optional function to use for user-facing status logging
    :param auth_tries: number of times to try authentication in case it fails
    :raises DockerLoginFailed
    :return: ContextManager
    """
    if not isinstance(registry_credentials, dict):  # no credentials to manage
        return get_dummy_credential_manager()

    version = registry_credentials.get('version')
    credentials_type = str(registry_credentials.get('type'))
    manager = credential_managers.get((credentials_type, str(version)))
    if manager:
        return manager(
            image=image,
            registry_credentials=registry_credentials,
            log_status=log_status,
            auth_tries=auth_tries,
        )

    log_status(f'Unable to parse {credentials_type} version {version} registry credentials; upcoming action may fail.')
    return get_dummy_credential_manager()
