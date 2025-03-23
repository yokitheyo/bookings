from pydantic import BaseModel, ConfigDict
from typing import List


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)


class SHotelInfo(SHotel):
    rooms_left: int
