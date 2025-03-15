from fastapi import APIRouter, Depends

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking

from typing import List

from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get(
    "",
)  # response_model=List[SBooking]
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingDAO.find_all(user_id=1)
