from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field
from datetime import datetime, UTC

router = APIRouter()

metrics_history = []

API_KEY = "super-secret-lab-key"


class SensorData(BaseModel):
    device: str = Field(..., min_length=3, max_length=50)
    temperature: float = Field(..., ge=-20, le=80)
    humidity: float = Field(..., ge=0, le=100)


@router.post("/metrics", status_code=201)
def receive_metrics(
    data: SensorData,
    x_api_key: str | None = Header(default=None)
):
    if x_api_key != API_KEY:
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


@router.get("/latest")
def get_latest_metric():
    if not metrics_history:
        raise HTTPException(status_code=404, detail="No metrics received yet")

    return metrics_history[-1]


@router.get("/metrics")
def get_metrics():
    return {
        "count": len(metrics_history),
        "items": metrics_history
    }
