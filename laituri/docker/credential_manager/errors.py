class DockerLoginFailed(Exception):
    """We failed to login to Docker from some reason."""

    pass


class InvalidDockerCommand(Exception):
    """The Docker command is misconfigured."""
