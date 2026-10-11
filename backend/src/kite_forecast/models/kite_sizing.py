from datetime import datetime

from pydantic import BaseModel, Field


class KiteSizingCell(BaseModel):
    weight_kg: int = Field(ge=40, le=120)
    kite_size_m2: int = Field(ge=4, le=21)
    score: float = Field(ge=0, le=100)


class KiteSizingMatrix(BaseModel):
    timestamp: datetime
    wind_speed_kmh: float
    wind_gusts_kmh: float
    weights_kg: list[int]
    kite_sizes_m2: list[int]
    cells: list[KiteSizingCell]
