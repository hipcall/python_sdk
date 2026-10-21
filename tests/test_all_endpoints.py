"""Smoke-test every public endpoint method of Client and AsyncClient.

For each method we call it with sentinel arguments against a fake session
whose response is generated from the method's return model, then check that:

* the response parses into the annotated return type,
* the sync and async clients send exactly the same request,
* every required argument reaches the request (path, query or body),
* path arguments appear in the URL in the same order as in the signature.
"""

import inspect
import types
import typing
from datetime import date, datetime

import pytest
from pydantic import BaseModel

from hipcall_sdk.client import AsyncClient, Client
from hipcall_sdk.client.base import HipcallBaseClient
from tests.fakes import FakeAsyncSession, FakeSession

BASE = "https://use.hipcall.com.tr"

HELPERS = {
    name
    for name, member in inspect.getmembers(HipcallBaseClient)
    if not getattr(member, "__isabstractmethod__", False)
}

ENDPOINTS = sorted(
    name
    for name, _ in inspect.getmembers(Client, inspect.isfunction)
    if not name.startswith("_") and name not in HELPERS
)


def fake_value(tp):
    """Build a minimal valid JSON value for a type annotation."""
    origin, args = typing.get_origin(tp), typing.get_args(tp)
    if origin in (typing.Union, types.UnionType):
        return fake_value(next(a for a in args if a is not type(None)))
    if origin is list:
        return [fake_value(args[0])]
    if origin is dict:
        return {}
    if origin is typing.Literal:
        return args[0]
    if inspect.isclass(tp) and issubclass(tp, BaseModel):
        return {
            name: fake_value(field.annotation)
            for name, field in tp.model_fields.items()
            if field.is_required()
        }
    if tp is bool:
        return True
    if tp is int:
        return 1
    if tp is float:
        return 1.0
    if tp is datetime:
        return "2026-01-01T00:00:00Z"
    if tp is date:
        return "2026-01-01"
    return "x"


def build_args(method):
    """Required arguments: models get valid instances, scalars get sentinels."""
    hints = typing.get_type_hints(method)
    args, sentinels = [], []
    for i, param in enumerate(inspect.signature(method).parameters.values()):
        if param.name == "self" or param.default is not inspect.Parameter.empty:
            continue
        tp = hints[param.name]
        if typing.get_origin(tp) in (typing.Union, types.UnionType):
            tp = next(a for a in typing.get_args(tp) if a is not type(None))
        if inspect.isclass(tp) and issubclass(tp, BaseModel):
            args.append(tp(**fake_value(tp)))
        else:
            value = 9001 + i if tp is int else f"str{501 + i}"
            args.append(value)
            sentinels.append(str(value))
    return args, sentinels


def response_for(method):
    return_type = typing.get_type_hints(method)["return"]
    if return_type is type(None):
        return return_type, {"status": 204}
    return return_type, {"payload": fake_value(return_type)}


def test_endpoint_list_is_complete():
    assert len(ENDPOINTS) >= 100
    async_endpoints = {
        name
        for name, _ in inspect.getmembers(AsyncClient, inspect.isfunction)
        if not name.startswith("_") and name not in HELPERS
    }
    assert async_endpoints == set(ENDPOINTS)


@pytest.mark.asyncio
@pytest.mark.parametrize("name", ENDPOINTS)
async def test_endpoint(name):
    method = getattr(Client, name)
    args, sentinels = build_args(method)
    return_type, response = response_for(method)

    client = Client("dummy_api_key")
    client.session = FakeSession(**response)
    result = getattr(client, name)(*args)

    async_client = AsyncClient("dummy_api_key")
    async_client.session = FakeAsyncSession(**response)
    async_result = await getattr(async_client, name)(*args)

    # Response parses into the annotated type, identically on both clients.
    if return_type is type(None):
        assert result is None
    else:
        assert isinstance(result, return_type)
    assert async_result == result

    # Both clients send exactly one, identical request.
    assert len(client.session.calls) == 1
    assert async_client.session.calls == client.session.calls

    verb, url, kwargs = client.session.calls[0]
    assert verb in {"GET", "POST", "PATCH", "PUT", "DELETE"}
    assert url.startswith(f"{BASE}/api/v3/")
    assert "{" not in url and "None" not in url

    # Every scalar argument reaches the request, path ones in signature order.
    path = url.removeprefix(BASE)
    for value in sentinels:
        assert value in path or value in str(kwargs), f"{value} not sent"
    positions = [path.index(v) for v in sentinels if v in path]
    assert positions == sorted(positions)

    # Bodies are only sent by write requests.
    if verb in {"GET", "DELETE"}:
        assert "json" not in kwargs
