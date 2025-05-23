from fastapi import FastAPI
from app.core.database import engine, Base
from app.routes import auth, bookings, properties, users

app = FastAPI()

# Include all your routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(properties.router)
app.include_router(bookings.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()