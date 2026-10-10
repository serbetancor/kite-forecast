from pydantic import BaseModel, Field


class ComponentScore(BaseModel):
    total: float = Field(ge=0, le=100)


class WindScore(ComponentScore):
    speed: float = Field(ge=0, le=100)
    direction: float = Field(ge=0, le=100)
    gusts: float = Field(ge=0, le=100)


class WaveScore(ComponentScore):
    height: float = Field(ge=0, le=100)
    period: float = Field(ge=0, le=100)
    direction: float = Field(ge=0, le=100)


class HourlyScore(BaseModel):
    total: float = Field(ge=0, le=100)
    wind: WindScore
    waves: WaveScore
