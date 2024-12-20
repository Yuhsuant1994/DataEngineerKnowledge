from app.api.api import api_router
from fastapi import FastAPI


def get_app() -> FastAPI:
    app = FastAPI(title="Demo search engin")

    app.include_router(api_router, prefix="/api")
    return app


app = get_app()


if __name__ == "__main__":
    get_app()
