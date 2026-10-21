import pytest

from hipcall_sdk.client import AsyncClient, Client
from hipcall_sdk.exceptions import HipcallAPIException, NotFoundException
from hipcall_sdk.models import (
    CommentCreate,
    ContactCreate,
    DispositionUpdate,
    TagCreate,
    TaskCreate,
    TaskUpdate,
)
from tests.fakes import FakeAsyncSession, FakeSession

BASE = "https://use.hipcall.com.tr"


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


def test_get_contacts_parses_meta():
    session = FakeSession(
        payload={"data": [CONTACT], "meta": {"count": 42, "limit": 5, "offset": 10}}
    )
    result = make_client(session).get_contacts(limit=5, offset=10)

    assert result.meta.count == 42
    assert result.meta.offset == 10
    assert result.data[0].first_name == "John"


def test_get_call_sends_date_param():
    session = FakeSession(
        payload={
            "data": {
                "uuid": "abc",
                "started_at": "2026-10-21T09:00:00Z",
                "ended_at": "2026-10-21T09:01:00Z",
                "direction": "inbound",
            }
        }
    )
    result = make_client(session).get_call("abc", "2026-10-21")

    verb, url, kwargs = session.calls[0]
    assert (verb, url) == ("GET", f"{BASE}/api/v3/calls/abc")
    assert kwargs["params"] == {"date": "2026-10-21"}
    assert result.data.started_at.year == 2026


def test_call_and_bridge_minimal_body():
    session = FakeSession(payload={"data": {"id": "xyz"}})
    result = make_client(session).call_and_bridge(3, "905326202911")

    verb, url, kwargs = session.calls[0]
    assert (verb, url) == ("POST", f"{BASE}/api/v3/users/3/call")
    assert kwargs["json"] == {"callee_number": "905326202911", "ring_user_first": True}
    assert result.data.id == "xyz"


def test_call_and_bridge_optional_fields():
    session = FakeSession(payload={"data": {"id": "xyz"}})
    make_client(session).call_and_bridge(
        3,
        "905326202911",
        ring_user_first=False,
        call_masking=False,
        call_masking_name="Support",
    )

    assert session.calls[0][2]["json"] == {
        "callee_number": "905326202911",
        "ring_user_first": False,
        "call_masking": False,
        "call_masking_name": "Support",
    }


@pytest.mark.parametrize("status", [500, 502])
@pytest.mark.parametrize("text", ["<html>Bad Gateway</html>", ""])
def test_non_json_error_body_raises_api_exception(status, text):
    session = FakeSession(status=status, text=text)

    with pytest.raises(HipcallAPIException) as exc_info:
        make_client(session).get_contact(1)

    assert exc_info.value.status_code == status
    assert str(exc_info.value)


@pytest.mark.asyncio
async def test_async_non_json_error_body_raises_api_exception():
    client = AsyncClient("dummy_api_key")
    client.session = FakeAsyncSession(status=502, text="<html>Bad Gateway</html>")

    with pytest.raises(HipcallAPIException) as exc_info:
        await client.get_contact(1)

    assert exc_info.value.content == {"raw": "<html>Bad Gateway</html>"}


@pytest.mark.asyncio
async def test_async_set_call_disposition_uses_put():
    client = AsyncClient("dummy_api_key")
    client.session = FakeAsyncSession(
        payload={"data": {"editable": True, "edit_window_minutes": 30}}
    )

    result = await client.set_call_disposition(
        "abc", DispositionUpdate(disposition_id=7)
    )

    verb, url, kwargs = client.session.calls[0]
    assert (verb, url) == ("PUT", f"{BASE}/api/v3/calls/abc/disposition")
    assert kwargs["json"] == {"disposition_id": 7}
    assert result.data.editable is True
