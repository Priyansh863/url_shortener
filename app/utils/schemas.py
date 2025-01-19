from typing import Any, List

from pydantic import BaseModel, HttpUrl


class ResponseModal(BaseModel):
    message: str
    success: bool
    data: Any | None


class URLRequest(BaseModel):
    url: HttpUrl
    expiry_hours: int = 24
    password: str=None


class AccessLog(BaseModel):
    timestamp: str
    ip_address: str
