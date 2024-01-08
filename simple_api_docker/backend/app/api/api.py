from fastapi import APIRouter
from app.api.endpoints import (
    calculate,
    hello
)

api_router = APIRouter()
api_router.include_router(
    hello.router,
    prefix="/hello",
    tags=["hello_word"],
)
api_router.include_router(
    calculate.router,
    prefix="/calculate",
    tags=["math"],
)
