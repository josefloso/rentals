from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.core.database import get_db
from app.models import Booking, Property, User
from app.schemas import BookingCreate, BookingOut
from app.core.security import get_current_user

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new booking"""
    # Check property exists
    property = await db.get(Property, booking.property_id)
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )

    # Create booking
    db_booking = Booking(**booking.dict(), tenant_id=current_user.id)
    db.add(db_booking)
    await db.commit()
    await db.refresh(db_booking)
    return db_booking

@router.get("/{booking_id}", response_model=BookingOut)
async def get_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific booking details"""
    booking = await db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.tenant_id != current_user.id and booking.property.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return booking