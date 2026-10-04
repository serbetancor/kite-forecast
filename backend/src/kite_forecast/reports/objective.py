from datetime import datetime

from pydantic import BaseModel

from kite_forecast.models.beach import Beach
from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.utils.directions import degrees_to_cardinal


class WindReport(BaseModel):
    speed_knots: float
    direction_deg: float
    direction_cardinal: str
    gusts_knots: float


class WeatherReport(BaseModel):
    temperature_c: float


class WavesReport(BaseModel):
    height_m: float
    direction_deg: float
    direction_cardinal: str
    period_s: float


class SeaReport(BaseModel):
    level_m: float
    current_velocity_kmh: float
    current_direction_deg: float
    current_direction_cardinal: str


class ObjectiveReport(BaseModel):
    beach: Beach
    timestamp: datetime
    wind: WindReport
    weather: WeatherReport
    waves: WavesReport
    sea: SeaReport


def build_objective_report(
    forecast: HourlyForecast,
) -> ObjectiveReport:
    weather = forecast.weather
    marine = forecast.marine

    return ObjectiveReport(
        beach=forecast.beach,
        timestamp=forecast.timestamp,
        wind=WindReport(
            speed_knots=weather.wind_speed_knots,
            direction_deg=weather.wind_direction_deg,
            direction_cardinal=degrees_to_cardinal(weather.wind_direction_deg),
            gusts_knots=weather.wind_gusts_knots,
        ),
        weather=WeatherReport(
            temperature_c=weather.temperature_c,
        ),
        waves=WavesReport(
            height_m=marine.wave_height_m,
            direction_deg=marine.wave_direction_deg,
            direction_cardinal=degrees_to_cardinal(marine.wave_direction_deg),
            period_s=marine.wave_period_s,
        ),
        sea=SeaReport(
            level_m=marine.sea_level_height_m,
            current_velocity_kmh=marine.current_velocity_kmh,
            current_direction_deg=marine.current_direction_deg,
            current_direction_cardinal=degrees_to_cardinal(
                marine.current_direction_deg
            ),
        ),
    )
