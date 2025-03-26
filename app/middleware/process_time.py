import time
from typing import Callable
from fastapi import Request, Response
from app.logger import logger


class ProcessTimeMiddleware:
    async def __call__(
        self, request: Request, call_next: Callable[[Request], Response]
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        logger.info(
            "Время выполнения запроса",
            extra={
                "process_time": round(process_time, 4),
                "path": request.url.path,
                "method": request.method,
            },
        )


async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info(
        "Request execution time", extra={"process_time": round(process_time, 4)}
    )
    return response
