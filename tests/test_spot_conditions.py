from kite_forecast.config.spot_conditions import SPOT_CONDITIONS


def test_spot_conditions_have_unique_beach_ids() -> None:
    ids = [conditions.beach_id for conditions in SPOT_CONDITIONS]

    assert len(ids) == len(set(ids))
