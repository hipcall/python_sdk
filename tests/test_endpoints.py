from types import SimpleNamespace

import pytest

from hipcall_sdk.client import AsyncClient, Client
from hipcall_sdk.exceptions import NotFoundException
from hipcall_sdk.models import (
    CommentCreate,
    ContactCreate,
    TagCreate,
    TaskCreate,
    TaskUpdate,
)

BASE = "https://use.hipcall.com.tr"


class FakeSession:
    """Records the last request and returns a canned response."""

    def __init__(self, status=200, payload=None, text=""):
        self.status = status
        self.payload = payload if payload is not None else {}
        self.text = text
        self.calls = []

    def _respond(self, verb, url, **kwargs):
        self.calls.append((verb, url, kwargs))
        return SimpleNamespace(
            status_code=self.status,
            text=self.text,
            json=lambda: self.payload,
        )

    def get(self, url, **kwargs):
        return self._respond("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self._respond("POST", url, **kwargs)

    def patch(self, url, **kwargs):
        return self._respond("PATCH", url, **kwargs)

    def put(self, url, **kwargs):
        return self._respond("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        return self._respond("DELETE", url, **kwargs)


class FakeAsyncResponse:
    def __init__(self, status, payload, text):
        self.status = status
        self._payload = payload
        self._text = text

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def json(self):
        return self._payload

    async def text(self):
        return self._text


class FakeAsyncSession:
    def __init__(self, status=200, payload=None, text=""):
        self.status = status
        self.payload = payload if payload is not None else {}
        self.text = text
        self.calls = []

    def _respond(self, verb, url, **kwargs):
        self.calls.append((verb, url, kwargs))
        return FakeAsyncResponse(self.status, self.payload, self.text)

    def get(self, url, **kwargs):
        return self._respond("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self._respond("POST", url, **kwargs)

    def patch(self, url, **kwargs):
        return self._respond("PATCH", url, **kwargs)

    def delete(self, url, **kwargs):
        return self._respond("DELETE", url, **kwargs)


CONTACT = {"id": 1, "first_name": "John"}


def make_client(session):
    client = Client("dummy_api_key")
    client.session = session
    return client


def test_get_contact():
    session = FakeSession(payload={"data": CONTACT})
    result = make_client(session).get_contact(1)

    assert result.data.id == 1
    assert session.calls[0][:2] == ("GET", f"{BASE}/api/v3/contacts/1")


def test_get_contacts_params_drop_none():
    session = FakeSession(
        payload={"data": [CONTACT], "meta": {"count": 1, "limit": 5, "offset": 0}}
    )
    make_client(session).get_contacts(limit=5, q="john")

    params = session.calls[0][2]["params"]
    assert params == {"limit": 5, "offset": 0, "q": "john"}


def test_create_contact_sends_flat_body():
    session = FakeSession(payload={"data": CONTACT})
    make_client(session).create_contact(ContactCreate(first_name="John"))

    verb, url, kwargs = session.calls[0]
    assert (verb, url) == ("POST", f"{BASE}/api/v3/contacts")
    assert kwargs["json"] == {"first_name": "John"}


def test_create_task_wraps_body_in_data():
    session = FakeSession(payload={"data": {"id": 1, "name": "x", "done": False}})
    make_client(session).create_task(TaskCreate(name="x"))

    assert session.calls[0][2]["json"] == {"data": {"name": "x"}}


def test_update_task_uses_patch():
    session = FakeSession(payload={"data": {"id": 1, "name": "y", "done": True}})
    make_client(session).update_task(1, TaskUpdate(done=True))

    verb, url, kwargs = session.calls[0]
    assert (verb, url) == ("PATCH", f"{BASE}/api/v3/tasks/1")
    assert kwargs["json"] == {"done": True}


def test_get_calls_bracket_filters():
    session = FakeSession(
        payload={"data": [], "meta": {"count": 0, "limit": 10, "offset": 0}}
    )
    make_client(session).get_calls(missing_call=True, user_id=3)

    params = session.calls[0][2]["params"]
    assert params["missing_call[eq]"] == "true"
    assert params["user_id[eq]"] == 3
    assert "direction[eq]" not in params


def test_add_tag_to_call_sends_tag_id():
    session = FakeSession(
        payload={"data": {"id": 1, "name": "vip", "color": "red", "color_name": "red"}}
    )
    make_client(session).add_call_tag("abc", TagCreate(tag_id=1))

    verb, url, kwargs = session.calls[0]
    assert (verb, url) == ("POST", f"{BASE}/api/v3/calls/abc/tags")
    assert kwargs["json"] == {"tag_id": 1}


def test_comment_body_is_flat_for_contacts():
    session = FakeSession(payload={"data": {"id": 1, "content": "hi"}})
    make_client(session).create_contact_comment(1, CommentCreate(content="hi"))

    assert session.calls[0][2]["json"] == {"content": "hi"}


def test_lookup_by_phone_uses_number_param():
    session = FakeSession(payload={"data": {"contacts": [], "companies": []}})
    make_client(session).lookup_by_phone("+905326202911")

    assert session.calls[0][2]["params"] == {"number": "+905326202911"}


def test_delete_returns_none_on_204():
    session = FakeSession(status=204)
    result = make_client(session).delete_contact_tag(1, 2)

    assert result is None
    assert session.calls[0][:2] == ("DELETE", f"{BASE}/api/v3/contacts/1/tags/2")


def test_delete_raises_on_404():
    session = FakeSession(status=404, text='{"errors": {"detail": "Not Found"}}')

    with pytest.raises(NotFoundException):
        make_client(session).delete_contact_tag(1, 2)


@pytest.mark.asyncio
async def test_async_get_contact():
    client = AsyncClient("dummy_api_key")
    client.session = FakeAsyncSession(payload={"data": CONTACT})

    result = await client.get_contact(1)

    assert result.data.id == 1
    assert client.session.calls[0][:2] == ("GET", f"{BASE}/api/v3/contacts/1")


@pytest.mark.asyncio
async def test_async_delete_returns_none_on_204():
    client = AsyncClient("dummy_api_key")
    client.session = FakeAsyncSession(status=204)

    assert await client.delete_company_tag(1, 2) is None
    assert client.session.calls[0][:2] == (
        "DELETE",
        f"{BASE}/api/v3/companies/1/tags/2",
    )


@pytest.mark.asyncio
async def test_async_create_task_wraps_body_in_data():
    client = AsyncClient("dummy_api_key")
    client.session = FakeAsyncSession(
        payload={"data": {"id": 1, "name": "x", "done": False}}
    )

    await client.create_task(TaskCreate(name="x"))

    assert client.session.calls[0][2]["json"] == {"data": {"name": "x"}}
