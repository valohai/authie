import pytest

from laituri.utils.retry import make_retrying, retry


class TestRetry:

    @pytest.fixture(autouse=True)
    def disable_sleep(self, mocker):
        return mocker.patch('time.sleep')  # removes retry delays for testing

    def test_decorator_works(self, mocker):
        my_action = mocker.Mock()

        @retry()
        def my_retryable_action():
            my_action('AWESOME', a=1)

        my_retryable_action()
        my_action.assert_called_once_with('AWESOME', a=1)

    def test_decorator_default_tries(self, mocker):
        my_action = mocker.Mock(side_effect=Exception('boom!'))

        @retry()
        def my_retryable_action():
            my_action()

        with pytest.raises(Exception, match='boom!'):
            my_retryable_action()

        assert my_action.call_count == 5

    def test_decorator_custom_tries(self, mocker):
        my_action = mocker.Mock(side_effect=Exception('pow!'))

        @retry(tries=11)
        def my_retryable_action():
            my_action()

        with pytest.raises(Exception, match='pow!'):
            my_retryable_action()

        assert my_action.call_count == 11

    def test_wrapper_works(self, mocker):
        my_action = mocker.Mock()
        my_retrying_action = make_retrying(my_action)
        my_retrying_action('GREAT', b=2)
        my_action.assert_called_once_with('GREAT', b=2)

    def test_wrapper_default_tries(self, mocker):
        my_action = mocker.Mock(side_effect=Exception('bang!'))
        my_retrying_action = make_retrying(my_action)
        with pytest.raises(Exception, match='bang!'):
            my_retrying_action()
        assert my_action.call_count == 5

    def test_wrapper_custom_tries(self, mocker):
        my_action = mocker.Mock(side_effect=Exception('oof!'))
        my_retrying_action = make_retrying(my_action, tries=3)
        with pytest.raises(Exception, match='oof!'):
            my_retrying_action()
        assert my_action.call_count == 3
