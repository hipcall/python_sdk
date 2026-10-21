import pytest

from hipcall_sdk.client import AsyncClient, Client
from hipcall_sdk.exceptions import (
    BadRequestException,
    HipcallAPIException,
    NotFoundException,
    UnauthorizedException,
    UnprocessableEntityException,
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


def test_client_custom_base_url():
    client = Client("dummy_api_key", base_url="https://use.hipcall.com")

    assert client.get_task_detail_url(5) == "https://use.hipcall.com/api/v3/tasks/5"


def test_client_session_sends_default_headers():
    client = Client("dummy_api_key")

    assert client.session.headers["Authorization"] == "Bearer dummy_api_key"


@pytest.mark.parametrize("content,expected", [(None, {}), ({"ok": 1}, {"ok": 1})])
def test_client_handle_response_no_content(content, expected):
    assert Client.handle_response(204, content) == expected


def test_build_params_drops_only_none_and_lowercases_bools():
    params = Client.build_params(a=None, b=False, c=True, d=0, e="", f="x")

    assert params == {"b": "false", "c": "true", "d": 0, "e": "", "f": "x"}


@pytest.mark.parametrize(
    "text,expected",
    [
        ("", None),
        ('{"data": 1}', {"data": 1}),
        ("<html>Bad Gateway</html>", {"raw": "<html>Bad Gateway</html>"}),
    ],
)
def test_load_json(text, expected):
    assert Client.load_json(text) == expected


@pytest.mark.parametrize(
    "exc,expected",
    [
        (
            BadRequestException(400, {"errors": {"detail": "Bad Request"}}),
            "Bad request: Bad Request",
        ),
        (BadRequestException(400, {"errors": "oops"}), "Bad request: oops"),
        (BadRequestException(400, None), "Bad request: None"),
        (
            UnprocessableEntityException(
                422, {"errors": {"name": ["can't be blank"], "email": ["is invalid"]}}
            ),
            "The request was unprocessable: Errors: "
            "name: can't be blank | email: is invalid",
        ),
        (
            UnprocessableEntityException(422, {"errors": {"detail": "Invalid"}}),
            "The request was unprocessable: Errors: detail: Invalid",
        ),
        (
            UnprocessableEntityException(422, None),
            "The request was unprocessable: Errors: None",
        ),
        (
            UnauthorizedException(401, None),
            "Invalid API key or unauthorized access",
        ),
        (NotFoundException(404, None), "The requested resource was not found"),
        (
            HipcallAPIException(500, {"raw": "boom"}),
            "Unexpected error. Status: 500, Content: {'raw': 'boom'}",
        ),
    ],
)
def test_exception_messages(exc, expected):
    assert str(exc) == expected


@pytest.mark.parametrize("status_code", [400, 401, 404, 422, 500])
def test_exception_is_hipcall_api_exception(status_code):
    with pytest.raises(HipcallAPIException) as exc_info:
        Client.handle_response(status_code, {"errors": {"detail": "x"}})

    assert exc_info.value.status_code == status_code
    assert exc_info.value.errors == {"detail": "x"}


@pytest.mark.asyncio
async def test_async_client_without_context_manager_raises_clear_error():
    client = AsyncClient("dummy_api_key")

    with pytest.raises(RuntimeError, match="async with"):
        await client.get_contact(1)


@pytest.mark.asyncio
async def test_async_client_context_manager_opens_and_closes_session():
    async with AsyncClient("dummy_api_key") as client:
        session = client.session
        assert not session.closed
        assert session.headers["Authorization"] == "Bearer dummy_api_key"

    assert session.closed
    with pytest.raises(RuntimeError):
        client.session
