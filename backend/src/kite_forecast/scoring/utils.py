def angular_distance_deg(
    direction_deg: float,
    target_deg: float,
) -> float:
    difference = abs(direction_deg - target_deg) % 360

    return min(difference, 360 - difference)


def linear_score(
    value: float,
    input_min: float,
    input_max: float,
    output_min: float,
    output_max: float,
) -> float:
    if input_min == input_max:
        return output_max

    ratio = (value - input_min) / (input_max - input_min)

    return output_min + ratio * (output_max - output_min)
