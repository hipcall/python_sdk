from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Meta(BaseModel):
    count: int
    limit: int
    offset: int


class Call(BaseModel):
    uuid: str
    started_at: str
    ended_at: str
    direction: str
    call_duration: Optional[int] = None
    first_touch_duration: Optional[int] = None
    missing_call: Optional[bool] = None
    answered_at: Optional[str] = None
    bridged_at: Optional[str] = None


class CallDetail(BaseModel):
    uuid: str
    started_at: datetime
    ended_at: datetime
    direction: str
    call_duration: Optional[int] = None
    first_touch_duration: Optional[int] = None
    missing_call: Optional[bool] = None
    answered_at: Optional[datetime] = None
    bridged_at: Optional[datetime] = None
    caller_id: Optional[int] = None
    contact_id: Optional[int] = None
    credited: Optional[bool] = None
    related_id: Optional[int] = None
    related_type: Optional[str] = None
    channel_type: Optional[str] = None
    number_id: Optional[int] = None
    caller_number: Optional[str] = None
    voicemail_id: Optional[int] = None
    voicemail_type: Optional[str] = None
    hangup_by: Optional[str] = None
    missing_call_reason: Optional[str] = None
    caller_type: Optional[str] = None
    callee_id: Optional[int] = None
    voicemail_url: Optional[str] = None
    channel_id: Optional[int] = None
    user_id: Optional[int] = None
    callee_number: Optional[str] = None
    call_flow: Optional[str] = None
    record_url: Optional[str] = None
    callback_time: Optional[datetime] = None
    callback_cdr_uuid: Optional[str] = None
    callee_type: Optional[str] = None
    callback_user_id: Optional[int] = None


class CallListResponse(BaseModel):
    data: List[Call]
    meta: Meta


class CallDetailResponse(BaseModel):
    data: CallDetail


class CallAndBridge(BaseModel):
    id: str


class CallAndBridgeResponse(BaseModel):
    data: CallAndBridge


class Task(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    done: bool
    done_at: Optional[datetime] = None


class TaskListResponse(BaseModel):
    data: List[Task]
    meta: Meta


class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None
    assign_to_user_id: Optional[int] = None
    auto_assign_to_user: Optional[bool] = None
    company_ids: Optional[List[int]] = None
    contact_ids: Optional[List[int]] = None
    deal_ids: Optional[List[int]] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    task_list_id: Optional[int] = None


class TaskResponse(BaseModel):
    data: Task


class TaskDetail(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    done: bool
    done_at: Optional[datetime] = None
    assign_to_user_id: Optional[int] = None
    auto_assign_to_user: Optional[bool] = None
    company_ids: Optional[List[int]] = None
    contact_ids: Optional[List[int]] = None
    deal_ids: Optional[List[int]] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    task_list_id: Optional[int] = None


class TaskDetailResponse(BaseModel):
    data: TaskDetail
