from datetime import datetime

from kite_forecast.models.beach import Beach
from kite_forecast.providers.forecast_builder import build_hourly_forecasts
from kite_forecast.providers.open_meteo_marine import OpenMeteoMarineProvider
from kite_forecast.providers.open_meteo_weather import OpenMeteoWeatherProvider
from kite_forecast.reports.objective import (
    ObjectiveReport,
    build_objective_report,
)


class ForecastService:
    def __init__(self) -> None:
        self.weather_provider = OpenMeteoWeatherProvider()
        self.marine_provider = OpenMeteoMarineProvider()

    async def get_forecast(
        self,
        beach: Beach,
        timestamp: datetime,
    ) -> ObjectiveReport:
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

        return build_objective_report(forecasts[0])
