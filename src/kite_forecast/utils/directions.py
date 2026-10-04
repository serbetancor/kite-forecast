CARDINAL_DIRECTIONS = (
    "N",
    "NNE",
    "NE",
    "ENE",
    "E",
    "ESE",
    "SE",
    "SSE",
    "S",
    "SSW",
    "SW",
    "WSW",
    "W",
    "WNW",
    "NW",
    "NNW",
)


def degrees_to_cardinal(direction_deg: float) -> str:
    normalized_direction = direction_deg % 360
    index = round(normalized_direction / 22.5) % 16
    return CARDINAL_DIRECTIONS[index]
