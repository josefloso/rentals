from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select

from app.core.database import get_db
from app.models import Property, User
from app.schemas import PropertyCreate, PropertyOut
from app.core.security import get_current_user

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.post("/", response_model=PropertyOut, status_code=status.HTTP_201_CREATED)
async def create_property(
    property: PropertyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new property listing"""
    db_property = Property(**property.dict(), owner_id=current_user.id)
    db.add(db_property)
    await db.commit()
    await db.refresh(db_property)
    return db_property

@router.get("/", response_model=List[PropertyOut])
async def get_properties(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all property listings"""
    result = await db.execute(select(Property).offset(skip).limit(limit))
    return result.scalars().all()