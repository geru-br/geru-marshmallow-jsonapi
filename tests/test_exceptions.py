import pytest

from geru.marshmallow_jsonapi.exceptions import BaseApiException


class CustomException(BaseApiException):
    pass


class TestBaseApiException:
    def test_exception_message(self):
        message = 'Name is invalid'
        e = BaseApiException(message=message)
        assert e.message == {'error': message, 'status': 400}

    def test_status_code(self):
        message = 'Invalid credentials'
        e = BaseApiException(message=message, status=403)
        assert e.message == {'error': message, 'status': 403}


class TestCustomException:
    def test_exception(self):
        def raises_exception():
            raise CustomException(message='This is as exception', status=401)

        with pytest.raises(CustomException):
            raises_exception()
