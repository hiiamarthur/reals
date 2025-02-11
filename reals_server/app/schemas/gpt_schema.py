import json
from typing import List, Optional, Dict, Any, Mapping
from pydantic import BaseModel, Field


from app.schemas.base_schema import BaseSchema

# Define the pydantic models for the response structure


class Message(BaseSchema):
    role: str
    content: str
    refusal: Optional[str] = None


class ChatCompletionMessage(BaseSchema):
    content: str
    role: str
    refusal: Optional[Any] = None
    function_call: Optional[Dict] = None
    tool_calls: Optional[List] = None


class Choice(BaseSchema):
    finish_reason: str
    index: int
    message: ChatCompletionMessage
    logprobs: Optional[Any] = None

    def to_json(self) -> str:
        json_str = super().to_json()
        json_dict = json.loads(json_str)
        json_dict.pop("created_at")
        json_dict.pop("updated_at")
        return json.dumps(json_dict)


class PromptTokensDetails(BaseSchema):
    cached_tokens: int = 0
    audio_tokens: int = 0


class CompletionTokensDetails(BaseSchema):
    reasoning_tokens: int = 0
    audio_tokens: int = 0
    accepted_prediction_tokens: int = 0
    rejected_prediction_tokens: int = 0


class CompletionUsageDetails(BaseSchema):
    cached_tokens: int = 0
    audio_tokens: int = 0
    reasoning_tokens: int = 0
    accepted_prediction_tokens: int = 0
    rejected_prediction_tokens: int = 0


class CompletionUsage(BaseSchema):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    prompt_tokens_details: Dict[str, int]
    completion_tokens_details: Dict[str, int]


class OpenAIRequest(BaseSchema):
    user_id: str
    session_id: Optional[str] = None
    content: str


class OpenAIResponse(BaseSchema):
    id: str
    choices: Optional[List[Choice]] = None
    created: Optional[int] = None
    model: Optional[str] = None
    object: Optional[str] = None
    service_tier: Optional[str] = None
    system_fingerprint: Optional[str] = None
    usage: Optional[CompletionUsage] = None

    class Config:
        extra = "allow"  # Allow extra fields


class OpenAIHeaders(BaseSchema):
    openai_organization: Optional[str] = Field(None, alias="openai-organization")
    openai_processing_ms: Optional[int] = Field(None, alias="openai-processing-ms")
    openai_version: Optional[str] = Field(None, alias="openai-version")
    x_request_id: Optional[str] = Field(None, alias="x-request-id")
    x_ratelimit_limit_requests: Optional[int] = Field(
        None, alias="x-ratelimit-limit-requests"
    )
    x_ratelimit_limit_tokens: Optional[int] = Field(
        None, alias="x-ratelimit-limit-tokens"
    )
    x_ratelimit_remaining_requests: Optional[int] = Field(
        None, alias="x-ratelimit-remaining-requests"
    )
    x_ratelimit_remaining_tokens: Optional[int] = Field(
        None, alias="x-ratelimit-remaining-tokens"
    )
    x_ratelimit_reset_requests: Optional[str] = Field(
        None, alias="x-ratelimit-reset-requests"
    )
    x_ratelimit_reset_tokens: Optional[str] = Field(
        None, alias="x-ratelimit-reset-tokens"
    )

    @classmethod
    def from_headers(cls, headers: Mapping[str, str]) -> "OpenAIHeaders":
        """Create OpenAIHeaders from a headers mapping, taking only the fields we need"""
        header_fields = {
            "openai-organization",
            "openai-processing-ms",
            "openai-version",
            "x-request-id",
            "x-ratelimit-limit-requests",
            "x-ratelimit-limit-tokens",
            "x-ratelimit-remaining-requests",
            "x-ratelimit-remaining-tokens",
            "x-ratelimit-reset-requests",
            "x-ratelimit-reset-tokens",
        }

        # Extract only the headers we want, if they exist
        header_dict = {key: headers.get(key) for key in header_fields if key in headers}

        return cls(**header_dict)

    class Config:
        populate_by_name = True
        extra = "allow"
