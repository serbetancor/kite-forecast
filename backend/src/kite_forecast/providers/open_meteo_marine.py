from datetime import datetime

from pydantic import BaseModel

from kite_forecast.models.beach import Beach
from kite_forecast.models.forecast import MarineForecast, MarineObservation
from kite_forecast.providers.client import get_json


class OpenMeteoMarineHourly(BaseModel):
    time: list[str]
    wave_height: list[float | None]
    wave_direction: list[float | None]
    wave_period: list[float | None]
    swell_wave_height: list[float | None]
    swell_wave_direction: list[float | None]
    swell_wave_period: list[float | None]
    sea_level_height_msl: list[float | None]
    ocean_current_velocity: list[float | None]
    ocean_current_direction: list[float | None]


class OpenMeteoMarineResponse(BaseModel):
    latitude: float
    longitude: float
    timezone: str
    hourly: OpenMeteoMarineHourly


def to_marine_observations(
    hourly: OpenMeteoMarineHourly,
) -> list[MarineObservation]:
    observations: list[MarineObservation] = []

    for (
        timestamp,
        wave_height,
        wave_direction,
        wave_period,
        swell_wave_height,
        swell_wave_direction,
        swell_wave_period,
        sea_level_height,
        current_velocity,
        current_direction,
    ) in zip(
        hourly.time,
        hourly.wave_height,
        hourly.wave_direction,
        hourly.wave_period,
        hourly.swell_wave_height,
        hourly.swell_wave_direction,
        hourly.swell_wave_period,
        hourly.sea_level_height_msl,
        hourly.ocean_current_velocity,
        hourly.ocean_current_direction,
    ):
        observations.append(
            MarineObservation(
                timestamp=datetime.fromisoformat(timestamp),
                wave_height_m=wave_height,
                wave_direction_deg=wave_direction,
                wave_period_s=wave_period,
                swell_wave_height_m=swell_wave_height,
                swell_wave_direction_deg=swell_wave_direction,
                swell_wave_period_s=swell_wave_period,
                sea_level_height_m=sea_level_height,
                current_velocity_kmh=current_velocity,
                current_direction_deg=current_direction,
            )
        )

    return observations


def to_marine_forecast(
    beach: Beach,
    response: OpenMeteoMarineResponse,
) -> MarineForecast:
    return MarineForecast(
        beach=beach,
        model_latitude=response.latitude,
        model_longitude=response.longitude,
        observations=to_marine_observations(response.hourly),
    )


class OpenMeteoMarineProvider:
    BASE_URL = "https://marine-api.open-meteo.com/v1/marine"

    async def get_forecast(
        self,
        beach: Beach,
        timestamp: datetime,
    ) -> MarineForecast:
        url = (
            f"{self.BASE_URL}"
            f"?latitude={beach.location.latitude}"
            f"&longitude={beach.location.longitude}"
            "&hourly=wave_height,wave_direction,wave_period,"
            "swell_wave_height,swell_wave_direction,swell_wave_period,"
            "sea_level_height_msl,ocean_current_velocity,ocean_current_direction"
            f"&start_date={timestamp.date()}"
            f"&end_date={timestamp.date()}"
            "&timezone=Atlantic%2FCanary"
        )

        data = await get_json(url)
        response = OpenMeteoMarineResponse.model_validate(data)

        forecast = to_marine_forecast(beach, response)

        for observation in forecast.observations:
            if observation.timestamp == timestamp:
                return MarineForecast(
                    beach=forecast.beach,
                    model_latitude=forecast.model_latitude,
                    model_longitude=forecast.model_longitude,
                    observations=[observation],
                )

        raise ValueError(f"No marine forecast found for {beach.name} at {timestamp}")
