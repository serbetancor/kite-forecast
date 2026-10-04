from kite_forecast.utils.directions import degrees_to_cardinal


def test_degrees_to_cardinal() -> None:
    assert degrees_to_cardinal(0) == "N"
    assert degrees_to_cardinal(22.5) == "NNE"
    assert degrees_to_cardinal(45) == "NE"
    assert degrees_to_cardinal(90) == "E"
    assert degrees_to_cardinal(180) == "S"
    assert degrees_to_cardinal(270) == "W"
    assert degrees_to_cardinal(337.5) == "NNW"


def test_degrees_to_cardinal_wraps_around() -> None:
    assert degrees_to_cardinal(360) == "N"
    assert degrees_to_cardinal(370) == "N"
    assert degrees_to_cardinal(-10) == "N"
