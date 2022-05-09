from laituri.utils.images import get_image_domain


def test_get_image_domain():
    assert get_image_domain("python:3.6") == "docker.io"
    assert get_image_domain("gcr.io/google-containers/busybox:latest") == "gcr.io"
