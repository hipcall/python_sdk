import requests

from hipcall_sdk.client.base import HipcallBaseClient
from hipcall_sdk.models import (
    AttributionCreate,
    AttributionResponse,
    CallAndBridgeResponse,
    CallDetailResponse,
    CallListResponse,
    CardCreate,
    CardListResponse,
    CardResponse,
    CommentCreate,
    CommentListResponse,
    CommentResponse,
    CompanyCreate,
    CompanyListResponse,
    CompanyResponse,
    CompanyUpdate,
    ConsentCreate,
    ConsentListResponse,
    ConsentResponse,
    ContactCenterAttributesResponse,
    ContactCreate,
    ContactListResponse,
    ContactResponse,
    ContactUpdate,
    ConversationListResponse,
    ConversationResponse,
    ConversationUpdate,
    CustomFieldDefinitionListResponse,
    DealListResponse,
    DealResponse,
    DispositionListResponse,
    DispositionOnCallResponse,
    DispositionUpdate,
    EmailListResponse,
    EmailRequest,
    EmployeeSizeListResponse,
    ExtensionCall,
    ExtensionCallCreate,
    ExtensionListResponse,
    ExtensionResponse,
    GreetingListResponse,
    GreetingResponse,
    InboxListResponse,
    InboxResponse,
    InboxUpdate,
    LifeCycleListResponse,
    LookupByEmailResponse,
    LookupByPhoneResponse,
    MessageListResponse,
    MessageResponse,
    MobileDevice,
    MobileDeviceCreate,
    MobileDeviceDeleteResponse,
    MobileDeviceUpdate,
    MobileDeviceUpdateResponse,
    NumberListResponse,
    NumberResponse,
    PhoneListResponse,
    PhoneRequest,
    ProcedureListResponse,
    ProcedureResponse,
    ProfileResponse,
    PushTokenCreate,
    PushTokenResponse,
    SectorListResponse,
    SipTokenCreate,
    SipTokenResponse,
    SourceListResponse,
    TagCreate,
    TagListResponse,
    TagResponse,
    TaskCreate,
    TaskDetailResponse,
    TaskListResponse,
    TaskResponse,
    TaskUpdate,
    TeamListResponse,
    TeamResponse,
    TemplateMessageCreate,
    TemplateMessageResponse,
    TextMessageCreate,
    TodayStatsResponse,
    UserListResponse,
    UserResponse,
    UserUpdate,
    VoicemailListResponse,
    VoicemailResponse,
)


