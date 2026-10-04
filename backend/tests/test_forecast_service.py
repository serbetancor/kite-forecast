import asyncio
from datetime import datetime
from unittest.mock import AsyncMock

from kite_forecast.models.beach import Beach
from kite_forecast.models.location import Location
from kite_forecast.models.marine import MarineForecast, MarineObservation
from kite_forecast.models.weather import WeatherForecast, WeatherObservation
from kite_forecast.services.forecast import ForecastService


def create_beach() -> Beach:
    return Beach(
        id="test",
        name="Test Beach",
        location=Location(
            latitude=27.95,
            longitude=-15.38,
        ),
    )


def create_weather_forecast(beach: Beach) -> WeatherForecast:
    timestamp = datetime(2026, 10, 5, 12)

    return WeatherForecast(
        beach=beach,
        model_latitude=beach.location.latitude,
        model_longitude=beach.location.longitude,
        observations=[
            WeatherObservation(
                timestamp=timestamp,
                wind_speed_knots=20.0,
                wind_direction_deg=45,
                wind_gusts_knots=25.0,
                temperature_c=24.0,
            )
        ],
    )


def create_marine_forecast(beach: Beach) -> MarineForecast:
    timestamp = datetime(2026, 10, 5, 12)

    return MarineForecast(
        beach=beach,
        model_latitude=beach.location.latitude,
        model_longitude=beach.location.longitude,
        observations=[
            MarineObservation(
                timestamp=timestamp,
                wave_height_m=0.8,
                wave_direction_deg=90,
                wave_period_s=5.0,
                sea_level_height_m=0.3,
                current_velocity_kmh=1.0,
                current_direction_deg=180,
            )
        ],
    )


def test_get_forecast() -> None:
    beach = create_beach()
    timestamp = datetime(2026, 10, 5, 12)

    service = ForecastService()

    service.weather_provider.get_forecast = AsyncMock(
        return_value=create_weather_forecast(beach)
    )

    service.marine_provider.get_forecast = AsyncMock(
        return_value=create_marine_forecast(beach)
    )

    report = asyncio.run(
        service.get_forecast(
            beach,
            timestamp,
        )
    )

    assert report.beach == beach
    assert report.timestamp == timestamp

    assert report.wind.speed_knots == 20.0
    assert report.wind.direction_cardinal == "NE"

    assert report.waves.height_m == 0.8
    assert report.waves.direction_cardinal == "E"

    assert report.sea.current_velocity_kmh == 1.0
    assert report.sea.current_direction_cardinal == "S"

    service.weather_provider.get_forecast.assert_awaited_once_with(
        beach,
        timestamp,
    )
    service.marine_provider.get_forecast.assert_awaited_once_with(
        beach,
        timestamp,
    )
