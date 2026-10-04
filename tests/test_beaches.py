from kite_forecast.config.beaches import BEACHES


def test_we_have_seven_beaches() -> None:
    assert len(BEACHES) == 7


def test_all_beaches_have_unique_ids() -> None:
    ids = [beach.id for beach in BEACHES]

    assert len(ids) == len(set(ids))


def test_all_beaches_have_valid_coordinates() -> None:
    for beach in BEACHES:
        assert -90 <= beach.location.latitude <= 90
        assert -180 <= beach.location.longitude <= 180