class Client(HipcallBaseClient):
    def __init__(self, api_key: str, base_url: str | None = None):
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
        url = self.get_call_list_url()
        params = self.build_params(
            **{
                "limit": limit,
                "offset": offset,
                "sort": sort,
                "q": q,
                "started_at[gte]": started_at_gte,
                "started_at[lte]": started_at_lte,
                "missing_call[eq]": missing_call,
                "direction[eq]": direction,
                "call_duration[gte]": call_duration_gte,
                "call_duration[lte]": call_duration_lte,
                "user_id[eq]": user_id,
                "team_id[eq]": team_id,
            }
        )
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return CallListResponse(**data)

    def call_and_bridge(
        self,
        user_id: int,
        callee_number: str,
        ring_user_first: bool = True,
        call_masking: bool | None = None,
        call_masking_name: str | None = None,
    ) -> CallAndBridgeResponse:
        url = self.get_call_and_bridge_url(user_id)
        data = {"callee_number": callee_number, "ring_user_first": ring_user_first}
        if call_masking is not None:
            data["call_masking"] = call_masking
        if call_masking_name is not None:
            data["call_masking_name"] = call_masking_name
        response = self.session.post(url, json=data)
        data = self.handle_response(response.status_code, response.json())
        return CallAndBridgeResponse(**data)

    def get_tasks(
        self,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str = "id.asc",
        assign_to_user_id: int | None = None,
        done: bool | None = None,
    ) -> TaskListResponse:
        url = self.get_task_list_url()
        params = self.build_params(
            **{
                "limit": limit,
                "offset": offset,
                "sort": sort,
                "q": q,
                "assign_to_user_id[eq]": assign_to_user_id,
                "done[eq]": done,
            }
        )
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return TaskListResponse(**data)

    def create_task(self, task: TaskCreate) -> TaskResponse:
        url = self.get_task_list_url()
        payload = {"data": task.model_dump(mode="json", exclude_unset=True)}
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return TaskResponse(**data)

    def get_task(self, task_id: int) -> TaskDetailResponse:
        url = self.get_task_detail_url(task_id)
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return TaskDetailResponse(**data)

    def update_task(self, task_id: int, body: TaskUpdate) -> TaskResponse:
        """Update a task."""
        url = f"{self.base_url}/api/v3/tasks/{task_id}"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.patch(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return TaskResponse(**data)

    def get_task_comments(
        self,
        task_id: int,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> CommentListResponse:
        """List comments on a task."""
        url = f"{self.base_url}/api/v3/tasks/{task_id}/comments"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return CommentListResponse(**data)

    def create_task_comment(self, task_id: int, body: CommentCreate) -> CommentResponse:
        """Add a comment to a task."""
        url = f"{self.base_url}/api/v3/tasks/{task_id}/comments"
        payload = {"data": body.model_dump(mode="json", exclude_unset=True)}
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return CommentResponse(**data)

    def get_task_tags(
        self, task_id: int, limit: int = 10, offset: int = 0
    ) -> TagListResponse:
        """List tags on a task."""
        url = f"{self.base_url}/api/v3/tasks/{task_id}/tags"
        params = self.build_params(limit=limit, offset=offset)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return TagListResponse(**data)

    def add_task_tag(self, task_id: int, body: TagCreate) -> TagResponse:
        """Add a tag to a task."""
        url = f"{self.base_url}/api/v3/tasks/{task_id}/tags"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return TagResponse(**data)

    def delete_task_tag(self, task_id: int, tag_id: int) -> None:
        """Remove a tag from a task."""
        url = f"{self.base_url}/api/v3/tasks/{task_id}/tags/{tag_id}"
        response = self.session.delete(url)
        self.handle_response(response.status_code, self.load_json(response.text))

    def get_call_comments(
        self,
        call_id: str,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> CommentListResponse:
        """List comments on a call."""
        url = f"{self.base_url}/api/v3/calls/{call_id}/comments"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return CommentListResponse(**data)

    def create_call_comment(self, call_id: str, body: CommentCreate) -> CommentResponse:
        """Add a comment to a call."""
        url = f"{self.base_url}/api/v3/calls/{call_id}/comments"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return CommentResponse(**data)

    def get_call_tags(
        self, call_id: str, limit: int = 10, offset: int = 0
    ) -> TagListResponse:
        """List tags on a call."""
        url = f"{self.base_url}/api/v3/calls/{call_id}/tags"
        params = self.build_params(limit=limit, offset=offset)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return TagListResponse(**data)

    def add_call_tag(self, call_id: str, body: TagCreate) -> TagResponse:
        """Add a tag to a call."""
        url = f"{self.base_url}/api/v3/calls/{call_id}/tags"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return TagResponse(**data)

    def delete_call_tag(self, call_id: str, tag_id: int) -> None:
        """Remove a tag from a call."""
        url = f"{self.base_url}/api/v3/calls/{call_id}/tags/{tag_id}"
        response = self.session.delete(url)
        self.handle_response(response.status_code, self.load_json(response.text))

    def get_call_cards(self, call_id: str) -> CardListResponse:
        """List cards sent during a call."""
        url = f"{self.base_url}/api/v3/calls/{call_id}/cards"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return CardListResponse(**data)

    def create_call_card(self, call_id: str, body: CardCreate) -> CardResponse:
        """Send a card to a live call."""
        url = f"{self.base_url}/api/v3/calls/{call_id}/cards"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return CardResponse(**data)

    def get_call_disposition(self, call_id: str) -> DispositionOnCallResponse:
        """Get the disposition set on a call."""
        url = f"{self.base_url}/api/v3/calls/{call_id}/disposition"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return DispositionOnCallResponse(**data)

    def set_call_disposition(
        self, call_id: str, body: DispositionUpdate
    ) -> DispositionOnCallResponse:
        """Set or replace a call's disposition."""
        url = f"{self.base_url}/api/v3/calls/{call_id}/disposition"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.put(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return DispositionOnCallResponse(**data)

    def get_dispositions(
        self,
        direction: str | None = None,
        outcome: str | None = None,
        active: bool | None = None,
        call_uuid: str | None = None,
    ) -> DispositionListResponse:
        """List call dispositions."""
        url = f"{self.base_url}/api/v3/dispositions"
        params = self.build_params(
            direction=direction, outcome=outcome, active=active, call_uuid=call_uuid
        )
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return DispositionListResponse(**data)

    def get_extensions(
        self,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> ExtensionListResponse:
        """List extensions."""
        url = f"{self.base_url}/api/v3/extensions"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return ExtensionListResponse(**data)

    def get_extension(self, extension_id: int) -> ExtensionResponse:
        """Get an extension by ID."""
        url = f"{self.base_url}/api/v3/extensions/{extension_id}"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return ExtensionResponse(**data)

    def call_extension(
        self, extension_id: int, body: ExtensionCallCreate
    ) -> ExtensionCall:
        """Place an outbound call from an extension."""
        url = f"{self.base_url}/api/v3/extensions/{extension_id}/call"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return ExtensionCall(**data)

    def get_greetings(
        self,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> GreetingListResponse:
        """List greetings."""
        url = f"{self.base_url}/api/v3/greetings"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return GreetingListResponse(**data)

    def get_greeting(self, greeting_id: int) -> GreetingResponse:
        """Get a greeting by ID."""
        url = f"{self.base_url}/api/v3/greetings/{greeting_id}"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return GreetingResponse(**data)

    def get_numbers(
        self,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> NumberListResponse:
        """List phone numbers."""
        url = f"{self.base_url}/api/v3/numbers"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return NumberListResponse(**data)

    def get_number(self, number_id: int) -> NumberResponse:
        """Get a phone number by ID."""
        url = f"{self.base_url}/api/v3/numbers/{number_id}"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return NumberResponse(**data)

    def get_teams(
        self,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> TeamListResponse:
        """List teams."""
        url = f"{self.base_url}/api/v3/teams"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return TeamListResponse(**data)

    def get_team(self, team_id: int) -> TeamResponse:
        """Get a team by ID."""
        url = f"{self.base_url}/api/v3/teams/{team_id}"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return TeamResponse(**data)

    def get_voicemails(
        self,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> VoicemailListResponse:
        """List voicemails."""
        url = f"{self.base_url}/api/v3/voicemails"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return VoicemailListResponse(**data)

    def get_voicemail(self, voicemail_id: int) -> VoicemailResponse:
        """Get a voicemail by ID."""
        url = f"{self.base_url}/api/v3/voicemails/{voicemail_id}"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return VoicemailResponse(**data)

    def get_users(
        self,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> UserListResponse:
        """List users."""
        url = f"{self.base_url}/api/v3/users"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return UserListResponse(**data)

    def get_user(self, user_id: int) -> UserResponse:
        """Get a user by ID."""
        url = f"{self.base_url}/api/v3/users/{user_id}"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return UserResponse(**data)

    def update_user(self, user_id: int, body: UserUpdate) -> UserResponse:
        """Update a user."""
        url = f"{self.base_url}/api/v3/users/{user_id}"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.patch(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return UserResponse(**data)

    def get_user_today_stats(self, user_id: int) -> TodayStatsResponse:
        """Get today's statistics for a user."""
        url = f"{self.base_url}/api/v3/users/{user_id}/stats/today"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return TodayStatsResponse(**data)

    def get_profile(self) -> ProfileResponse:
        """Get the authenticated user's profile."""
        url = f"{self.base_url}/api/v3/profile"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return ProfileResponse(**data)

    def get_profile_today_stats(self) -> TodayStatsResponse:
        """Get today's statistics for the caller."""
        url = f"{self.base_url}/api/v3/profile/stats/today"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return TodayStatsResponse(**data)

    def get_contacts(
        self,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> ContactListResponse:
        """List contacts."""
        url = f"{self.base_url}/api/v3/contacts"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return ContactListResponse(**data)

    def create_contact(self, body: ContactCreate) -> ContactResponse:
        """Create a contact."""
        url = f"{self.base_url}/api/v3/contacts"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return ContactResponse(**data)

    def get_contact(self, contact_id: int) -> ContactResponse:
        """Get a contact by ID."""
        url = f"{self.base_url}/api/v3/contacts/{contact_id}"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return ContactResponse(**data)

    def update_contact(self, contact_id: int, body: ContactUpdate) -> ContactResponse:
        """Update a contact."""
        url = f"{self.base_url}/api/v3/contacts/{contact_id}"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.patch(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return ContactResponse(**data)

    def get_contact_by_external_id(self, external_id: str) -> ContactResponse:
        """Get a contact by external ID."""
        url = f"{self.base_url}/api/v3/contacts/by-external-id/{external_id}"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return ContactResponse(**data)

    def assign_contact(
        self, contact_id: int, assign_to_user_id: int | None
    ) -> ContactResponse:
        """Assign a contact to a user. Pass None to unassign."""
        url = f"{self.base_url}/api/v3/contacts/{contact_id}/assign"
        payload = {"assign_to_user_id": assign_to_user_id}
        response = self.session.patch(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return ContactResponse(**data)

    def get_contact_custom_fields(
        self, active: bool | None = None
    ) -> CustomFieldDefinitionListResponse:
        """List contact custom field definitions."""
        url = f"{self.base_url}/api/v3/contacts/custom-fields"
        params = self.build_params(active=active)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return CustomFieldDefinitionListResponse(**data)

    def get_contact_comments(
        self,
        contact_id: int,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> CommentListResponse:
        """List comments on a contact."""
        url = f"{self.base_url}/api/v3/contacts/{contact_id}/comments"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return CommentListResponse(**data)

    def create_contact_comment(
        self, contact_id: int, body: CommentCreate
    ) -> CommentResponse:
        """Add a comment to a contact."""
        url = f"{self.base_url}/api/v3/contacts/{contact_id}/comments"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return CommentResponse(**data)

    def get_contact_consents(self, contact_id: int) -> ConsentListResponse:
        """List a contact's consent history."""
        url = f"{self.base_url}/api/v3/contacts/{contact_id}/consent"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return ConsentListResponse(**data)

    def create_contact_consent(
        self, contact_id: int, body: ConsentCreate
    ) -> ConsentResponse:
        """Record advertising consent on a contact."""
        url = f"{self.base_url}/api/v3/contacts/{contact_id}/consent"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return ConsentResponse(**data)

    def add_contact_emails(
        self, contact_id: int, body: EmailRequest
    ) -> EmailListResponse:
        """Add email addresses to a contact."""
        url = f"{self.base_url}/api/v3/contacts/{contact_id}/emails"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return EmailListResponse(**data)

    def delete_contact_email(self, contact_id: int, email: str) -> None:
        """Remove an email address from a contact."""
        url = f"{self.base_url}/api/v3/contacts/{contact_id}/emails/{email}"
        response = self.session.delete(url)
        self.handle_response(response.status_code, self.load_json(response.text))

    def add_contact_phones(
        self, contact_id: int, body: PhoneRequest
    ) -> PhoneListResponse:
        """Add phone numbers to a contact."""
        url = f"{self.base_url}/api/v3/contacts/{contact_id}/phones"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return PhoneListResponse(**data)

    def delete_contact_phone(self, contact_id: int, number: str) -> None:
        """Remove a phone number from a contact."""
        url = f"{self.base_url}/api/v3/contacts/{contact_id}/phones/{number}"
        response = self.session.delete(url)
        self.handle_response(response.status_code, self.load_json(response.text))

    def get_contact_tags(
        self, contact_id: int, limit: int = 10, offset: int = 0
    ) -> TagListResponse:
        """List tags on a contact."""
        url = f"{self.base_url}/api/v3/contacts/{contact_id}/tags"
        params = self.build_params(limit=limit, offset=offset)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return TagListResponse(**data)

    def add_contact_tag(self, contact_id: int, body: TagCreate) -> TagResponse:
        """Add a tag to a contact."""
        url = f"{self.base_url}/api/v3/contacts/{contact_id}/tags"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return TagResponse(**data)

    def delete_contact_tag(self, contact_id: int, tag_id: int) -> None:
        """Remove a tag from a contact."""
        url = f"{self.base_url}/api/v3/contacts/{contact_id}/tags/{tag_id}"
        response = self.session.delete(url)
        self.handle_response(response.status_code, self.load_json(response.text))

    def get_companies(
        self,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> CompanyListResponse:
        """List companies."""
        url = f"{self.base_url}/api/v3/companies"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return CompanyListResponse(**data)

    def create_company(self, body: CompanyCreate) -> CompanyResponse:
        """Create a company."""
        url = f"{self.base_url}/api/v3/companies"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return CompanyResponse(**data)

    def get_company(self, company_id: int) -> CompanyResponse:
        """Get a company by ID."""
        url = f"{self.base_url}/api/v3/companies/{company_id}"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return CompanyResponse(**data)

    def update_company(self, company_id: int, body: CompanyUpdate) -> CompanyResponse:
        """Update a company."""
        url = f"{self.base_url}/api/v3/companies/{company_id}"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.patch(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return CompanyResponse(**data)

    def get_company_by_external_id(self, external_id: str) -> CompanyResponse:
        """Get a company by external ID."""
        url = f"{self.base_url}/api/v3/companies/by-external-id/{external_id}"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return CompanyResponse(**data)

    def assign_company(
        self, company_id: int, assign_to_user_id: int | None
    ) -> CompanyResponse:
        """Assign a company to a user. Pass None to unassign."""
        url = f"{self.base_url}/api/v3/companies/{company_id}/assign"
        payload = {"assign_to_user_id": assign_to_user_id}
        response = self.session.patch(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return CompanyResponse(**data)

    def get_company_custom_fields(
        self, active: bool | None = None
    ) -> CustomFieldDefinitionListResponse:
        """List company custom field definitions."""
        url = f"{self.base_url}/api/v3/companies/custom-fields"
        params = self.build_params(active=active)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return CustomFieldDefinitionListResponse(**data)

    def get_company_comments(
        self,
        company_id: int,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> CommentListResponse:
        """List comments on a company."""
        url = f"{self.base_url}/api/v3/companies/{company_id}/comments"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return CommentListResponse(**data)

    def create_company_comment(
        self, company_id: int, body: CommentCreate
    ) -> CommentResponse:
        """Add a comment to a company."""
        url = f"{self.base_url}/api/v3/companies/{company_id}/comments"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return CommentResponse(**data)

    def add_company_emails(
        self, company_id: int, body: EmailRequest
    ) -> EmailListResponse:
        """Add email addresses to a company."""
        url = f"{self.base_url}/api/v3/companies/{company_id}/emails"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return EmailListResponse(**data)

    def delete_company_email(self, company_id: int, email: str) -> None:
        """Remove an email address from a company."""
        url = f"{self.base_url}/api/v3/companies/{company_id}/emails/{email}"
        response = self.session.delete(url)
        self.handle_response(response.status_code, self.load_json(response.text))

    def add_company_phones(
        self, company_id: int, body: PhoneRequest
    ) -> PhoneListResponse:
        """Add phone numbers to a company."""
        url = f"{self.base_url}/api/v3/companies/{company_id}/phones"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return PhoneListResponse(**data)

    def delete_company_phone(self, company_id: int, number: str) -> None:
        """Remove a phone number from a company."""
        url = f"{self.base_url}/api/v3/companies/{company_id}/phones/{number}"
        response = self.session.delete(url)
        self.handle_response(response.status_code, self.load_json(response.text))

    def get_company_tags(
        self, company_id: int, limit: int = 10, offset: int = 0
    ) -> TagListResponse:
        """List tags on a company."""
        url = f"{self.base_url}/api/v3/companies/{company_id}/tags"
        params = self.build_params(limit=limit, offset=offset)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return TagListResponse(**data)

    def add_company_tag(self, company_id: int, body: TagCreate) -> TagResponse:
        """Add a tag to a company."""
        url = f"{self.base_url}/api/v3/companies/{company_id}/tags"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return TagResponse(**data)

    def delete_company_tag(self, company_id: int, tag_id: int) -> None:
        """Remove a tag from a company."""
        url = f"{self.base_url}/api/v3/companies/{company_id}/tags/{tag_id}"
        response = self.session.delete(url)
        self.handle_response(response.status_code, self.load_json(response.text))

    def get_employee_sizes(self) -> EmployeeSizeListResponse:
        """List employee-size bands."""
        url = f"{self.base_url}/api/v3/employee-sizes"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return EmployeeSizeListResponse(**data)

    def get_life_cycles(
        self,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> LifeCycleListResponse:
        """List life cycle values."""
        url = f"{self.base_url}/api/v3/life-cycles"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return LifeCycleListResponse(**data)

    def get_sectors(
        self,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> SectorListResponse:
        """List sector values."""
        url = f"{self.base_url}/api/v3/sectors"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return SectorListResponse(**data)

    def get_sources(
        self,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> SourceListResponse:
        """List traction channel (source) values."""
        url = f"{self.base_url}/api/v3/sources"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return SourceListResponse(**data)

    def get_contact_center_attributes(self) -> ContactCenterAttributesResponse:
        """List all contact-centre attributes in one call."""
        url = f"{self.base_url}/api/v3/contact-center/attributes"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return ContactCenterAttributesResponse(**data)

    def lookup_by_email(self, email: str) -> LookupByEmailResponse:
        """Look up contacts and companies by email address."""
        url = f"{self.base_url}/api/v3/lookup/by_email"
        params = self.build_params(email=email)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return LookupByEmailResponse(**data)

    def lookup_by_phone(self, number: str) -> LookupByPhoneResponse:
        """Look up contacts and companies by phone number."""
        url = f"{self.base_url}/api/v3/lookup/by_phone"
        params = self.build_params(number=number)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return LookupByPhoneResponse(**data)

    def get_tags(
        self,
        type: str | None = None,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> TagListResponse:
        """List tags. `type` is one of contact_centre, communication, task, ticket, content, deal."""
        url = f"{self.base_url}/api/v3/tags"
        params = self.build_params(
            type=type, limit=limit, offset=offset, q=q, sort=sort
        )
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return TagListResponse(**data)

    def get_inboxes(
        self, limit: int = 10, offset: int = 0, q: str | None = None
    ) -> InboxListResponse:
        """List inboxes."""
        url = f"{self.base_url}/api/v3/inbox"
        params = self.build_params(limit=limit, offset=offset, q=q)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return InboxListResponse(**data)

    def get_inbox(self, inbox_id: str) -> InboxResponse:
        """Get an inbox."""
        url = f"{self.base_url}/api/v3/inbox/{inbox_id}"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return InboxResponse(**data)

    def update_inbox(self, inbox_id: str, body: InboxUpdate) -> InboxResponse:
        """Update an inbox."""
        url = f"{self.base_url}/api/v3/inbox/{inbox_id}"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.patch(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return InboxResponse(**data)

    def get_conversations(
        self,
        status_in: str | None = None,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> ConversationListResponse:
        """List conversations. `status_in` is a comma-separated list of statuses."""
        url = f"{self.base_url}/api/v3/conversations"
        params = self.build_params(
            **{
                "status[in]": status_in,
                "limit": limit,
                "offset": offset,
                "q": q,
                "sort": sort,
            }
        )
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return ConversationListResponse(**data)

    def get_conversation(self, conversation_id: str, date: str) -> ConversationResponse:
        """Get a conversation by ID. `date` (UTC, %Y-%m-%d) is required by the API spec."""
        url = f"{self.base_url}/api/v3/conversations/{conversation_id}"
        params = self.build_params(date=date)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return ConversationResponse(**data)

    def update_conversation(
        self, conversation_id: str, body: ConversationUpdate
    ) -> ConversationResponse:
        """Update a conversation."""
        url = f"{self.base_url}/api/v3/conversations/{conversation_id}"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.patch(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return ConversationResponse(**data)

    def get_conversation_messages(
        self, conversation_id: str, limit: int = 10, offset: int = 0
    ) -> MessageListResponse:
        """List messages in a conversation."""
        url = f"{self.base_url}/api/v3/conversations/{conversation_id}/messages"
        params = self.build_params(limit=limit, offset=offset)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return MessageListResponse(**data)

    def send_text_message(
        self, conversation_id: str, body: TextMessageCreate
    ) -> MessageResponse:
        """Send a text message to a conversation."""
        url = f"{self.base_url}/api/v3/conversations/{conversation_id}/messages/text"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return MessageResponse(**data)

    def send_template_message(
        self, inbox_id: str, body: TemplateMessageCreate
    ) -> TemplateMessageResponse:
        """Send a WhatsApp template message."""
        url = f"{self.base_url}/api/v3/inbox/{inbox_id}/messages/template"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return TemplateMessageResponse(**data)

    def get_template_message(
        self, inbox_id: str, template_message_id: str
    ) -> TemplateMessageResponse:
        """Get a template send record."""
        url = f"{self.base_url}/api/v3/inbox/{inbox_id}/messages/template/{template_message_id}"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return TemplateMessageResponse(**data)

    def get_deals(
        self,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> DealListResponse:
        """List deals."""
        url = f"{self.base_url}/api/v3/deals"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return DealListResponse(**data)

    def get_deal(self, deal_id: int) -> DealResponse:
        """Get a deal by ID."""
        url = f"{self.base_url}/api/v3/deals/{deal_id}"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return DealResponse(**data)

    def get_deal_comments(
        self,
        deal_id: int,
        limit: int = 10,
        offset: int = 0,
        q: str | None = None,
        sort: str | None = None,
    ) -> CommentListResponse:
        """List comments on a deal."""
        url = f"{self.base_url}/api/v3/deals/{deal_id}/comments"
        params = self.build_params(limit=limit, offset=offset, q=q, sort=sort)
        response = self.session.get(url, params=params)
        data = self.handle_response(response.status_code, response.json())
        return CommentListResponse(**data)

    def create_deal_comment(self, deal_id: int, body: CommentCreate) -> CommentResponse:
        """Add a comment to a deal."""
        url = f"{self.base_url}/api/v3/deals/{deal_id}/comments"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return CommentResponse(**data)

    def get_procedures(self) -> ProcedureListResponse:
        """List published procedures."""
        url = f"{self.base_url}/api/v3/procedures"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return ProcedureListResponse(**data)

    def get_procedure(self, procedure_uuid: str) -> ProcedureResponse:
        """Get a published procedure by UUID."""
        url = f"{self.base_url}/api/v3/procedures/{procedure_uuid}"
        response = self.session.get(url)
        data = self.handle_response(response.status_code, response.json())
        return ProcedureResponse(**data)

    def register_mobile_device(self, body: MobileDeviceCreate) -> MobileDevice:
        """Register a mobile device."""
        url = f"{self.base_url}/api/v3/mobile/devices"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return MobileDevice(**data)

    def update_mobile_device(
        self, device_id: str, body: MobileDeviceUpdate
    ) -> MobileDeviceUpdateResponse:
        """Update mobile device settings."""
        url = f"{self.base_url}/api/v3/mobile/devices/{device_id}"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.patch(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return MobileDeviceUpdateResponse(**data)

    def delete_mobile_device(self, device_id: str) -> MobileDeviceDeleteResponse:
        """Unregister a mobile device."""
        url = f"{self.base_url}/api/v3/mobile/devices/{device_id}"
        response = self.session.delete(url)
        data = self.handle_response(response.status_code, response.json())
        return MobileDeviceDeleteResponse(**data)

    def register_push_token(self, body: PushTokenCreate) -> PushTokenResponse:
        """Register a push notification token."""
        url = f"{self.base_url}/api/v3/push/token"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return PushTokenResponse(**data)

    def delete_push_token(self) -> None:
        """Delete a push notification token."""
        url = f"{self.base_url}/api/v3/push/token"
        response = self.session.delete(url)
        self.handle_response(response.status_code, self.load_json(response.text))

    def create_sip_token(
        self, request: SipTokenCreate | None = None
    ) -> SipTokenResponse:
        """Generate a SIP JWT token."""
        url = f"{self.base_url}/api/v3/sip/token"
        payload = request.model_dump(mode="json", exclude_unset=True) if request else {}
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return SipTokenResponse(**data)

    def create_attribution(self, body: AttributionCreate) -> AttributionResponse:
        """Record an attribution event."""
        url = f"{self.base_url}/api/v3/attribution"
        payload = body.model_dump(mode="json", exclude_unset=True)
        response = self.session.post(url, json=payload)
        data = self.handle_response(response.status_code, response.json())
        return AttributionResponse(**data)
