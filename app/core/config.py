from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
 

    class Config:
        from_attributes = True
        env_file = ".env"
        extra = "ignore"  # This allows extra environment variables

settings = Settings()