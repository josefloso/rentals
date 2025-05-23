from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional

class BookingBase(BaseModel):
    start_date: date
    end_date: date
    property_id: int

    @validator('end_date')
    def validate_dates(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError("End date must be after start date")
        return v

class BookingCreate(BookingBase):
    pass

class BookingOut(BookingBase):
    id: int
    status: str
    tenant_id: int

    class Config:
        from_attributes = True