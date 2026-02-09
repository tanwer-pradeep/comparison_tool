from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import runs
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
def root():
    return {"message": "Welcome to Visual QA API. Visit /docs for OpenAPI docs."}

app.include_router(runs.router, prefix="/api/v1/runs", tags=["runs"])

from fastapi.staticfiles import StaticFiles
import os

# Ensure directory exists for static mount
os.makedirs(settings.ARTIFACTS_DIR, exist_ok=True)

app.mount("/artifacts", StaticFiles(directory=settings.ARTIFACTS_DIR), name="artifacts")

