import pytest
from hipcall_sdk.client import Client
from hipcall_sdk.exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
    UnprocessableEntityException,
    HipcallAPIException,
)


def test_client_api_key_required():
    # Act & Assert
    with pytest.raises(ValueError):
        Client("")


def test_client_base_url_defaults():
    # Arrange
    client = Client("dummy_api_key")

    # Assert
    assert client.base_url == "https://use.hipcall.com.tr"



def test_client_default_headers():
    # Arrange
    client = Client("dummy_api_key")

    # Act
    headers = client.get_default_headers()

    # Assert
    assert headers == {
        "Authorization": "Bearer dummy_api_key",
        "Content-Type": "application/json",
    }


@pytest.mark.parametrize(
    "status_code",
    [200, 201],
)
def test_client_handle_response_success(status_code):
    # Arrange
    client = Client("dummy_api_key")

    # Act
    result = client.handle_response(status_code, {"data": "foobar"})

    # Assert
    assert result == {"data": "foobar"}


@pytest.mark.parametrize(
    "status_code,exc_class",
    [
        (400, BadRequestException),
        (401, UnauthorizedException),
        (404, NotFoundException),
        (422, UnprocessableEntityException),
        (500, HipcallAPIException),
        (503, HipcallAPIException),
    ],
)
def test_client_handle_response_fail(status_code, exc_class):
    # Arrange
    client = Client("dummy_api_key")

    # Act & Assert
    with pytest.raises(exc_class):
        client.handle_response(status_code, {"data": "foobar"})
