import pytest

from laituri.utils.retry import retry


class TestRetry:

    @pytest.fixture(autouse=True)
    def disable_sleep(self, mocker):
        return mocker.patch('time.sleep')  # removes retry delays for testing

    def test_works_if_no_exception(self, mocker):
        my_action = mocker.Mock()

        @retry()
        def my_retryable_action():
            my_action()

        my_retryable_action()
        assert my_action.call_count == 1

    def test_default_attempt_count(self, mocker):
        my_action = mocker.Mock(side_effect=Exception('boom!'))

        @retry()
        def my_retryable_action():
            my_action()

        with pytest.raises(Exception, match='boom!'):
            my_retryable_action()

        assert my_action.call_count == 5


    def test_custom_attempt_count(self, mocker):
        my_action = mocker.Mock(side_effect=Exception('pow!'))

        @retry(tries=11)
        def my_retryable_action():
            my_action()

        with pytest.raises(Exception, match='pow!'):
            my_retryable_action()

        assert my_action.call_count == 11
