from laituri.utils.images import get_image_domain


def test_get_image_domain():
    assert get_image_domain("python:3.6") == "docker.io"
    assert get_image_domain("tensorflow/tensorflow:latest") == "docker.io"
    assert get_image_domain("docker.io/tensorflow/tensorflow:latest") == "docker.io"
    assert get_image_domain("my.io/tensorflow:latest") == "my.io"
    assert get_image_domain("localhost:500/tensorflow:latest") == "localhost:500"
    assert get_image_domain("gcr.io/google-containers/busybox:latest") == "gcr.io"
