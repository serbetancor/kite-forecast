from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic import ValidationError

from kite_forecast.models.scored_forecast import (
    ScoreCache as ScoreCacheModel,
)
from kite_forecast.models.scored_forecast import (
    ScoredHour,
)

TIMEZONE = ZoneInfo("Atlantic/Canary")


class ScoreCacheError(RuntimeError):
    """Raised when cached scores are unavailable or invalid."""


class ScoreCacheService:
    def __init__(self, path: Path | None = None) -> None:
        self.path = (
            path
            if path is not None
            else Path(__file__).resolve().parents[3] / "data" / "scores.json"
        )

    def _load(self) -> ScoreCacheModel:
        try:
            return ScoreCacheModel.model_validate_json(
                self.path.read_text(encoding="utf-8")
            )
        except FileNotFoundError as error:
            raise ScoreCacheError("Score cache is not available") from error
        except (OSError, ValidationError) as error:
            raise ScoreCacheError("Score cache is invalid or unreadable") from error

    @staticmethod
    def _normalize_datetime(timestamp: datetime) -> datetime:
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            return timestamp.replace(tzinfo=TIMEZONE)

        return timestamp.astimezone(TIMEZONE)

    def get_score(self, beach_id: str, timestamp: datetime):
        target = self._normalize_datetime(timestamp)
        cache = self._load()

        for entry in cache.entries:
            if (
                entry.beach_id == beach_id
                and self._normalize_datetime(entry.datetime) == target
            ):
                return entry.score

        raise ScoreCacheError(
            f"No cached score found for beach {beach_id} at {target.isoformat()}"
        )

    def get_scores(
        self,
        beach_id: str | None = None,
        target_date: date | None = None,
    ) -> list[ScoredHour]:
        cache = self._load()
        entries = cache.entries

        if beach_id is not None:
            entries = [entry for entry in entries if entry.beach_id == beach_id]

        if target_date is not None:
            entries = [
                entry
                for entry in entries
                if self._normalize_datetime(entry.datetime).date() == target_date
            ]

        entries = [
            entry
            for entry in entries
            if 7 <= self._normalize_datetime(entry.datetime).hour <= 19
        ]

        return sorted(
            entries,
            key=lambda entry: (
                self._normalize_datetime(entry.datetime),
                entry.beach_id,
            ),
        )
