from datetime import datetime

from pydantic import BaseModel

from kite_forecast.models.beach import Beach
from kite_forecast.models.weather import WeatherForecast, WeatherObservation
from kite_forecast.providers.client import get_json


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


class OpenMeteoWeatherProvider:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    async def get_forecast(
        self,
        beach: Beach,
        timestamp: datetime,
    ) -> WeatherForecast:
        url = (
            f"{self.BASE_URL}"
            f"?latitude={beach.location.latitude}"
            f"&longitude={beach.location.longitude}"
            "&hourly=wind_speed_10m,wind_direction_10m,"
            "wind_gusts_10m,temperature_2m"
            f"&start_date={timestamp.date()}"
            f"&end_date={timestamp.date()}"
            "&timezone=Europe%2FMadrid"
        )

        data = await get_json(url)
        response = OpenMeteoWeatherResponse.model_validate(data)

        forecast = to_weather_forecast(beach, response)

        for observation in forecast.observations:
            if observation.timestamp == timestamp:
                return WeatherForecast(
                    beach=forecast.beach,
                    model_latitude=forecast.model_latitude,
                    model_longitude=forecast.model_longitude,
                    observations=[observation],
                )

        raise ValueError(f"No weather forecast found for {beach.name} at {timestamp}")


def to_weather_observations(
    response: OpenMeteoWeatherResponse,
) -> list[WeatherObservation]:
    hourly = response.hourly

    return [
        WeatherObservation(
            timestamp=datetime.fromisoformat(timestamp),
            wind_speed_kmh=wind_speed,
            wind_direction_deg=wind_direction,
            wind_gusts_kmh=wind_gusts,
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
