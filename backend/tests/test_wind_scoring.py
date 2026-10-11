import pytest

from kite_forecast.models.spot_conditions import WindConditions, WindScoreWeights
from kite_forecast.scoring.wind import (
    score_wind,
    score_wind_direction,
    score_wind_gusts,
    score_wind_speed,
)

CONDITIONS = WindConditions(
    preferred_directions_deg=(60.0,),
    direction_tolerance_deg=30.0,
    min_speed_kmh=15.0,
    ideal_speed_kmh=22.0,
    max_speed_kmh=30.0,
    max_gust_kmh=35.0,
    score_weights=WindScoreWeights(
        speed=0.5,
        direction=0.3,
        gusts=0.2,
    ),
)


def test_wind_speed_below_minimum() -> None:
    assert score_wind_speed(10.0, CONDITIONS) == 0.0


def test_wind_speed_at_minimum() -> None:
    assert score_wind_speed(15.0, CONDITIONS) == 0.0


def test_wind_speed_at_ideal() -> None:
    assert score_wind_speed(22.0, CONDITIONS) == 100.0


def test_wind_speed_at_maximum() -> None:
    assert score_wind_speed(30.0, CONDITIONS) == 0.0


def test_wind_speed_above_maximum() -> None:
    assert score_wind_speed(35.0, CONDITIONS) == 0.0


def test_wind_speed_between_minimum_and_ideal() -> None:
    assert score_wind_speed(18.5, CONDITIONS) == 50.0


def test_wind_speed_between_ideal_and_maximum() -> None:
    assert score_wind_speed(26.0, CONDITIONS) == 50.0


def test_wind_direction_at_preferred_direction() -> None:
    assert score_wind_direction(60.0, CONDITIONS) == 100.0


def test_wind_direction_at_tolerance_boundary() -> None:
    assert score_wind_direction(30.0, CONDITIONS) == 0.0


def test_wind_direction_inside_tolerance() -> None:
    assert score_wind_direction(45.0, CONDITIONS) == 50.0


def test_wind_direction_uses_closest_preferred_direction() -> None:
    conditions = CONDITIONS.model_copy(
        update={
            "preferred_directions_deg": (60.0, 120.0),
        }
    )

    score = score_wind_direction(110.0, conditions)

    assert score == pytest.approx(66.66666666666667)


def test_wind_gusts_below_maximum() -> None:
    assert score_wind_gusts(30.0, CONDITIONS) == 100.0


def test_wind_gusts_at_maximum() -> None:
    assert score_wind_gusts(35.0, CONDITIONS) == 100.0


def test_wind_gusts_above_maximum() -> None:
    assert score_wind_gusts(36.0, CONDITIONS) == 0.0


def test_wind_score() -> None:
    score = score_wind(
        speed_kmh=22.0,
        direction_deg=60.0,
        gust_speed_kmh=30.0,
        conditions=CONDITIONS,
    )

    assert score.total == 100.0


def test_wind_score_with_bad_direction() -> None:
    score = score_wind(
        speed_kmh=22.0,
        direction_deg=30.0,
        gust_speed_kmh=30.0,
        conditions=CONDITIONS,
    )

    assert score.total == 70.0


def test_wind_score_with_excessive_gusts() -> None:
    score = score_wind(
        speed_kmh=22.0,
        direction_deg=60.0,
        gust_speed_kmh=40.0,
        conditions=CONDITIONS,
    )

    assert score.total == 80.0
