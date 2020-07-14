import pytest

from laituri.docker.credential_manager import get_credential_manager
from laituri_tests.mock_data import EXAMPLE_IMAGES


@pytest.mark.parametrize('image', EXAMPLE_IMAGES)
def test_that_context_manager_triggers_the_action_regardless_of_image_validity(mocker, image: str):
    my_action = mocker.Mock()
    with get_credential_manager(image=image):
        my_action()
    my_action.assert_called_once_with()
