# Centralize schema imports
from .user import UserCreate, UserOut, UserUpdate
from .property import PropertyCreate, PropertyOut
from .booking import BookingCreate, BookingOut

__all__ = [
    "UserCreate", "UserOut", "UserUpdate",
    "PropertyCreate", "PropertyOut",
    "BookingCreate", "BookingOut"
]