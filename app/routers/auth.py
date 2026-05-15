from app.settings import settings
from datetime import datetime, timedelta, UTC

from fastapi import APIRouter, HTTPException
from jose import jwt
from pydantic import BaseModel

router = APIRouter()

FAKE_USER = "admin"
FAKE_PASSWORD = "admin123"

settings.JWT_EXPIRE_MINUTES
settings.JWT_SECRET_KEY
settings.JWT_ALGORITHM

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    if data.username != FAKE_USER or data.password != FAKE_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    expires_at = datetime.now(UTC) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

    payload = {
        "sub": data.username,
        "exp": expires_at
    }
    token = jwt.encode(payload,settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
