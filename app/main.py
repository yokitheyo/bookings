from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator

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
from app.prometheus.router import router as router_prometheus
from app.importer.router import router as router_import
from app.middleware.process_time import add_process_time_header
from app.core.config import CORS_ORIGINS, CORS_HEADERS, CORS_METHODS


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis_client), prefix="cache")
    yield
    await FastAPICache.clear()
    await redis_client.close()


def create_base_app() -> FastAPI:
    app = FastAPI(
        title="Бронирование Отелей",
        version="0.1.0",
        lifespan=lifespan,
        root_path="/api",
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=CORS_METHODS,
        allow_headers=CORS_HEADERS,
    )

    # Основные роутеры
    routers = [
        router_users,
        router_hotels,
        router_rooms,
        router_bookings,
        router_images,
        router_prometheus,
        router_import,
    ]

    for router in routers:
        app.include_router(router)

    return app


# Создание базового приложения
base_app = create_base_app()

# Добавление версионирования API только для API роутеров
versioned_routers = [
    router_users,
    router_hotels,
    router_rooms,
    router_bookings,
    router_images,
    router_import,
]

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), "static")

# Применяем VersionedFastAPI только к versioned_routers
versioned_app = VersionedFastAPI(
    base_app,
    version_format="{major}",
    prefix_format="/api/v{major}",
    enable_latest=True,
    description="Versioned API for hotel booking system",
)


# Переносим все маршруты из versioned_app в основной app
for route in versioned_app.routes:
    app.routes.append(route)

app.include_router(router_pages)

# Настройка Prometheus
instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)

# Настройка административной панели
admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend,
    title="Административная панель",
    logo_url="/static/admin-logo.png",
    templates_dir="app/admin/templates",
)

# Добавление моделей в админку
admin_views = [UsersAdmin, HotelsAdmin, RoomsAdmin, BookingsAdmin]
for view in admin_views:
    admin.add_view(view)


app.middleware("http")(add_process_time_header)
