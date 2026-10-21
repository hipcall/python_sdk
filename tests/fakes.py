import json
from types import SimpleNamespace


def _body(payload, text):
    if text is not None:
        return text
    return json.dumps(payload) if payload is not None else ""


class FakeSession:
    """Records every request and returns a canned response."""

    def __init__(self, status=200, payload=None, text=None):
        self.status = status
        self.text = _body(payload, text)
        self.calls = []

    def _respond(self, verb, url, **kwargs):
        self.calls.append((verb, url, kwargs))
        return SimpleNamespace(status_code=self.status, text=self.text)

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
    def __init__(self, status, text):
        self.status = status
        self._text = text

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def text(self):
        return self._text


class FakeAsyncSession(FakeSession):
    """Async counterpart of FakeSession, usable with `async with`."""

    def _respond(self, verb, url, **kwargs):
        self.calls.append((verb, url, kwargs))
        return FakeAsyncResponse(self.status, self.text)
