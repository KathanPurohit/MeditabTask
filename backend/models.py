from pydantic import BaseModel, field_validator


class ChatRequest(BaseModel):
    message: str

    # Minor hardening: reject blank / whitespace-only messages early so the
    # LLM never receives an empty prompt.
    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("message must not be blank")
        return v.strip()


class ChatResponse(BaseModel):
    response: str
    suggestions: list[str]