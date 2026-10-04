from datetime import datetime

from kite_forecast.config.beaches import BEACHES
from kite_forecast.models.marine import MarineForecast, MarineObservation
from kite_forecast.models.weather import WeatherForecast, WeatherObservation
from kite_forecast.providers.forecast_builder import build_hourly_forecasts


def test_build_hourly_forecasts_matches_by_timestamp() -> None:
    beach = BEACHES[0]

    weather_forecast = WeatherForecast(
        beach=beach,
        model_latitude=27.87346,
        model_longitude=-15.4053955,
        observations=[
            WeatherObservation(
                timestamp=datetime(2026, 10, 3, 12),
                wind_speed_knots=28.2,
                wind_direction_deg=13.0,
                wind_gusts_knots=59.0,
                temperature_c=23.3,
            ),
            WeatherObservation(
                timestamp=datetime(2026, 10, 3, 13),
                wind_speed_knots=30.5,
                wind_direction_deg=20.0,
                wind_gusts_knots=62.0,
                temperature_c=23.5,
            ),
        ],
    )

    marine_forecast = MarineForecast(
        beach=beach,
        model_latitude=27.791664,
        model_longitude=-15.458328,
        observations=[
            MarineObservation(
                timestamp=datetime(2026, 10, 3, 13),
                wave_height_m=1.18,
                wave_direction_deg=55.0,
                wave_period_s=6.1,
                sea_level_height_m=-0.55,
                current_direction_deg=230.0,
                current_velocity_kmh=1.7 * 1.852,
            ),
            MarineObservation(
                timestamp=datetime(2026, 10, 3, 14),
                wave_height_m=1.20,
                wave_direction_deg=56.0,
                wave_period_s=6.2,
                sea_level_height_m=-0.50,
                current_velocity_kmh=1.8 * 1.852,
                current_direction_deg=228.0,
            ),
        ],
    )

    forecasts = build_hourly_forecasts(
        weather_forecast,
        marine_forecast,
    )

    assert len(forecasts) == 1

    forecast = forecasts[0]

    assert forecast.timestamp == datetime(2026, 10, 3, 13)
    assert forecast.weather.wind_speed_knots == 30.5
    assert forecast.marine.wave_height_m == 1.18
