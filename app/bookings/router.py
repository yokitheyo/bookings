from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SBookingInfo
from app.exсeptions import RoomFullyBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users
from fastapi_versioning import version

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("", response_model=List[SBookingInfo])
async def get_bookings(user: Users = Depends(get_current_user)) -> List[SBookingInfo]:
    """Get all bookings for the current user with room images."""
    return await BookingDAO.find_all_with_images(user_id=user.id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    """Create a new booking and send confirmation email."""
    try:
        booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
        booking_dict = SBooking.model_validate(booking).model_dump()
        send_booking_confirmation_email.delay(booking_dict, user.email)
        return booking_dict
    except RoomFullyBooked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The room is fully booked for the selected dates",
        )


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_booking(
    booking_id: int,
    current_user: Users = Depends(get_current_user),
):
    """Delete a booking for the current user."""
    await BookingDAO.delete(id=booking_id, user_id=current_user.id)
    return {"status": "success"}
