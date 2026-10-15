from pathlib import Path

from pydantic import ValidationError

from kite_forecast.models.beach import Beach
from kite_forecast.models.forecast import CachedForecast


class ForecastCacheError(RuntimeError):
    """Raised when a cached forecast cannot be loaded or validated."""


class ForecastCache:
    def __init__(self, directory: Path | None = None) -> None:
        self.directory = (
            directory
            if directory is not None
            else Path(__file__).resolve().parents[3] / "data" / "forecasts"
        )

    def get_forecast(self, beach: Beach) -> CachedForecast:
        path = self.directory / f"{beach.id}.json"

        try:
            forecast = CachedForecast.model_validate_json(
                path.read_text(encoding="utf-8")
            )
        except FileNotFoundError as error:
            raise ForecastCacheError(
                f"No cached forecast available for {beach.name}"
            ) from error
        except (OSError, ValidationError) as error:
            raise ForecastCacheError(
                f"Cached forecast for {beach.name} is invalid or unreadable"
            ) from error

        if (
            forecast.weather.beach.id != beach.id
            or forecast.marine.beach.id != beach.id
        ):
            raise ForecastCacheError(f"Cached forecast does not match beach {beach.id}")

        return forecast
