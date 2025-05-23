from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str  # Only need connection string for NeonDB
    
    # Remove these if they exist:
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str  
    # POSTGRES_DB: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"  # Important for security

# Keep this instantiation
settings = Settings()