from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class PropertyBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    location: str = Field(..., max_length=100)
    bedrooms: int = Field(..., gt=0)

class PropertyCreate(PropertyBase):
    pass

class PropertyOut(PropertyBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True  