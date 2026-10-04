from pydantic import BaseModel, Field


class ComponentScore(BaseModel):
    score: float = Field(ge=0, le=100)
    reason: str


class WindScoreBreakdown(BaseModel):
    speed: float = Field(ge=0, le=100)
    direction: float = Field(ge=0, le=100)
    gusts: float = Field(ge=0, le=100)
    total: float = Field(ge=0, le=100)


class WaveScoreBreakdown(BaseModel):
    height: float = Field(ge=0, le=100)
    period: float = Field(ge=0, le=100)
    direction: float = Field(ge=0, le=100)
    total: float = Field(ge=0, le=100)


class HourlyScore(BaseModel):
    wind: ComponentScore
    waves: ComponentScore
    total: float = Field(ge=0, le=100)


class HourlyScoreResult(BaseModel):
    score: HourlyScore
    wind: WindScoreBreakdown
    waves: WaveScoreBreakdown
