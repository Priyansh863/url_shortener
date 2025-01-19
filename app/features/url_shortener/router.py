from app.features.url_shortener.repository import UrlShortenerRepository
from fastapi import APIRouter, Request
from app.utils.schemas import URLRequest, ResponseModal
from datetime import datetime

url_shortener_router = APIRouter(tags=["url_shortener"], prefix="/url_shortener")
repo = UrlShortenerRepository()  


@url_shortener_router.post("/shorten", response_model=ResponseModal)
async def shorten_url(request: URLRequest):
    return await repo.create_shortened_url(
        request.url, request.password,request.expiry_hours
    )


@url_shortener_router.get("/")
async def redirect_to_url(short_url: str, request: Request,password:str=None):
    print(request.client.host, "request.client.hostrequest.client.host")
    return await repo.get_original_url(short_url, request.client.host, password)


@url_shortener_router.get("/analytics/", response_model=ResponseModal)
async def get_analytics(short_url: str):
    return await repo.get_access_logs(short_url)
