from fastapi import FastAPI
from app.routers.iot import router as iot_router
from app.routers.auth import router as auth_router

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(
    iot_router,
    prefix="/api/iot",
    tags=["iot"]
)

app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["auth"]
)

