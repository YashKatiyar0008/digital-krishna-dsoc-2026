"""Public request and response schemas for Digital Krishna AI.

This sanitized DSOC implementation contains no API keys, private
endpoints, user records, or production configuration.
"""

from typing import Literal

from pydantic import BaseModel, Field, field_validator


LanguageCode = Literal["en", "hi", "hinglish"]
SourceStatus = Literal["reviewed", "none"]


class GuidanceRequest(BaseModel):
    """Validated request sent by the Digital Krishna interface."""

    message: str = Field(
        ...,
        min_length=3,
        max_length=2_000,
        description="The concern or reflection shared by the user.",
    )
    language: LanguageCode = Field(
        default="en",
        description="Preferred response language.",
    )

    @field_validator("message")
    @classmethod
    def clean_message(cls, value: str) -> str:
        """Remove unnecessary whitespace and reject empty input."""

        cleaned = " ".join(value.split())

        if len(cleaned) < 3:
            raise ValueError("Please provide a meaningful message.")

        return cleaned


class ScriptureSource(BaseModel):
    """Reviewed scripture information attached to a response."""

    status: SourceStatus = "none"
    reference: str | None = Field(
        default=None,
        description="For example: Bhagavad Gita 2.47.",
    )
    original_text: str | None = None
    translation: str | None = None
    review_note: str | None = Field(
        default=None,
        description="Information about the review status of the source.",
    )


class PracticalStep(BaseModel):
    """A small action the user can apply in everyday life."""

    title: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=3, max_length=500)


class GuidanceResponse(BaseModel):
    """Structured guidance returned to the frontend."""

    request_id: str = Field(
        ...,
        description="Anonymous identifier used for request tracing.",
    )
    category: str = Field(..., min_length=2, max_length=100)
    language: LanguageCode

    acknowledgement: str = Field(
        ...,
        min_length=5,
        max_length=1_000,
    )

    scripture: ScriptureSource

    explanation: str = Field(
        ...,
        min_length=5,
        max_length=2_000,
    )

    practical_steps: list[PracticalStep] = Field(
        ...,
        min_length=1,
        max_length=5,
    )

    reflection_question: str = Field(
        ...,
        min_length=5,
        max_length=500,
    )

    safety_note: str | None = Field(
        default=None,
        max_length=1_000,
    )

    disclaimer: str = Field(
        default=(
            "Digital Krishna provides spiritual reflection and "
            "educational guidance. It does not replace qualified "
            "professional or emergency support."
        )
    )


class ErrorResponse(BaseModel):
    """Safe error response returned when processing fails."""

    error: str
    message: str
    request_id: str | None = None
