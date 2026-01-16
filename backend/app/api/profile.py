from fastapi import APIRouter, HTTPException, Depends
from app.models.profile import ProfileCreate, ProfileResponse, ProfileInDB
from app.core.database import db
from app.services.auth import create_access_token # Needs a way to get current user
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid credential")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@router.post("/", response_model=ProfileResponse)
async def create_profile(profile: ProfileCreate, user_id: str = Depends(get_current_user_id)):
    profile_data = profile.dict()
    profile_data["user_id"] = user_id
    
    existing_profile = await db.client.edtech_platform.profiles.find_one({"user_id": user_id})
    if existing_profile:
        # Update logic could go here, for now just replace or error
        await db.client.edtech_platform.profiles.update_one({"user_id": user_id}, {"$set": profile_data})
        return profile_data

    await db.client.edtech_platform.profiles.insert_one(profile_data)
    return profile_data

@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(user_id: str = Depends(get_current_user_id)):
    profile = await db.client.edtech_platform.profiles.find_one({"user_id": user_id})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
