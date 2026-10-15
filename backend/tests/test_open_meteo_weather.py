from kite_forecast.models.forecast import WeatherObservation
from kite_forecast.providers.open_meteo_weather import (
    OpenMeteoWeatherHourly,
    OpenMeteoWeatherResponse,
    to_weather_observations,
)


def test_to_weather_observations() -> None:
    response = OpenMeteoWeatherResponse(
        latitude=27.87346,
        longitude=-15.4053955,
        timezone="Atlantic/Canary",
        hourly=OpenMeteoWeatherHourly(
            time=[
                "2026-10-03T12:00",
                "2026-10-03T13:00",
            ],
            wind_speed_10m=[28.2, 30.5],
            wind_direction_10m=[13.0, 20.0],
            wind_gusts_10m=[59.0, 62.0],
            temperature_2m=[23.3, 23.5],
        ),
    )

    observations = to_weather_observations(response)

    assert len(observations) == 2
    assert all(
        isinstance(observation, WeatherObservation) for observation in observations
    )

    first = observations[0]

    assert first.timestamp.isoformat() == "2026-10-03T12:00:00"
    assert first.wind_speed_kn == 28.2
    assert first.wind_direction_deg == 13.0
    assert first.wind_gusts_kn == 59.0
    assert first.temperature_c == 23.3
