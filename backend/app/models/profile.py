from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from bson import ObjectId

class ProfileBase(BaseModel):
    current_skills: List[str] = []
    interests: List[str] = []
    career_goals: str
    preferred_pace: str = "medium" # slow, medium, fast

class ProfileCreate(ProfileBase):
    pass

class ProfileInDB(ProfileBase):
    user_id: str
    
    model_config = ConfigDict(
        from_attributes=True
    )

class ProfileResponse(ProfileBase):
    user_id: str
