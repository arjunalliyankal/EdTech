from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

from app.core.database import connect_to_mongo, close_mongo_connection

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.assessment import router as assessment_router

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(profile_router, prefix="/api/v1/profile", tags=["profile"])
app.include_router(assessment_router, prefix="/api/v1/assessment", tags=["assessment"])

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
base_dir = Path(__file__).resolve().parent.parent.parent
frontend_dir = base_dir / "frontend"

app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="static")
