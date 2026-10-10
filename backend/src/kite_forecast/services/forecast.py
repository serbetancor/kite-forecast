from datetime import datetime

from kite_forecast.models.beach import Beach
from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.models.kite_sizing import KiteSizingMatrix
from kite_forecast.providers.forecast_builder import build_hourly_forecasts
from kite_forecast.providers.open_meteo_marine import OpenMeteoMarineProvider
from kite_forecast.providers.open_meteo_weather import OpenMeteoWeatherProvider
from kite_forecast.reports.objective import (
    ObjectiveReport,
    build_objective_report,
)
from kite_forecast.services.kite_sizing import build_kite_sizing_matrix
from kite_forecast.services.spot_scoring import score_forecast


class ForecastService:
    def __init__(self) -> None:
        self.weather_provider = OpenMeteoWeatherProvider()
        self.marine_provider = OpenMeteoMarineProvider()

    async def _get_hourly_forecast(
        self,
        beach: Beach,
        timestamp: datetime,
    ) -> HourlyForecast:
        weather_forecast = await self.weather_provider.get_forecast(
            beach,
            timestamp,
        )

        marine_forecast = await self.marine_provider.get_forecast(
            beach,
            timestamp,
        )

        forecasts = build_hourly_forecasts(
            weather_forecast,
            marine_forecast,
        )

        if not forecasts:
            raise ValueError(f"No forecast found for {beach.name} at {timestamp}")

        return forecasts[0]

    async def get_forecast(
        self,
        beach: Beach,
        timestamp: datetime,
    ) -> ObjectiveReport:
        forecast = await self._get_hourly_forecast(beach, timestamp)
        score = score_forecast(forecast)
        return build_objective_report(forecast, score)

    async def get_kite_sizing(
        self,
        beach: Beach,
        timestamp: datetime,
    ) -> KiteSizingMatrix:
        forecast = await self._get_hourly_forecast(beach, timestamp)
        return build_kite_sizing_matrix(forecast)
