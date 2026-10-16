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
