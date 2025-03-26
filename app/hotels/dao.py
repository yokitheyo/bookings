from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):
        """
        Finds all available hotels in a specific location for a given date range.

        The query works in three steps:
        1. Find all booked rooms for the date range
        2. Calculate how many rooms are left in each hotel
        3. Return hotels that have available rooms in the specified location
        """
        # Step 1: Find all booked rooms for the date range
        booked_rooms = cls._get_booked_rooms_cte(date_from, date_to)

        # Step 2: Calculate rooms left in each hotel
        booked_hotels = cls._get_booked_hotels_cte(booked_rooms)

        # Step 3: Get hotels with available rooms in the specified location
        hotels_query = cls._get_hotels_with_rooms_query(booked_hotels, location)

        async with async_session_maker() as session:
            hotels_with_rooms = await session.execute(hotels_query)
            return hotels_with_rooms.mappings().all()

    @staticmethod
    def _get_booked_rooms_cte(date_from: date, date_to: date):
        """Creates a CTE for booked rooms in the specified date range."""
        return (
            select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
            .select_from(Bookings)
            .where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to,
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from,
                    ),
                ),
            )
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )

    @staticmethod
    def _get_booked_hotels_cte(booked_rooms):
        """Creates a CTE for hotels with the number of available rooms."""
        return (
            select(
                Rooms.hotel_id,
                func.sum(
                    Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)
                ).label("rooms_left"),
            )
            .select_from(Rooms)
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .group_by(Rooms.hotel_id)
            .cte("booked_hotels")
        )

    @staticmethod
    def _get_hotels_with_rooms_query(booked_hotels, location: str):
        """Creates a query to get hotels with available rooms in the specified location."""
        return (
            select(
                Hotels.__table__.columns,
                booked_hotels.c.rooms_left,
            )
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id, isouter=True)
            .where(
                and_(
                    booked_hotels.c.rooms_left > 0,
                    Hotels.location.like(f"%{location}%"),
                )
            )
        )
