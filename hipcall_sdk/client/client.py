from typing import Optional

import requests

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


class Client(HipcallBaseClient):
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        super().__init__(api_key, base_url)
        self.session = requests.Session()
        self.session.headers.update(self.get_default_headers())

    def get_call(self, call_id: str, date: str) -> CallDetailResponse:
        url = self.get_call_detail_url(call_id)
        params = {"date": date}
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return CallDetailResponse(**data)

    def get_calls(
        self,
        limit: int = 10,
        offset: int = 0,
        q: Optional[str] = None,
        sort: str = "started_at.desc",
    ) -> CallListResponse:
        url = self.get_call_list_url()
        params = {"limit": limit, "offset": offset, "sort": sort}
        if q:
            params["q"] = q
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return CallListResponse(**data)

    def call_and_bridge(
        self,
        user_id: int,
        callee_number: str,
        ring_user_first: bool = True,
    ) -> CallAndBridgeResponse:
        url = self.get_call_and_bridge_url(user_id)
        data = {"callee_number": callee_number, "ring_user_first": ring_user_first}
        response = self.session.post(url, json=data)
        data = self.handle_response(response.status_code, response.json())
        return CallAndBridgeResponse(**data)

    def get_tasks(
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
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return TaskListResponse(**data)

    def create_task(self, task: TaskCreate) -> TaskResponse:
        url = self.get_task_list_url()
        response = self.session.post(url, json=task.model_dump(exclude_unset=True))
        data = self.handle_response(response.status_code, response.json())
        return TaskResponse(**data)

    def get_task(self, task_id: int) -> TaskDetailResponse:
        url = self.get_task_detail_url(task_id)
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return TaskDetailResponse(**data)
