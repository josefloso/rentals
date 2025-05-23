# Aggregate all routers
from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .properties import router as properties_router
from .bookings import router as bookings_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(properties_router)
router.include_router(bookings_router)

__all__ = ["router"]