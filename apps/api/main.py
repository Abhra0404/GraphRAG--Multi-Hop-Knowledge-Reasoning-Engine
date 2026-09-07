from fastapi import FastAPI

from core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="Multi-Hop Knowledge Reasoning Engine",
    version="0.1.0",
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
    }