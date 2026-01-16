from typing import List, Union
from pydantic import AnyHttpUrl, EmailStr, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "EdTech Platform"
    
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:8000", "http://127.0.0.1:8000", "http://localhost:5500", "http://127.0.0.1:5500"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "edtech_platform"
    
    JWT_SECRET_KEY: str = "CHANGE_THIS_SECRET_KEY_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GEMINI_API_KEY: str = ""

    class Config:
        case_sensitive = True
        # Go up 3 levels from app/core/config.py to reach root (where .env is)
        # However, backend/ is where we run uvicorn, so .env is one level up from backend
        # Let's rely on a more robust path determination
        import os
        from pathlib import Path
        
        # Determine the base directory (backend directory)
        # config.py is in app/core/, so we go up 2 levels to get to backend/
        # But .env is in inkrithackthon/ which is parent of backend/
        
        # Assuming uvicorn is run from backend/, .env is at ../.env
        # But let's be safe and use absolute path
        
        # file: backend/app/core/config.py
        # parent: backend/app/core
        # parent.parent: backend/app
        # parent.parent.parent: backend
        # parent.parent.parent.parent: inkrithackthon (where .env is)
        
        _base_dir = Path(__file__).resolve().parent.parent.parent.parent
        env_file = str(_base_dir / ".env")

settings = Settings()
