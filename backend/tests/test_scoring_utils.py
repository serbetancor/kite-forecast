from kite_forecast.scoring.utils import angular_distance_deg


def test_angular_distance() -> None:
    assert angular_distance_deg(60.0, 60.0) == 0.0
    assert angular_distance_deg(60.0, 70.0) == 10.0
    assert angular_distance_deg(60.0, 30.0) == 30.0


def test_angular_distance_wraps_at_zero() -> None:
    assert angular_distance_deg(350.0, 10.0) == 20.0
    assert angular_distance_deg(10.0, 350.0) == 20.0
