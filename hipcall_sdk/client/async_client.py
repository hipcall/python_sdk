from typing import Optional

import aiohttp

from hipcall_sdk.client.base import HipcallBaseClient
from hipcall_sdk.models import (
    CallDetailResponse,
    CallListResponse,
    TaskListResponse,
    TaskCreate,
    TaskResponse,
    TaskDetailResponse,
    CallAndBridgeResponse,
)


class AsyncClient(HipcallBaseClient):
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        super().__init__(api_key, base_url)
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.get_default_headers())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_call(self, call_id: str, date: str) -> CallDetailResponse:
        url = self.get_call_detail_url(call_id)
        params = {"date": date}
        async with self.session.get(url, params=params) as response:
            content = await response.json()
            data = self.handle_response(response.status, content)
            return CallDetailResponse(**data)

    async def get_calls(
        self,
        limit: int = 10,
        offset: int = 0,
        q: Optional[str] = None,
        sort: str = "started_at.asc",
    ) -> CallListResponse:
        url = self.get_call_list_url()
        params = {"limit": limit, "offset": offset, "sort": sort}
        if q:
            params["q"] = q
        async with self.session.get(url, params=params) as response:
            content = await response.json()
            data = self.handle_response(response.status, content)
            return CallListResponse(**data)

    async def call_and_bridge(
        self,
        user_id: int,
        callee_number: str,
        ring_user_first: bool = True,
    ) -> CallAndBridgeResponse:
        url = self.get_call_and_bridge_url(user_id)
        data = {"callee_number": callee_number, "ring_user_first": ring_user_first}
        async with self.session.post(url, json=data) as response:
            content = await response.json()
            data = self.handle_response(response.status, content)
            return CallAndBridgeResponse(**data)

    async def get_tasks(
        self,
        limit: int = 10,
        offset: int = 0,
        q: Optional[str] = None,
        sort: str = "id.asc",
    ) -> TaskListResponse:
        url = self.get_task_list_url()
        params = {"limit": limit, "offset": offset, "sort": sort}
        if q:
            params["q"] = q
        async with self.session.get(url, params=params) as response:
            content = await response.json()
            data = self.handle_response(response.status, content)
            return TaskListResponse(**data)

    async def create_task(self, task: TaskCreate) -> TaskResponse:
        url = self.get_task_list_url()
        data = task.model_dump(exclude_unset=True)
        async with self.session.post(url, json=data) as response:
            content = await response.json()
            data = self.handle_response(response.status, content)
            return TaskResponse(**data)

    async def get_task(self, task_id: int) -> TaskDetailResponse:
        url = self.get_task_detail_url(task_id)
        async with self.session.get(url) as response:
            content = await response.json()
            data = self.handle_response(response.status, content)
            return TaskDetailResponse(**data)
