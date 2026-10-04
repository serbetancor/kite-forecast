import pytest

from kite_forecast.models.spot_conditions import (
    WaveConditions,
    WaveScoreWeights,
)
from kite_forecast.scoring.wave import (
    score_wave_direction,
    score_wave_height,
    score_wave_period,
    score_waves,
)

CONDITIONS = WaveConditions(
    preferred_directions_deg=(60.0,),
    direction_tolerance_deg=30.0,
    min_height_m=0.5,
    ideal_height_m=1.0,
    max_height_m=2.0,
    min_period_s=5.0,
    score_weights=WaveScoreWeights(
        height=0.5,
        period=0.3,
        direction=0.2,
    ),
)


def test_wave_height_below_minimum() -> None:
    assert score_wave_height(0.3, CONDITIONS) == 0.0


def test_wave_height_at_minimum() -> None:
    assert score_wave_height(0.5, CONDITIONS) == 0.0


def test_wave_height_at_ideal() -> None:
    assert score_wave_height(1.0, CONDITIONS) == 100.0


def test_wave_height_at_maximum() -> None:
    assert score_wave_height(2.0, CONDITIONS) == 0.0


def test_wave_height_above_maximum() -> None:
    assert score_wave_height(2.5, CONDITIONS) == 0.0


def test_wave_height_between_minimum_and_ideal() -> None:
    assert score_wave_height(0.75, CONDITIONS) == 50.0


def test_wave_period_below_minimum() -> None:
    assert score_wave_period(4.0, CONDITIONS) == 0.0


def test_wave_period_at_minimum() -> None:
    assert score_wave_period(5.0, CONDITIONS) == 100.0


def test_wave_period_above_minimum() -> None:
    assert score_wave_period(8.0, CONDITIONS) == 100.0


def test_wave_score() -> None:
    score = score_waves(
        height_m=1.0,
        direction_deg=60.0,
        period_s=8.0,
        conditions=CONDITIONS,
    )

    assert score.total == 100.0


def test_wave_score_with_short_period() -> None:
    score = score_waves(
        height_m=1.0,
        direction_deg=60.0,
        period_s=4.0,
        conditions=CONDITIONS,
    )

    assert score.total == pytest.approx(70.0)


def test_wave_direction_at_preferred_direction() -> None:
    assert score_wave_direction(60.0, CONDITIONS) == 100.0


def test_wave_direction_at_tolerance_boundary() -> None:
    assert score_wave_direction(30.0, CONDITIONS) == 0.0


def test_wave_direction_inside_tolerance() -> None:
    assert score_wave_direction(45.0, CONDITIONS) == 50.0


def test_wave_direction_wraps_at_zero() -> None:
    conditions = CONDITIONS.model_copy(update={"preferred_directions_deg": (350.0,)})

    assert score_wave_direction(10.0, conditions) == pytest.approx(33.33333333333333)
