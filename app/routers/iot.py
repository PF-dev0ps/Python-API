import os
from app.settings import settings
from jose import JWTError, jwt
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field
from datetime import datetime, UTC

router = APIRouter()

metrics_history = []


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

from app.settings import settings
settings.API_KEY

class SensorData(BaseModel):
    device: str = Field(..., min_length=3, max_length=50)
    temperature: float = Field(..., ge=-20, le=80)
    humidity: float = Field(..., ge=0, le=100)

class MetricResponse(BaseModel):
    device: str
    temperature: float
    humidity: float
    received_at: str


class MetricsListResponse(BaseModel):
    count: int
    items: list[MetricResponse]

@router.post("/metrics", status_code=201)
def receive_metrics(
    data: SensorData,
    x_api_key: str | None = Header(default=None)
):

    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    metric = {
        "device": data.device,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "received_at": datetime.now(UTC).isoformat()
    }

    metrics_history.append(metric)

    return {
        "message": "metric received",
        "metric": metric
    }


@router.get("/latest", response_model=MetricResponse)
def get_latest_metric():
    if not metrics_history:
        raise HTTPException(status_code=404, detail="No metrics received yet")

    return metrics_history[-1]



@router.get("/metrics", response_model=MetricsListResponse)
def get_metrics(
    authorization: str | None = Header(default=None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid bearer token")

    return {
        "count": len(metrics_history),
        "items": metrics_history
    }
