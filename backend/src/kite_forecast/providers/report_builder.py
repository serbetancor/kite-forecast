from kite_forecast.models.forecast import HourlyForecast
from kite_forecast.models.report import (
    ObjectiveReport,
    SeaReport,
    SwellReport,
    WavesReport,
    WeatherReport,
    WindReport,
)
from kite_forecast.models.score import HourlyScore
from kite_forecast.utils.directions import degrees_to_cardinal
from kite_forecast.models.report import TideReport


def build_report(
    forecast: HourlyForecast,
    score: HourlyScore,
    tide: TideReport,
) -> ObjectiveReport:
    weather = forecast.weather
    marine = forecast.marine

    return ObjectiveReport(
        beach=forecast.beach,
        timestamp=forecast.timestamp,
        wind=WindReport(
            speed_kn=weather.wind_speed_kn,
            direction_deg=weather.wind_direction_deg,
            direction_cardinal=degrees_to_cardinal(weather.wind_direction_deg),
            gusts_kn=weather.wind_gusts_kn,
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
        swell=SwellReport(
            height_m=marine.swell_wave_height_m,
            direction_deg=marine.swell_wave_direction_deg,
            direction_cardinal=degrees_to_cardinal(marine.swell_wave_direction_deg),
            period_s=marine.swell_wave_period_s,
        ),
        tide=tide,
        sea=SeaReport(
            level_m=marine.sea_level_height_m,
            current_velocity_kmh=marine.current_velocity_kmh,
            current_direction_deg=marine.current_direction_deg,
            current_direction_cardinal=degrees_to_cardinal(
                marine.current_direction_deg,
            ),
        ),
        score=score,
    )
