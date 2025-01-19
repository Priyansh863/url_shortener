from contextlib import asynccontextmanager
from app.database import init_db
from app.features.url_shortener import router
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.features.url_shortener.router import url_shortener_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield  # Start request handling


def get_application():
    _app = FastAPI(
        title="test",
        lifespan=lifespan,
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    routes = APIRouter()
    routes.include_router(router=url_shortener_router)
    _app.include_router(routes, prefix="/api/v1")

    return _app


app = get_application()
