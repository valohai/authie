from laituri.utils.images import get_image_hostname


def test_get_image_hostname():
    assert get_image_hostname("python:3.6") == "docker.io"
    assert get_image_hostname("tensorflow/tensorflow:latest") == "docker.io"
    assert get_image_hostname("docker.io/tensorflow/tensorflow:latest") == "docker.io"
    assert get_image_hostname("my.io/tensorflow:latest") == "my.io"
    assert get_image_hostname("localhost:500/tensorflow:latest") == "localhost:500"
    assert get_image_hostname("gcr.io/google-containers/busybox:latest") == "gcr.io"
