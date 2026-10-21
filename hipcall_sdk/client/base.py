import json
from abc import ABC, abstractmethod

from hipcall_sdk.constants import DEFAULT_HIPCALL_BASE_ADDRESS
from hipcall_sdk.exceptions import (
    BadRequestException,
    HipcallAPIException,
    NotFoundException,
    UnauthorizedException,
    UnprocessableEntityException,
)
from hipcall_sdk.models import (
    CallAndBridgeResponse,
    CallDetailResponse,
    CallListResponse,
    TaskCreate,
    TaskDetailResponse,
    TaskListResponse,
    TaskResponse,
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

    def __init__(self, api_key: str, base_url: str | None = None):
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
    def handle_response(status_code: int, content: dict | None = None) -> dict:
        """Handle Hipcall API response status codes.

        :param status_code: HTTP response status code.
        :param content: HTTP response content.
        :return: Response dict if status is OK.
        :raises HipcallAPIException: If status code is not OK.
        """
        if status_code in [200, 201]:
            return content

        if status_code == 204:
            return content or {}

        exc_class = EXCEPTION_MAP.get(status_code, HipcallAPIException)
        raise exc_class(status_code, content)

    @staticmethod
    def load_json(text: str) -> dict | None:
        """Parse a response body that may be empty (e.g. HTTP 204) or not JSON
        (e.g. an HTML error page from a proxy).

        :param text: Raw response body.
        :return: Parsed JSON, None if the body is empty, or {"raw": text} if
            the body is not valid JSON.
        """
        if not text:
            return None
        try:
            return json.loads(text)
        except ValueError:
            return {"raw": text}

    @staticmethod
    def build_params(**kwargs) -> dict:
        """Build query params, dropping None values and lower-casing booleans.

        :param kwargs: Query parameters.
        :return: Dict of query parameters ready to send.
        """
        return {
            k: (str(v).lower() if isinstance(v, bool) else v)
            for k, v in kwargs.items()
            if v is not None
        }

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

    @abstractmethod
    def get_calls(
        self,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str = "started_at.desc",
        started_at_gte: str | None = None,
        started_at_lte: str | None = None,
        missing_call: bool | None = None,
        direction: str | None = None,
        call_duration_gte: int | None = None,
        call_duration_lte: int | None = None,
        user_id: int | None = None,
        team_id: int | None = None,
    ) -> CallListResponse:
        """Get list of calls with query.

        :param limit: Limit of query. Min 1, Max 100. Defaults to 10.
        :param offset: Offset of the query. Defaults to 0.
        :param q: Search query which is searched at caller_number and callee_number.
            Don't add + or 00 as prefix just write number with country code.
        :param sort: Sort parameter. Defaults to "started_at.desc".
        :param started_at_gte: Only calls started at or after this UTC datetime.
        :param started_at_lte: Only calls started at or before this UTC datetime.
        :param missing_call: Filter by missing call status.
        :param direction: Filter by direction (inbound, outbound, internal).
        :param call_duration_gte: Minimum call duration in seconds.
        :param call_duration_lte: Maximum call duration in seconds.
        :param user_id: Only calls handled by this user.
        :param team_id: Only calls routed to this team.
        :return: Pydantic model containing call list and metadata.
        """

    @abstractmethod
    def call_and_bridge(
        self,
        user_id: int,
        callee_number: str,
        ring_user_first: bool = True,
        call_masking: bool | None = None,
        call_masking_name: str | None = None,
    ) -> CallAndBridgeResponse:
        """Call and bridge user and given number.

        :param user_id: Database ID of the caller user.
        :param callee_number: Callee number.
        :param ring_user_first: Rings user first if set to True. Defaults to True.
        :param call_masking: Enable call masking for this call.
        :param call_masking_name: Name to use for call masking (max 30 chars).
        :return: Pydantic model containing call & bridge response.
        """

    @abstractmethod
    def get_tasks(
        self,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str = "id.asc",
        assign_to_user_id: int | None = None,
        done: bool | None = None,
    ) -> TaskListResponse:
        """Get list of tasks with query.

        :param limit: Limit of query. Min 1, Max 100. Defaults to 10.
        :param offset: Offset of the query. Defaults to 0.
        :param q: Search query which is searched name of the task.
        :param sort: Sort parameter. Defaults to "id.asc".
            Supported fields: id and name
            Ordering options: asc, asc_nulls_last, asc_nulls_first, desc,
            desc_nulls_last, desc_nulls_first
        :param assign_to_user_id: Only tasks assigned to this user.
        :param done: Filter by completion status.
        :return: Pydantic model containing task list and metadata.
        """

    @abstractmethod
    def create_task(self, task: TaskCreate) -> TaskResponse:
        """Create new task on Hipcall.

        :param task: Pydantic model containing data for Task creation.
        :return: Pydantic model containing created task information.
        """

    @abstractmethod
    def get_task(self, task_id: int) -> TaskDetailResponse:
        """Get task information by ID.

        :param task_id: Database ID of the task.
        :return: Pydantic model containing task information.
        """
