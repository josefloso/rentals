from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  # ✅ Add this
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.auth import security, verify_token

router = APIRouter(tags=["auth"])

@router.post("/login")
async def login(db: AsyncSession = Depends(get_db)):
    # Your actual login logic here
    return {"message": "Login endpoint"}

@router.get("/protected")
async def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user_id = verify_token(credentials)
    return {"user": user_id}