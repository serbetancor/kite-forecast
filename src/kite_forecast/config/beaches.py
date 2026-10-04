from kite_forecast.models.beach import Beach
from kite_forecast.models.location import Location

BEACHES: tuple[Beach, ...] = (
    Beach(
        id="salinas",
        name="Salinas",
        location=Location(
            latitude=27.818078,
            longitude=-15.421142,
        ),
    ),
    Beach(
        id="vargas",
        name="Vargas",
        location=Location(
            latitude=27.8883,
            longitude=-15.3938,
        ),
    ),
    Beach(
        id="bocabarranco",
        name="Bocabarranco",
        location=Location(
            latitude=28.03182,
            longitude=-15.39614,
        ),
    ),
    Beach(
        id="las-burras",
        name="Las Burras",
        location=Location(
            latitude=27.7655,
            longitude=-15.5529,
        ),
    ),
    Beach(
        id="castillo-del-romeral",
        name="Castillo del Romeral",
        location=Location(
            latitude=27.7973,
            longitude=-15.4631,
        ),
    ),
    Beach(
        id="el-burrero",
        name="El Burrero",
        location=Location(
            latitude=27.9106,
            longitude=-15.3865,
        ),
    ),
    Beach(
        id="punta-de-maspalomas",
        name="Punta de Maspalomas",
        location=Location(
            latitude=27.73885,
            longitude=-15.56943,
        ),
    ),
)
