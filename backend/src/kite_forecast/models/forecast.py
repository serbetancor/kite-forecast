from datetime import datetime

from pydantic import BaseModel, model_validator

from kite_forecast.models.beach import Beach


class WeatherObservation(BaseModel):
    timestamp: datetime
    wind_speed_kn: float
    wind_direction_deg: float
    wind_gusts_kn: float
    temperature_c: float


class MarineObservation(BaseModel):
    timestamp: datetime
    wave_height_m: float
    wave_direction_deg: float
    wave_period_s: float
    swell_wave_height_m: float
    swell_wave_direction_deg: float
    swell_wave_period_s: float
    sea_level_height_m: float
    current_velocity_kmh: float
    current_direction_deg: float


class WeatherForecast(BaseModel):
    beach: Beach
    model_latitude: float
    model_longitude: float
    observations: list[WeatherObservation]


class MarineForecast(BaseModel):
    beach: Beach
    model_latitude: float
    model_longitude: float
    observations: list[MarineObservation]


class HourlyForecast(BaseModel):
    beach: Beach
    timestamp: datetime
    weather: WeatherObservation
    marine: MarineObservation


class CachedForecast(BaseModel):
    weather: WeatherForecast
    marine: MarineForecast

    @model_validator(mode="after")
    def validate_matching_beaches(self) -> "CachedForecast":
        if self.weather.beach.id != self.marine.beach.id:
            raise ValueError(
                "Weather and marine forecasts must belong to the same beach"
            )

        return self
