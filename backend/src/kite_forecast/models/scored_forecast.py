from datetime import datetime

from pydantic import BaseModel, model_validator

from kite_forecast.models.score import HourlyScore


class ScoredHour(BaseModel):
    """Score for one beach at one forecast hour."""

    beach_id: str
    datetime: datetime
    score: HourlyScore

    @model_validator(mode="after")
    def validate_timezone(self) -> "ScoredHour":
        if self.datetime.tzinfo is None or self.datetime.utcoffset() is None:
            raise ValueError("Scored hour datetime must be timezone-aware")

        return self


def _validate_unique_entries(entries: list[ScoredHour]) -> None:
    """Ensure each beach has at most one score per forecast timestamp."""

    keys: list[tuple[str, datetime]] = [
        (entry.beach_id, entry.datetime) for entry in entries
    ]

    if len(keys) != len(set(keys)):
        raise ValueError("Score cache contains duplicate beach and datetime entries")


class ScoreCache(BaseModel):
    """Persisted scores for all beaches and forecast hours."""

    generated_at: datetime
    entries: list[ScoredHour]

    @model_validator(mode="after")
    def validate_cache(self) -> "ScoreCache":
        if self.generated_at.tzinfo is None or self.generated_at.utcoffset() is None:
            raise ValueError("Cache generation datetime must be timezone-aware")

        _validate_unique_entries(self.entries)

        return self
