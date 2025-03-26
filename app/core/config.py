from typing import List

# Конфигурация CORS
CORS_ORIGINS: List[str] = [
    "http://localhost",
    "http://localhost:3000",
]

CORS_METHODS: List[str] = [
    "GET",
    "POST",
    "OPTIONS",
    "DELETE",
    "PATCH",
    "PUT",
]

CORS_HEADERS: List[str] = [
    "Content-Type",
    "Set_Cookie",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin",
    "Authorization",
]
