"""Pydantic models used by the toolkit."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class Candidate(BaseModel):
    """Represents a candidate record for validation and reporting."""

    model_config = ConfigDict(extra="forbid")

    STAGES: ClassVar[set[str]] = {
        "new",
        "screen",
        "interview",
        "offer",
        "hired",
        "archived",
    }

    id: int = Field(..., ge=1)
    name: str = Field(..., min_length=1)
    email: EmailStr
    stage: str
    last_contacted_at: datetime
    notes: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = " ".join(part for part in value.strip().split(" ") if part)
        if not cleaned:
            raise ValueError("name must be a non-empty string")
        return cleaned

    @field_validator("stage")
    @classmethod
    def validate_stage(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if cleaned not in cls.STAGES:
            allowed = ", ".join(sorted(cls.STAGES))
            raise ValueError(f"stage must be one of: {allowed}")
        return cleaned

    @field_validator("notes")
    @classmethod
    def validate_notes(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned if cleaned else None


def normalize_name(value: str) -> str:
    """Normalize a name while keeping simple capitalization."""

    return " ".join(part.capitalize() for part in value.strip().split())


def normalize_email(value: str) -> str:
    """Normalize email for storage/reporting."""

    return value.strip().lower()


def summarize_stages(stages: Iterable[str]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for stage in stages:
        summary[stage] = summary.get(stage, 0) + 1
    return summary
