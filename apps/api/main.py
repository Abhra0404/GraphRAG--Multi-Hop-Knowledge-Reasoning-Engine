from fastapi import FastAPI

from core.config import settings
from core.health import check_all_services


app = FastAPI(
    title=settings.app_name,
    description="Multi-Hop Knowledge Reasoning Engine",
    version="0.1.0",
)


@app.get("/health")
async def health():
    return check_all_services()