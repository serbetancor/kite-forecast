from dataclasses import dataclass

from kite_forecast.models.location import Location


@dataclass(frozen=True)
class Beach:
    id: str
    name: str
    location: Location
    # orientation
    # preferred_wind_directions
    # ideal_wind_min
    # ideal_wind_max


BEACHES = (
    Beach(
        id="salinas",
        name="Salinas",
        location=Location(
            latitude=0.0,
            longitude=0.0,
        ),
    ),
    Beach(
        id="vargas",
        name="Vargas",
        location=Location(
            latitude=0.0,
            longitude=0.0,
        ),
    ),
    Beach(
        id="bocababarranco",
        name="Bocababarranco",
        location=Location(
            latitude=0.0,
            longitude=0.0,
        ),
    ),
    Beach(
        id="las-burras",
        name="Las Burras",
        location=Location(
            latitude=0.0,
            longitude=0.0,
        ),
    ),
    Beach(
        id="castillo-del-romeral",
        name="Castillo del Romeral",
        location=Location(
            latitude=0.0,
            longitude=0.0,
        ),
    ),
    Beach(
        id="el-burrero",
        name="El Burrero",
        location=Location(
            latitude=0.0,
            longitude=0.0,
        ),
    ),
    Beach(
        id="punta-de-maspalomas",
        name="Punta de Maspalomas",
        location=Location(
            latitude=0.0,
            longitude=0.0,
        ),
    ),
)
