from datetime import datetime

from kite_forecast.models.beach import Beach
from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.models.kite_sizing import KiteSizingMatrix
from kite_forecast.providers.forecast_builder import build_hourly_forecasts
from kite_forecast.reports.objective import (
    ObjectiveReport,
    build_objective_report,
)
from kite_forecast.services.forecast_cache import ForecastCache
from kite_forecast.services.kite_sizing import build_kite_sizing_matrix
from kite_forecast.services.score_cache import ScoreCacheService


class ForecastService:
    def __init__(
        self,
        cache: ForecastCache | None = None,
        score_cache: ScoreCacheService | None = None,
    ) -> None:
        self.cache = cache if cache is not None else ForecastCache()
        self.score_cache = (
            score_cache if score_cache is not None else ScoreCacheService()
        )

    async def _get_hourly_forecast(
        self,
        beach: Beach,
        timestamp: datetime,
    ) -> HourlyForecast:
        cached_forecast = self.cache.get_forecast(beach)

        forecasts = build_hourly_forecasts(
            cached_forecast.weather,
            cached_forecast.marine,
        )

        for forecast in forecasts:
            if forecast.timestamp == timestamp:
                return forecast

        raise ValueError(f"No forecast found for {beach.name} at {timestamp}")

    async def get_forecast(
        self,
        beach: Beach,
        timestamp: datetime,
    ) -> ObjectiveReport:
        forecast = await self._get_hourly_forecast(beach, timestamp)
        score = self.score_cache.get_score(beach.id, forecast.timestamp)

        return build_objective_report(forecast, score)

    async def get_kite_sizing(
        self,
        beach: Beach,
        timestamp: datetime,
    ) -> KiteSizingMatrix:
        forecast = await self._get_hourly_forecast(beach, timestamp)
        return build_kite_sizing_matrix(forecast)
