from pydantic import BaseModel
from typing import List


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int

    class Config:
        orm_mode = True


class SHotelInfo(SHotel):
    rooms_left: int
