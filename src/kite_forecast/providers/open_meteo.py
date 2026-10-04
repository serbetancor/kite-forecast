from datetime import datetime

from pydantic import BaseModel

from kite_forecast.models.beach import Beach
from kite_forecast.models.marine import MarineForecast, MarineObservation
from kite_forecast.providers.client import get_json


class OpenMeteoHourly(BaseModel):
    time: list[str]
    wave_height: list[float | None]
    wave_direction: list[float | None]
    wave_period: list[float | None]
    sea_level_height_msl: list[float | None]
    ocean_current_velocity: list[float | None]
    ocean_current_direction: list[float | None]


class OpenMeteoMarineResponse(BaseModel):
    latitude: float
    longitude: float
    timezone: str
    hourly: OpenMeteoHourly


class OpenMeteoMarineProvider:
    BASE_URL = "https://marine-api.open-meteo.com/v1/marine"

    async def get_forecasts(
        self,
        beaches: tuple[Beach, ...],
    ) -> list[MarineForecast]:
        latitudes = ",".join(str(beach.location.latitude) for beach in beaches)
        longitudes = ",".join(str(beach.location.longitude) for beach in beaches)

        url = (
            f"{self.BASE_URL}"
            f"?latitude={latitudes}"
            f"&longitude={longitudes}"
            "&hourly=wave_height,wave_direction,wave_period,"
            "sea_level_height_msl,ocean_current_velocity,ocean_current_direction"
            "&forecast_days=2"
            "&timezone=Europe%2FMadrid"
        )

        data = await get_json(url)

        if isinstance(data, list):
            locations = [
                OpenMeteoMarineResponse.model_validate(location) for location in data
            ]
        else:
            locations = [OpenMeteoMarineResponse.model_validate(data)]

        return [
            to_marine_forecast(beach, response)
            for beach, response in zip(beaches, locations)
        ]


def to_marine_observations(
    response: OpenMeteoMarineResponse,
) -> list[MarineObservation]:
    hourly = response.hourly

    return [
        MarineObservation(
            timestamp=datetime.fromisoformat(timestamp),
            wave_height_m=wave_height,
            wave_direction_deg=wave_direction,
            wave_period_s=wave_period,
            sea_level_height_m=sea_level_height,
            current_velocity_kmh=current_velocity,
            current_direction_deg=current_direction,
        )
        for (
            timestamp,
            wave_height,
            wave_direction,
            wave_period,
            sea_level_height,
            current_velocity,
            current_direction,
        ) in zip(
            hourly.time,
            hourly.wave_height,
            hourly.wave_direction,
            hourly.wave_period,
            hourly.sea_level_height_msl,
            hourly.ocean_current_velocity,
            hourly.ocean_current_direction,
        )
    ]


def to_marine_forecast(
    beach: Beach,
    response: OpenMeteoMarineResponse,
) -> MarineForecast:
    return MarineForecast(
        beach=beach,
        model_latitude=response.latitude,
        model_longitude=response.longitude,
        observations=to_marine_observations(response),
    )
