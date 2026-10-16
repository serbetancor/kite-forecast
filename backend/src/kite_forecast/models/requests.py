from datetime import date

from pydantic import BaseModel, Field

from kite_forecast.providers.open_meteo_marine import (
    OpenMeteoMarineResponse,
)
from kite_forecast.providers.open_meteo_weather import (
    OpenMeteoWeatherResponse,
)


class ForecastRequest(BaseModel):
    beach: str
    target_date: date
    time: str
    weather: OpenMeteoWeatherResponse
    marine: OpenMeteoMarineResponse


class KiteSizingRequest(BaseModel):
    beach: str
    target_date: date
    time: str
    weather: OpenMeteoWeatherResponse


class BeachScoreForecast(BaseModel):
    beach_id: str
    weather: OpenMeteoWeatherResponse
    marine: OpenMeteoMarineResponse


class ScoresRequest(BaseModel):
    target_date: date
    forecasts: list[BeachScoreForecast] = Field(min_length=1)
