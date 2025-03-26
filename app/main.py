from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router import router as router_users
from app.middleware.process_time import add_process_time_header
from app.core.config import CORS_ORIGINS, CORS_HEADERS, CORS_METHODS


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = aioredis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        encoding="utf-8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis_client), prefix="cache")
    yield
    await redis_client.close()


def create_application() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title="Бронирование Отелей",
        version="0.1.0",
        root_path="/api",
    )

    # Подключаем статические файлы
    app.mount("/static", StaticFiles(directory="app/static"), "static")

    # Подключаем маршруты
    app.include_router(router_users)
    app.include_router(router_hotels)
    app.include_router(router_rooms)
    app.include_router(router_bookings)
    app.include_router(router_pages)
    app.include_router(router_images)

    # Добавляем CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=CORS_METHODS,
        allow_headers=CORS_HEADERS,
    )

    # Добавляем middleware для отслеживания времени выполнения запроса
    app.middleware("http")(add_process_time_header)

    # Настраиваем панель администратора
    admin = Admin(app, engine, authentication_backend=authentication_backend)
    admin.add_view(UsersAdmin)
    admin.add_view(HotelsAdmin)
    admin.add_view(RoomsAdmin)
    admin.add_view(BookingsAdmin)

    return app


app = create_application()
