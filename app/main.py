from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base

app = FastAPI()

# CORS Setup (keep your existing if you have it)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database lifecycle events
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

# Import routers AFTER app creation to avoid circular imports
from app.api.routes import router  # Keep your existing import path
app.include_router(router, prefix="/api")  # Add prefix if needed

# Keep any other existing app configurations