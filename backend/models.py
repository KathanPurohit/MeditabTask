from pydantic import BaseModel, field_validator
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    provider: Optional[str] = "ollama"


    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("message must not be blank")
        return v.strip()


class ChatResponse(BaseModel):
    response: str
    suggestions: list[str]