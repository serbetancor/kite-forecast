from datetime import datetime

from kite_forecast.models.beach import Beach
from kite_forecast.models.forecast import (
    MarineForecast,
    WeatherForecast,
)
from kite_forecast.models.kite_sizing import KiteSizingMatrix
from kite_forecast.models.report import ObjectiveReport
from kite_forecast.models.score import HourlyScore
from kite_forecast.providers.forecast_builder import build_hourly_forecasts
from kite_forecast.providers.report_builder import build_report
from kite_forecast.services.kite_sizing import build_kite_sizing_matrix
from kite_forecast.services.spot_scoring import score_forecast
from kite_forecast.services.tides import TideService


class ForecastService:
    def __init__(self) -> None:
        self.tide_service = TideService()

    @staticmethod
    def _get_hourly_forecast(
        weather_forecast: WeatherForecast,
        marine_forecast: MarineForecast,
        timestamp: datetime,
    ):
        forecasts = build_hourly_forecasts(
            weather_forecast,
            marine_forecast,
        )

        for forecast in forecasts:
            if forecast.timestamp == timestamp:
                return forecast

        raise ValueError(
            f"No forecast found for {weather_forecast.beach.name} at {timestamp}"
        )

    def get_forecast(
        self,
        beach: Beach,
        timestamp: datetime,
        weather_forecast: WeatherForecast,
        marine_forecast: MarineForecast,
    ) -> ObjectiveReport:
        if (
            weather_forecast.beach.id != beach.id
            or marine_forecast.beach.id != beach.id
        ):
            raise ValueError("Forecast data does not match the selected beach")

        forecast = self._get_hourly_forecast(
            weather_forecast,
            marine_forecast,
            timestamp,
        )

        score: HourlyScore = score_forecast(forecast)
        tide = self.tide_service.get_tide_report(
            marine_forecast,
            timestamp,
        )

        return build_report(
            forecast=forecast,
            score=score,
            tide=tide,
        )

    def get_kite_sizing(
        self,
        beach: Beach,
        timestamp: datetime,
        weather_forecast: WeatherForecast,
    ) -> KiteSizingMatrix:
        if weather_forecast.beach.id != beach.id:
            raise ValueError("Weather data does not match the selected beach")

        observation = next(
            (
                item
                for item in weather_forecast.observations
                if item.timestamp == timestamp
            ),
            None,
        )

        if observation is None:
            raise ValueError(
                f"No weather observation found for {beach.name} at {timestamp}"
            )

        return build_kite_sizing_matrix(observation)
