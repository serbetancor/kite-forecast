from datetime import datetime

from pydantic import BaseModel

from kite_forecast.models.beach import Beach
from kite_forecast.models.forecast import WeatherForecast, WeatherObservation


class OpenMeteoWeatherHourly(BaseModel):
    time: list[str]
    wind_speed_10m: list[float]
    wind_direction_10m: list[float]
    wind_gusts_10m: list[float]
    temperature_2m: list[float]


class OpenMeteoWeatherResponse(BaseModel):
    latitude: float
    longitude: float
    timezone: str
    hourly: OpenMeteoWeatherHourly


def to_weather_observations(
    response: OpenMeteoWeatherResponse,
) -> list[WeatherObservation]:
    hourly = response.hourly

    return [
        WeatherObservation(
            timestamp=datetime.fromisoformat(timestamp),
            wind_speed_kn=wind_speed,
            wind_direction_deg=wind_direction,
            wind_gusts_kn=wind_gusts,
            temperature_c=temperature,
        )
        for (
            timestamp,
            wind_speed,
            wind_direction,
            wind_gusts,
            temperature,
        ) in zip(
            hourly.time,
            hourly.wind_speed_10m,
            hourly.wind_direction_10m,
            hourly.wind_gusts_10m,
            hourly.temperature_2m,
        )
    ]


def to_weather_forecast(
    beach: Beach,
    response: OpenMeteoWeatherResponse,
) -> WeatherForecast:
    return WeatherForecast(
        beach=beach,
        model_latitude=response.latitude,
        model_longitude=response.longitude,
        observations=to_weather_observations(response),
    )
