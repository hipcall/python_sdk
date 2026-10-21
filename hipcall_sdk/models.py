from datetime import date as Date
from datetime import datetime
from typing import Any

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
    call_duration: int | None = None
    first_touch_duration: int | None = None
    missing_call: bool | None = None
    answered_at: str | None = None
    bridged_at: str | None = None


class CallDetail(BaseModel):
    uuid: str
    started_at: datetime
    ended_at: datetime
    direction: str
    call_duration: int | None = None
    first_touch_duration: int | None = None
    missing_call: bool | None = None
    answered_at: datetime | None = None
    bridged_at: datetime | None = None
    caller_id: int | None = None
    contact_id: int | None = None
    credited: bool | None = None
    related_id: int | None = None
    related_type: str | None = None
    channel_type: str | None = None
    number_id: int | None = None
    caller_number: str | None = None
    voicemail_id: int | None = None
    voicemail_type: str | None = None
    hangup_by: str | None = None
    missing_call_reason: str | None = None
    caller_type: str | None = None
    callee_id: int | None = None
    voicemail_url: str | None = None
    channel_id: int | None = None
    user_id: int | None = None
    callee_number: str | None = None
    call_flow: str | None = None
    record_url: str | None = None
    callback_time: datetime | None = None
    callback_cdr_uuid: str | None = None
    callee_type: str | None = None
    callback_user_id: int | None = None


class CallListResponse(BaseModel):
    data: list[Call]
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
    description: str | None = None
    done: bool
    done_at: datetime | None = None


class TaskListResponse(BaseModel):
    data: list[Task]
    meta: Meta


class TaskCreate(BaseModel):
    name: str
    description: str | None = None
    assign_to_user_id: int | None = None
    auto_assign_to_user: bool | None = None
    company_ids: list[int] | None = None
    contact_ids: list[int] | None = None
    deal_ids: list[int] | None = None
    due_date: datetime | None = None
    priority: str | None = None
    task_list_id: int | None = None


class TaskResponse(BaseModel):
    data: Task


class TaskDetail(BaseModel):
    id: int
    name: str
    description: str | None = None
    done: bool
    done_at: datetime | None = None
    assign_to_user_id: int | None = None
    auto_assign_to_user: bool | None = None
    company_ids: list[int] | None = None
    contact_ids: list[int] | None = None
    deal_ids: list[int] | None = None
    due_date: datetime | None = None
    priority: str | None = None
    task_list_id: int | None = None


class TaskDetailResponse(BaseModel):
    data: TaskDetail


class CountMeta(BaseModel):
    count: int


class UserSummary(BaseModel):
    id: int
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None


class NamedAttribute(BaseModel):
    id: int | None = None
    name: str | None = None


class Phone(BaseModel):
    number: str
    id: int | None = None
    country: str | None = None
    order: int | None = None


class PhoneInput(BaseModel):
    number: str
    country: str


class PhoneRequest(BaseModel):
    phones: list[PhoneInput]


class PhoneListResponse(BaseModel):
    data: list[Phone]
    meta: dict[str, Any] | None = None


class Email(BaseModel):
    email: str
    order: int | None = None


class EmailInput(BaseModel):
    email: str


class EmailRequest(BaseModel):
    emails: list[str]


class EmailListResponse(BaseModel):
    data: list[Email]
    meta: dict[str, Any] | None = None


class Tag(BaseModel):
    id: int
    name: str
    color: str
    color_name: str
    description: str | None = None


class TagResponse(BaseModel):
    data: Tag


class TagListResponse(BaseModel):
    data: list[Tag]
    meta: Meta | None = None


class TagCreate(BaseModel):
    tag_id: int


class Comment(BaseModel):
    id: int
    content: str
    user: UserSummary | None = None


class CommentResponse(BaseModel):
    data: Comment


class CommentListResponse(BaseModel):
    data: list[Comment]
    meta: Meta | None = None


class CommentCreate(BaseModel):
    content: str


class AssignRequest(BaseModel):
    assign_to_user_id: int | None = None


class CustomFieldDefinition(BaseModel):
    name: str
    slug: str
    field_type: str
    active: bool
    position: int
    required: bool
    number_type: str | None = None
    options: list[str] | None = None


class CustomFieldDefinitionListResponse(BaseModel):
    data: list[CustomFieldDefinition]
    meta: CountMeta | None = None


