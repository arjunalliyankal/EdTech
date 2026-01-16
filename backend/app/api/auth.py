from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserResponse, UserInDB
from app.services.auth import get_password_hash, verify_password, create_access_token
from app.core.database import db

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
async def create_user(user: UserCreate):
    existing_user = await db.client.edtech_platform.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(
        **user.dict(),
        hashed_password=hashed_password
    )
    
    new_user = await db.client.edtech_platform.users.insert_one(user_in_db.dict(by_alias=True))
    created_user = await db.client.edtech_platform.users.find_one({"_id": new_user.inserted_id})
    return UserResponse(id=str(created_user["_id"]), email=created_user["email"], role=created_user["role"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Login attempt for: {form_data.username}")
    user = await db.client.edtech_platform.users.find_one({"email": form_data.username})
    
    if not user:
        print(f"Login failed: User {form_data.username} not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not verify_password(form_data.password, user["hashed_password"]):
        print(f"Login failed: Password mismatch for {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"Login successful for: {form_data.username}")
    access_token = create_access_token(subject=user["_id"])
    return {"access_token": access_token, "token_type": "bearer", "role": user["role"]}
