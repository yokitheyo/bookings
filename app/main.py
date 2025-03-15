from fastapi import FastAPI, Query, Depends
from typing import Optional
from datetime import date
from pydantic import BaseModel

from app.users.router import router as router_users
from app.bookings.router import router as router_bookings
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms

app = FastAPI()

app.include_router(router_rooms)
app.include_router(router_hotels)
app.include_router(router_users)
app.include_router(router_bookings)
