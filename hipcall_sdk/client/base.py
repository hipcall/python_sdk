from abc import ABC, abstractmethod
from typing import Optional

from hipcall_sdk.constants import DEFAULT_HIPCALL_BASE_ADDRESS
from hipcall_sdk.exceptions import (
    UnauthorizedException,
    NotFoundException,
    UnprocessableEntityException,
    HipcallAPIException,
    BadRequestException,
)
from hipcall_sdk.models import (
    CallDetailResponse,
    CallListResponse,
    TaskListResponse,
    TaskResponse,
    TaskCreate,
    TaskDetailResponse,
    CallAndBridgeResponse,
)


EXCEPTION_MAP = {
    400: BadRequestException,
    401: UnauthorizedException,
    404: NotFoundException,
    422: UnprocessableEntityException,
}


class HipcallBaseClient(ABC):
    """
    Base class for Hipcall API clients.

    This class defines the interface for Hipcall API clients and provides
    some common functionality.

    Attributes:
        api_key (str): The API key used for authentication.
        base_url (str): The base URL for the Hipcall API, optional.
    """

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        if not api_key:
            raise ValueError("API key must be provided.")

        self.api_key = api_key
        self.base_url = base_url or DEFAULT_HIPCALL_BASE_ADDRESS

    def get_default_headers(self) -> dict[str, str]:
        """Get the default headers for the Hipcall API client.

        :return: Dict of default headers
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def handle_response(status_code: int, content: dict) -> dict:
        """Handle Hipcall API response status codes.

        :param status_code: HTTP response status code.
        :param content: HTTP response content.
        :return: Response dict if status is OK.
        :raises HipcallAPIException: If status code is not OK.
        """
        if status_code in [200, 201]:
            return content

        exc_class = EXCEPTION_MAP.get(status_code, HipcallAPIException)
        raise exc_class(status_code, content)

    def get_call_detail_url(self, call_id: str) -> str:
        """Get call detail URL for call ID.

        :param call_id: UUID of the call.
        :return: URL for fetching specific call detail.
        """
        return f"{self.base_url}/api/v3/calls/{call_id}"

    def get_call_list_url(self) -> str:
        """Get call list URL.

        :return: URL for fetching call list.
        """
        return f"{self.base_url}/api/v3/calls"

    def get_call_and_bridge_url(self, user_id) -> str:
        """Get call and bridge URL for given user ID.

        :param user_id: Database ID of the user.
        :return: URL for calling and bridging.
        """
        return f"{self.base_url}/api/v3/users/{user_id}/call"

    def get_task_list_url(self) -> str:
        """Get task list URL.

        :return: URL for fetching task list.
        """
        return f"{self.base_url}/api/v3/tasks"

    def get_task_detail_url(self, task_id) -> str:
        """Get task detail URL for given task ID.

        :param task_id: Database ID of the task.
        :return: URL for fetching task detail.
        """
        return f"{self.base_url}/api/v3/tasks/{task_id}"

    @abstractmethod
    def get_call(self, call_id: str, date: str) -> CallDetailResponse:
        """Get call details for given call ID and date.

        :param call_id: UUID of the call.
        :param date: Date of the call.
        :return: Pydantic model containing call details.
        """
        pass

    @abstractmethod
    def get_calls(
        self,
        limit: int = 10,
        offset: int = 0,
        q: Optional[str] = None,
        sort: str = "started_at.asc",
    ) -> CallListResponse:
        """Get list of calls with query.

        :param limit: Limit of query. Min 1, Max 100. Defaults to 10.
        :param offset: Offset of the query. Defaults to 0.
        :param q: Search query which is searched at caller_number and callee_number.
            Don't add + or 00 as prefix just write number with country code.
        :param sort: Sort parameter. Defaults to "started_at.asc".
        :return: Pydantic model containing call list and metadata.
        """
        pass

    @abstractmethod
    def call_and_bridge(
        self,
        user_id: int,
        callee_number: str,
        ring_user_first: bool = True,
    ) -> CallAndBridgeResponse:
        """Call and bridge user and given number.

        :param user_id: Database ID of the caller user.
        :param callee_number: Callee number.
        :param ring_user_first: Rings user first if set to True. Defaults to True.
        :return: Pydantic model containing call & bridge response.
        """
        pass

    @abstractmethod
    def get_tasks(
        self,
        limit: int = 10,
        offset: int = 0,
        q: Optional[str] = None,
        sort: str = "id.asc",
    ) -> TaskListResponse:
        """Get list of tasks with query.

        :param limit: Limit of query. Min 1, Max 100. Defaults to 10.
        :param offset: Offset of the query. Defaults to 0.
        :param q: Search query which is searched name of the task.
        :param sort: Sort parameter. Defaults to "id.asc".
            Supported fields: id and name
            Ordering options: asc, asc_nulls_last, asc_nulls_first, desc,
            desc_nulls_last, desc_nulls_first
        :return: Pydantic model containing task list and metadata.
        """
        pass

    @abstractmethod
    def create_task(self, task: TaskCreate) -> TaskResponse:
        """Create new task on Hipcall.

        :param task: Pydantic model containing data for Task creation.
        :return: Pydantic model containing created task information.
        """
        pass

    @abstractmethod
    def get_task(self, task_id: int) -> TaskDetailResponse:
        """Get task information by ID.

        :param task_id: Database ID of the task.
        :return: Pydantic model containing task information.
        """
        pass
