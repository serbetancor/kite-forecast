from pydantic import BaseModel, ConfigDict

from kite_forecast.models.location import Location


class Beach(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    location: Location
