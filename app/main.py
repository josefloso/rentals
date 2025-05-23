from fastapi import FastAPI
from app.core.database import engine, Base
from app.routes import auth, users, properties, bookings
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI(
    title="Rental Management API",
    description="API for property rentals and bookings",
    version="0.1.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(properties.router)
app.include_router(bookings.router)

@app.on_event("startup")
async def startup():
    # Test connection first
    async with engine.connect() as conn:
        await conn.execute("SELECT 1")
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()