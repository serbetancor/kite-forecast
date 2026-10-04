from kite_forecast.config.beaches import BEACHES
from kite_forecast.models.marine import MarineObservation
from kite_forecast.providers.open_meteo import (
    OpenMeteoHourly,
    OpenMeteoMarineResponse,
    to_marine_forecast,
    to_marine_observations,
)


def test_to_marine_observations() -> None:
    response = OpenMeteoMarineResponse(
        latitude=27.791664,
        longitude=-15.458328,
        timezone="Europe/Madrid",
        hourly=OpenMeteoHourly(
            time=[
                "2026-10-03T12:00",
                "2026-10-03T13:00",
            ],
            wave_height=[1.24, 1.18],
            wave_direction=[53.0, 55.0],
            wave_period=[5.9, 6.1],
            sea_level_height_msl=[-0.62, -0.55],
            ocean_current_velocity=[1.5, 1.7],
            ocean_current_direction=[234.0, 230.0],
        ),
    )

    observations = to_marine_observations(response)

    assert len(observations) == 2
    assert all(
        isinstance(observation, MarineObservation) for observation in observations
    )

    first = observations[0]

    assert first.timestamp.isoformat() == "2026-10-03T12:00:00"
    assert first.wave_height_m == 1.24
    assert first.wave_direction_deg == 53.0
    assert first.wave_period_s == 5.9
    assert first.sea_level_height_m == -0.62
    assert first.current_velocity_kmh == 1.5
    assert first.current_direction_deg == 234.0


def test_to_marine_forecast() -> None:
    beach = BEACHES[0]

    response = OpenMeteoMarineResponse(
        latitude=27.791664,
        longitude=-15.458328,
        timezone="Europe/Madrid",
        hourly=OpenMeteoHourly(
            time=["2026-10-03T12:00"],
            wave_height=[1.24],
            wave_direction=[53.0],
            wave_period=[5.9],
            sea_level_height_msl=[-0.62],
            ocean_current_velocity=[1.5],
            ocean_current_direction=[234.0],
        ),
    )

    forecast = to_marine_forecast(beach, response)

    assert forecast.beach == beach
    assert forecast.model_latitude == 27.791664
    assert forecast.model_longitude == -15.458328
    assert len(forecast.observations) == 1
    assert forecast.observations[0].wave_height_m == 1.24
