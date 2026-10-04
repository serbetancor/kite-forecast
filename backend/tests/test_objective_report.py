from datetime import datetime

from kite_forecast.models.beach import Beach
from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.models.location import Location
from kite_forecast.models.marine import MarineObservation
from kite_forecast.models.weather import WeatherObservation
from kite_forecast.reports.objective import build_objective_report


def test_build_objective_report() -> None:
    beach = Beach(
        id="salinas",
        name="Salinas",
        location=Location(
            latitude=27.95,
            longitude=-15.38,
        ),
    )

    timestamp = datetime(2026, 10, 5, 12)

    forecast = HourlyForecast(
        beach=beach,
        timestamp=timestamp,
        weather=WeatherObservation(
            timestamp=timestamp,
            wind_speed_knots=20.5,
            wind_direction_deg=45,
            wind_gusts_knots=28.2,
            temperature_c=24.5,
        ),
        marine=MarineObservation(
            timestamp=timestamp,
            wave_height_m=0.8,
            wave_direction_deg=90,
            wave_period_s=5.5,
            sea_level_height_m=0.3,
            current_velocity_kmh=1.2,
            current_direction_deg=180,
        ),
    )

    report = build_objective_report(forecast)

    assert report.beach == beach
    assert report.timestamp == timestamp

    assert report.wind.speed_knots == 20.5
    assert report.wind.direction_deg == 45
    assert report.wind.direction_cardinal == "NE"
    assert report.wind.gusts_knots == 28.2

    assert report.weather.temperature_c == 24.5

    assert report.waves.height_m == 0.8
    assert report.waves.direction_deg == 90
    assert report.waves.direction_cardinal == "E"
    assert report.waves.period_s == 5.5

    assert report.sea.level_m == 0.3
    assert report.sea.current_velocity_kmh == 1.2
    assert report.sea.current_direction_deg == 180
    assert report.sea.current_direction_cardinal == "S"
