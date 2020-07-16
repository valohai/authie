from contextlib import contextmanager
from typing import Dict, Callable

import requests

from laituri.utils.retry import retry
from .docker_v1 import docker_v1_credential_manager


@contextmanager
def registry_credentials_callback_v1_credential_manager(
    *,
    image: str,
    registry_credentials: Dict,
    log_status: Callable
):
    docker_credentials = fetch_docker_credentials(registry_credentials['url'])
    with docker_v1_credential_manager(image=image, registry_credentials=docker_credentials, log_status=log_status):
        yield


@retry()
def fetch_docker_credentials(url: str) -> Dict:
    response = requests.post(url, timeout=15)
    response.raise_for_status()
    return response.json()
