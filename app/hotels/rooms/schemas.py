from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str] = None
    price: int
    services: List[str]
    quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)


class SRoomInfo(SRoom):
    total_cost: int
    rooms_left: int

    model_config = ConfigDict(from_attributes=True)