class EmployeeSizeOption(BaseModel):
    value: str
    label: str


class EmployeeSizeListResponse(BaseModel):
    data: list[EmployeeSizeOption]
    meta: CountMeta | None = None


class LifeCycle(BaseModel):
    id: int
    name: str
    order: int | None = None


class LifeCycleListResponse(BaseModel):
    data: list[LifeCycle]
    meta: Meta | None = None


class SectorListResponse(BaseModel):
    data: list[NamedAttribute]
    meta: Meta | None = None


class SourceListResponse(BaseModel):
    data: list[NamedAttribute]
    meta: Meta | None = None


class AttributeGroup(BaseModel):
    data: list[dict[str, Any]] = []
    count: int | None = None
    truncated: bool | None = None


class ContactCenterAttributes(BaseModel):
    employee_sizes: AttributeGroup | None = None
    life_cycles: AttributeGroup | None = None
    sectors: AttributeGroup | None = None
    sources: AttributeGroup | None = None


class ContactCenterAttributesResponse(BaseModel):
    data: ContactCenterAttributes


class ContactCompany(BaseModel):
    id: int | None = None
    name: str | None = None
    linkedin_url: str | None = None
    website_url: str | None = None


class Contact(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    job_title: str | None = None
    external_id: str | None = None
    custom_url: str | None = None
    linkedin_url: str | None = None
    emails: list[Email] | None = None
    phones: list[Phone] | None = None
    company: ContactCompany | None = None
    user: UserSummary | None = None
    life_cycle: NamedAttribute | None = None
    sector: NamedAttribute | None = None
    source: NamedAttribute | None = None
    custom_fields: dict[str, Any] | None = None


class ContactResponse(BaseModel):
    data: Contact


class ContactListResponse(BaseModel):
    data: list[Contact]
    meta: Meta


class ContactCreate(BaseModel):
    first_name: str
    last_name: str | None = None
    job_title: str | None = None
    company_id: int | None = None
    assign_to_user_id: int | None = None
    external_id: str | None = None
    custom_url: str | None = None
    linkedin_url: str | None = None
    life_cycle_id: int | None = None
    sector_id: int | None = None
    source_id: int | None = None
    custom_fields: dict[str, Any] | None = None
    phones: list[PhoneInput] | None = None
    emails: list[EmailInput] | None = None


class ContactUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    job_title: str | None = None
    company_id: int | None = None
    assign_to_user_id: int | None = None
    external_id: str | None = None
    custom_url: str | None = None
    linkedin_url: str | None = None
    life_cycle_id: int | None = None
    sector_id: int | None = None
    source_id: int | None = None
    custom_fields: dict[str, Any] | None = None


class ConsentEvidence(BaseModel):
    note: str


class Consent(BaseModel):
    id: int
    action: str
    purpose: str
    source: str | None = None
    performed_at: datetime | None = None
    expires_at: datetime | None = None
    evidence: dict[str, Any] | None = None
    text_version: str | None = None


class ConsentResponse(BaseModel):
    data: Consent


class ConsentListResponse(BaseModel):
    data: list[Consent]


class ConsentCreate(BaseModel):
    action: str
    evidence: ConsentEvidence
    expires_at: datetime | None = None


class CompanyContact(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    job_title: str | None = None


class Company(BaseModel):
    id: int
    name: str
    external_id: str | None = None
    custom_url: str | None = None
    linkedin_url: str | None = None
    website_url: str | None = None
    employee_size: str | None = None
    emails: list[Email] | None = None
    phones: list[Phone] | None = None
    contacts: list[CompanyContact] | None = None
    user: UserSummary | None = None
    life_cycle: NamedAttribute | None = None
    sector: NamedAttribute | None = None
    source: NamedAttribute | None = None
    custom_fields: dict[str, Any] | None = None


class CompanyResponse(BaseModel):
    data: Company


class CompanyListResponse(BaseModel):
    data: list[Company]
    meta: Meta


class CompanyCreate(BaseModel):
    name: str
    description: str | None = None
    assign_to_user_id: int | None = None
    external_id: str | None = None
    custom_url: str | None = None
    linkedin_url: str | None = None
    website_url: str | None = None
    employee_size: str | None = None
    life_cycle_id: int | None = None
    sector_id: int | None = None
    source_id: int | None = None
    custom_fields: dict[str, Any] | None = None
    phones: list[PhoneInput] | None = None
    emails: list[EmailInput] | None = None


class CompanyUpdate(BaseModel):
    name: str | None = None
    external_id: str | None = None
    custom_url: str | None = None
    linkedin_url: str | None = None
    website_url: str | None = None
    employee_size: str | None = None
    life_cycle_id: int | None = None
    sector_id: int | None = None
    source_id: int | None = None
    custom_fields: dict[str, Any] | None = None


class LookupData(BaseModel):
    contacts: list[Contact]
    companies: list[Company]


class LookupByEmailResponse(BaseModel):
    data: LookupData


class LookupByPhoneResponse(BaseModel):
    data: LookupData


class Inbox(BaseModel):
    id: str
    name: str
    description: str | None = None
    type: str | None = None
    user_case: str | None = None
    whatsapp_calls_enabled: bool | None = None


class InboxResponse(BaseModel):
    data: Inbox


class InboxListResponse(BaseModel):
    data: list[Inbox]
    meta: Meta | None = None


class InboxUpdate(BaseModel):
    whatsapp_calls_enabled: bool


class ConversationContactInfo(BaseModel):
    email: str | None = None
    name: str | None = None
    phone: str | None = None


class Conversation(BaseModel):
    id: str
    inbox_id: str
    status: str
    last_activity_at: datetime
    contact_id: int | None = None
    company_id: int | None = None
    assignee_id: int | None = None
    unread_count: int | None = None
    last_message_preview: str | None = None
    contact_info: ConversationContactInfo | None = None
    answered_at: datetime | None = None
    bridged_at: datetime | None = None
    closed_at: datetime | None = None


class ConversationResponse(BaseModel):
    data: Conversation


class ConversationListResponse(BaseModel):
    data: list[Conversation]
    meta: Meta


class ConversationUpdate(BaseModel):
    assignee_id: int | None = None
    contact_id: int | None = None
    company_id: int | None = None
    status: str | None = None


class Message(BaseModel):
    id: str | None = None
    conversation_id: str | None = None
    type: str | None = None
    direction: str | None = None
    author: str | None = None
    user_id: int | None = None
    state: str | None = None
    payload: dict[str, Any] | None = None
    media_url: str | None = None
    error_code: int | None = None
    inserted_at: datetime | None = None
    updated_at: datetime | None = None


class MessageResponse(BaseModel):
    data: Message


class MessageListResponse(BaseModel):
    data: list[Message]
    meta: Meta


class TextMessageCreate(BaseModel):
    text: str


class TemplateHeaderMedia(BaseModel):
    url: str
    filename: str | None = None


class TemplateMessageCreate(BaseModel):
    element_name: str
    language_code: str
    to: str
    conversation_id: str | None = None
    header_media: TemplateHeaderMedia | None = None
    opens_conversation: bool | None = None
    variables: dict[str, str] | None = None


class TemplateMessage(BaseModel):
    id: str
    element_name: str
    language_code: str
    to: str
    state: str
    gsm_id: str | None = None
    category: str | None = None
    inserted_at: datetime | None = None
    contact_id: int | None = None
    company_id: int | None = None
    conversation_id: str | None = None
    message_id: str | None = None


class TemplateMessageResponse(BaseModel):
    data: TemplateMessage


class CardRow(BaseModel):
    type: str | None = None
    text: str | None = None
    label: str | None = None
    link: str | None = None
    user_id: int | None = None
    android: str | None = None
    ios: str | None = None


class CardCreate(BaseModel):
    card: list[CardRow]


class Card(BaseModel):
    call_id: Any | None = None
    card: list[CardRow] = []


class CardResponse(BaseModel):
    data: Card


class CardListResponse(BaseModel):
    data: list[list[CardRow]]


class Disposition(BaseModel):
    id: int
    name: str
    code: str
    outcome: str
    direction: str
    order: int
    active: bool
    description: str | None = None


class DispositionListResponse(BaseModel):
    data: list[Disposition]
    meta: CountMeta | None = None


class DispositionActor(BaseModel):
    user_id: int
    at: datetime | None = None
    name: str | None = None


class DispositionOnCall(BaseModel):
    editable: bool
    edit_window_minutes: int
    disposition_id: int | None = None
    code: str | None = None
    name: str | None = None
    direction: str | None = None
    outcome: str | None = None
    editable_until: datetime | None = None
    set_by: DispositionActor | None = None
    updated_by: DispositionActor | None = None
    ai_suggestion: dict[str, Any] | None = None


class DispositionOnCallResponse(BaseModel):
    data: DispositionOnCall


class DispositionUpdate(BaseModel):
    disposition_id: int | None = None
    disposition_code: str | None = None


class Extension(BaseModel):
    name: str
    number: int | str
    target_id: int
    target_type: str


class ExtensionResponse(BaseModel):
    data: Extension


class ExtensionListResponse(BaseModel):
    data: list[Extension]
    meta: Meta | None = None


class ExtensionCallCreate(BaseModel):
    number_id: int
    callee_number: str
    wait_for_answer: bool | None = None


class ExtensionCall(BaseModel):
    id: str


class Greeting(BaseModel):
    id: int
    name: str
    state: str
    direct_dial_extension: bool | None = None
    input_timeout: int | None = None
    max_input_try_count: int | None = None


class GreetingResponse(BaseModel):
    data: Greeting


class GreetingListResponse(BaseModel):
    data: list[Greeting]
    meta: Meta | None = None


class Number(BaseModel):
    id: int
    name: str
    number: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class NumberResponse(BaseModel):
    data: Number


class NumberListResponse(BaseModel):
    data: list[Number]
    meta: Meta | None = None


class Team(BaseModel):
    id: int
    name: str
    state: str
    strategy: str
    user_case: str | bool
    callback_action: str
    callback: bool | None = None
    callback_dtmf: int | None = None
    locale: str | None = None
    play_announcement: bool | None = None
    say_line_number: bool | None = None
    say_line_number_in_second: int | None = None
    wrap_up_time: int | None = None


class TeamResponse(BaseModel):
    data: Team


class TeamListResponse(BaseModel):
    data: list[Team]
    meta: Meta | None = None


class Voicemail(BaseModel):
    id: int
    name: str


class VoicemailResponse(BaseModel):
    data: Voicemail


class VoicemailListResponse(BaseModel):
    data: list[Voicemail]
    meta: Meta | None = None


class ProcedureCategory(BaseModel):
    id: int | None = None
    name: str | None = None
    slug: str | None = None


class ProcedureVersion(BaseModel):
    number: int | None = None
    published_at: datetime | None = None


class ProcedureStepOption(BaseModel):
    id: int | None = None
    uuid: str | None = None
    label: str | None = None
    order: int | None = None
    terminates: bool | None = None


class ProcedureStepCondition(BaseModel):
    decision_step_id: int | None = None
    option_id: int | None = None


class ProcedureStep(BaseModel):
    uuid: str | None = None
    title: str | None = None
    body: str | None = None
    step_type: str | None = None
    decision_kind: str | None = None
    order: int | None = None
    options: list[ProcedureStepOption] = []
    conditions: list[ProcedureStepCondition] = []
    related_article: dict[str, Any] | None = None


class ProcedureSummary(BaseModel):
    uuid: str
    name: str
    slug: str | None = None
    status: str | None = None
    description: str | None = None
    category: ProcedureCategory | None = None


class ProcedureDetail(ProcedureSummary):
    body: str | None = None
    version: ProcedureVersion | None = None
    steps: list[ProcedureStep] = []


class ProcedureListResponse(BaseModel):
    data: list[ProcedureSummary]


class ProcedureResponse(BaseModel):
    data: ProcedureDetail


class DealLineItem(BaseModel):
    id: int
    name: str
    quantity: float
    unit_price: float
    total: float
    billing_frequency: str
    billing_cycles: int | None = None
    code: str | None = None
    commissionable: bool | None = None
    communications_tax_rate: float | None = None
    discount_type: str | None = None
    discount_value: float | None = None
    excise_duty_type: str | None = None
    excise_duty_value: float | None = None
    position: int | None = None
    product_id: int | None = None
    starts_on: Date | None = None
    unit: str | None = None
    unit_code: str | None = None
    vat_rate: float | None = None
    vat_withholding_rate: float | None = None


class Deal(BaseModel):
    id: int
    name: str
    amount: float | None = None
    arr: float | None = None
    mrr: float | None = None
    currency: str | None = None
    state: str | None = None
    won_at: datetime | None = None
    lost_at: datetime | None = None


class DealDetail(Deal):
    amount_source: str | None = None
    line_items: list[DealLineItem] | None = None


class DealResponse(BaseModel):
    data: DealDetail


class DealListResponse(BaseModel):
    data: list[Deal]
    meta: Meta


class User(BaseModel):
    id: int
    email: str
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    title: str | None = None
    avatar_url: str | None = None
    locale: str | None = None
    timezone: str | None = None
    owner: bool | None = None
    suspended: bool | None = None
    state: str | None = None
    state_changed_at: datetime | None = None
    phone_prefix: str | None = None
    phone_countries: Any | None = None
    default_number: dict[str, Any] | None = None
    signature: str | None = None
    voicemail: bool | None = None
    voicemail_action: str | None = None
    redirect: str | None = None
    redirect_to: str | None = None
    redirect_number: str | None = None


class UserResponse(BaseModel):
    data: User


class UserListResponse(BaseModel):
    data: list[User]
    meta: Meta


class UserUpdate(BaseModel):
    default_number: int | None = None
    state: str | None = None


class DirectionStats(BaseModel):
    count: int
    total_duration: int
    avg_duration: int


class CallStats(BaseModel):
    inbound: DirectionStats
    outbound: DirectionStats


class StateDurations(BaseModel):
    time_to_available: int
    time_to_away: int
    time_to_break: int
    time_to_busy: int
    time_to_remain: int
    time_to_unknown: int


class TodayStats(BaseModel):
    user_id: int
    date: Date
    timezone: str
    calls: CallStats
    states: StateDurations


class TodayStatsResponse(BaseModel):
    data: TodayStats


class ProfileData(BaseModel):
    user: dict[str, Any]
    account: dict[str, Any]
    capabilities: dict[str, Any]
    permissions: list[str]
    roles: list[dict[str, Any]]
    subscription: dict[str, Any] | None = None


class ProfileResponse(BaseModel):
    data: ProfileData


class MobileDeviceCreate(BaseModel):
    device_id: str
    fcm_token: str
    platform: str
    app_version: str
    os_version: str
    apns_token: str | None = None


class MobileDevice(BaseModel):
    device_id: str
    devices_count: int
    do_not_disturb: bool
    registered_at: int
    updated_at: int
    user_id: int


class MobileDeviceUpdate(BaseModel):
    do_not_disturb: bool


class MobileDeviceUpdateResponse(BaseModel):
    device_id: str
    do_not_disturb: bool
    updated_at: int


class MobileDeviceDeleteResponse(BaseModel):
    deleted: bool
    device_id: str
    devices_count: int


class PushTokenCreate(BaseModel):
    token: str
    token_type: str


class PushTokenResponse(BaseModel):
    user_id: int
    token_type: str
    last_seen: int


class SipTokenCreate(BaseModel):
    user_id: int | None = None


class SipTokenResponse(BaseModel):
    user_id: int
    sip_token: str
    sip_username: str
    sip_realm: str
    wss_url: str
    expires_at: int


class AttributionSource(BaseModel):
    url: str
    campaign: str | None = None
    campaignId: str | None = None
    dclid: str | None = None
    fbEventId: str | None = None
    fbc: str | None = None
    fbclid: str | None = None
    fbp: str | None = None
    gbraid: str | None = None
    gclid: str | None = None
    ip: str | None = None
    medium: str | None = None
    mediumId: str | None = None
    msclkid: str | None = None
    occurredAt: datetime | None = None
    referrer: str | None = None
    userAgent: str | None = None
    utmContent: str | None = None
    utmMedium: str | None = None
    utmSource: str | None = None
    wbraid: str | None = None


class AttributionCreate(BaseModel):
    source: AttributionSource
    consent: bool
    companyId: int | None = None
    contactId: int | None = None
    device: str | None = None
    visitorId: str | None = None


class AttributionResponse(BaseModel):
    eventId: int
    linkedEvents: int
    companyId: int | None = None
    contactId: int | None = None


class TaskUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    done: bool | None = None
    assign_to_user_id: int | None = None
    company_ids: list[int] | None = None
    contact_ids: list[int] | None = None
    deal_ids: list[int] | None = None
    due_date: datetime | None = None
    priority: str | None = None
    task_list_id: int | None = None
