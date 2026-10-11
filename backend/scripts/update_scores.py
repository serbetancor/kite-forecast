import json
import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from kite_forecast.config.beaches import BEACHES
from kite_forecast.models.cached_forecast import CachedForecast
from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.models.scored_forecast import ScoreCache, ScoredHour
from kite_forecast.services.spot_scoring import score_forecast

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[1]
FORECASTS_DIR = BASE_DIR / "data" / "forecasts"
SCORES_FILE = BASE_DIR / "data" / "scores.json"
TIMEZONE = ZoneInfo("Atlantic/Canary")


def _ensure_timezone(timestamp: datetime) -> datetime:
    """Interpret naive timestamps as local forecast times."""
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        return timestamp.replace(tzinfo=TIMEZONE)

    return timestamp.astimezone(TIMEZONE)


def _load_forecast(path: Path) -> CachedForecast:
    forecast = CachedForecast.model_validate_json(path.read_text(encoding="utf-8"))

    if path.stem != forecast.weather.beach.id:
        raise ValueError(
            f"Forecast filename {path.name!r} does not match "
            f"beach ID {forecast.weather.beach.id!r}"
        )

    return forecast


def _score_beach(
    beach_id: str,
    path: Path,
) -> list[ScoredHour]:
    forecast = _load_forecast(path)

    weather_observations = {
        _ensure_timezone(observation.timestamp): observation.model_copy(
            update={"timestamp": _ensure_timezone(observation.timestamp)}
        )
        for observation in forecast.weather.observations
    }
    marine_observations = {
        _ensure_timezone(observation.timestamp): observation.model_copy(
            update={"timestamp": _ensure_timezone(observation.timestamp)}
        )
        for observation in forecast.marine.observations
    }
    if len(weather_observations) != len(forecast.weather.observations):
        raise ValueError(f"{beach_id}: duplicate weather timestamps")

    if len(marine_observations) != len(forecast.marine.observations):
        raise ValueError(f"{beach_id}: duplicate marine timestamps")

    weather_timestamps = set(weather_observations)
    marine_timestamps = set(marine_observations)
    matching_timestamps = sorted(weather_timestamps & marine_timestamps)

    if not matching_timestamps:
        raise ValueError(f"{beach_id}: no matching weather and marine timestamps")

    unmatched_weather = weather_timestamps - marine_timestamps
    unmatched_marine = marine_timestamps - weather_timestamps

    if unmatched_weather or unmatched_marine:
        logger.warning(
            "[%s] Skipping unmatched timestamps: %d weather, %d marine",
            beach_id,
            len(unmatched_weather),
            len(unmatched_marine),
        )

    entries: list[ScoredHour] = []

    for timestamp in matching_timestamps:
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError(f"{beach_id}: timestamp {timestamp!s} has no timezone")

        hourly_forecast = HourlyForecast(
            beach=forecast.weather.beach,
            timestamp=timestamp,
            weather=weather_observations[timestamp],
            marine=marine_observations[timestamp],
        )

        entries.append(
            ScoredHour(
                beach_id=beach_id,
                datetime=timestamp,
                score=score_forecast(hourly_forecast),
            )
        )

    logger.info("[%s] Calculated %d hourly scores", beach_id, len(entries))
    return entries


def _write_atomically(cache: ScoreCache, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump(
                cache.model_dump(mode="json"),
                temporary_file,
                ensure_ascii=False,
                indent=2,
            )
            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        temporary_path.replace(destination)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    expected_beach_ids = {beach.id for beach in BEACHES}
    if not expected_beach_ids:
        raise ValueError("No beaches configured")

    if not FORECASTS_DIR.is_dir():
        raise FileNotFoundError(f"Forecast directory not found: {FORECASTS_DIR}")

    forecast_paths = {path.stem: path for path in FORECASTS_DIR.glob("*.json")}

    actual_beach_ids = set(forecast_paths)
    missing = expected_beach_ids - actual_beach_ids
    unexpected = actual_beach_ids - expected_beach_ids

    if missing or unexpected:
        raise ValueError(
            f"Forecast files do not match configured beaches. "
            f"Missing: {sorted(missing)}; "
            f"unexpected: {sorted(unexpected)}"
        )

    entries: list[ScoredHour] = []

    for beach_id in sorted(expected_beach_ids):
        entries.extend(_score_beach(beach_id, forecast_paths[beach_id]))

    if not entries:
        raise ValueError("No hourly scores were generated")

    entries.sort(key=lambda entry: (entry.datetime, entry.beach_id))

    cache = ScoreCache(
        generated_at=datetime.now(TIMEZONE),
        entries=entries,
    )

    _write_atomically(cache, SCORES_FILE)

    logger.info(
        "Wrote %d scores for %d beaches to %s",
        len(entries),
        len(expected_beach_ids),
        SCORES_FILE,
    )


if __name__ == "__main__":
    main()
