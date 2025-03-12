from fastapi import APIRouter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking

from typing import List

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("", response_model=List[SBooking])
async def get_bookings():
    return await BookingDAO.find_all()
