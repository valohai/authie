from contextlib import contextmanager
from typing import Callable, Dict

import requests
from requests.utils import default_headers

import laituri
from laituri.docker.credential_manager.docker_v1 import docker_v1_credential_manager
from laituri.utils.retry import retry


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
    headers = default_headers()
    headers['User-Agent'] = f'{headers.get("User-Agent")} laituri/{laituri.__version__}'
    response = requests.post(url, timeout=15, headers=headers)
    response.raise_for_status()
    return response.json()
