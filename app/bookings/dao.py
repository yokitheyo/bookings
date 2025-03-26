from datetime import date

from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exсeptions import RoomFullyBooked
from app.hotels.rooms.models import Rooms
from app.logger import logger


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def find_all_with_images(cls, user_id: int):
        """Get all bookings with room images for a user."""
        async with async_session_maker() as session:
            query = (
                select(
                    Bookings.__table__.columns,
                    Rooms.__table__.columns,
                )
                .join(Rooms, Rooms.id == Bookings.room_id, isouter=True)
                .where(Bookings.user_id == user_id)
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def _check_room_availability(
        cls, session, room_id: int, date_from: date, date_to: date
    ) -> int:
        """Check how many rooms are available for booking."""
        booked_rooms = (
            select(Bookings)
            .where(
                and_(
                    Bookings.room_id == room_id,
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
            )
            .cte("booked_rooms")
        )

        get_rooms_left = (
            select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                    "rooms_left"
                )
            )
            .select_from(Rooms)
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .where(Rooms.id == room_id)
            .group_by(Rooms.quantity, booked_rooms.c.room_id)
        )

        rooms_left = await session.execute(get_rooms_left)
        return rooms_left.scalar()

    @classmethod
    async def _create_booking(
        cls,
        session,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
        price: int,
    ):
        """Create a new booking record."""
        add_booking = (
            insert(Bookings)
            .values(
                room_id=room_id,
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
                price=price,
            )
            .returning(
                Bookings.id,
                Bookings.user_id,
                Bookings.room_id,
                Bookings.date_from,
                Bookings.date_to,
            )
        )

        new_booking = await session.execute(add_booking)
        await session.commit()
        return new_booking.mappings().one()

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        """Add a new booking if room is available."""
        try:
            async with async_session_maker() as session:
                rooms_left = await cls._check_room_availability(
                    session, room_id, date_from, date_to
                )
                logger.debug(f"{rooms_left=}")

                if rooms_left <= 0:
                    raise RoomFullyBooked

                price = await session.scalar(select(Rooms.price).filter_by(id=room_id))

                return await cls._create_booking(
                    session, user_id, room_id, date_from, date_to, price
                )

        except RoomFullyBooked:
            raise
        except (SQLAlchemyError, Exception) as e:
            msg = (
                "Database Exc: Cannot add booking"
                if isinstance(e, SQLAlchemyError)
                else "Unknown Exc: Cannot add booking"
            )
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(msg, extra=extra, exc_info=True)
