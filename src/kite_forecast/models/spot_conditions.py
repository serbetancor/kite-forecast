from pydantic import BaseModel, Field, model_validator


class WindScoreWeights(BaseModel):
    speed: float = Field(ge=0)
    direction: float = Field(ge=0)
    gusts: float = Field(ge=0)

    @model_validator(mode="after")
    def weights_must_sum_to_one(self) -> "WindScoreWeights":
        total = self.speed + self.direction + self.gusts

        if abs(total - 1.0) > 1e-9:
            raise ValueError("Wind score weights must sum to 1")

        return self


class WaveScoreWeights(BaseModel):
    height: float = Field(ge=0)
    period: float = Field(ge=0)
    direction: float = Field(ge=0)

    @model_validator(mode="after")
    def weights_must_sum_to_one(self) -> "WaveScoreWeights":
        total = self.height + self.period + self.direction

        if abs(total - 1.0) > 1e-9:
            raise ValueError("Wave score weights must sum to 1")

        return self


class WindConditions(BaseModel):
    preferred_directions_deg: tuple[float, ...]
    direction_tolerance_deg: float = Field(gt=0, le=180)

    min_speed_knots: float = Field(ge=0)
    ideal_speed_knots: float = Field(ge=0)
    max_speed_knots: float = Field(ge=0)
    max_gust_knots: float = Field(ge=0)

    score_weights: WindScoreWeights


class WaveConditions(BaseModel):
    preferred_directions_deg: tuple[float, ...]
    direction_tolerance_deg: float = Field(gt=0, le=180)

    min_height_m: float = Field(ge=0)
    ideal_height_m: float = Field(ge=0)
    max_height_m: float = Field(ge=0)

    min_period_s: float = Field(ge=0)

    score_weights: WaveScoreWeights


class SpotConditions(BaseModel):
    beach_id: str
    wind: WindConditions
    waves: WaveConditions


class WeatherScoreWeights(BaseModel):
    temperature: float = Field(ge=0)

    @model_validator(mode="after")
    def weights_must_sum_to_one(self) -> "WeatherScoreWeights":
        total = self.temperature

        if abs(total - 1.0) > 1e-9:
            raise ValueError("Weather score weights must sum to 1")

        return self


class WeatherConditions(BaseModel):
    min_temperature_c: float
    ideal_temperature_c: float
    max_temperature_c: float

    score_weights: WeatherScoreWeights
