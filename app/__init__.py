# Makes the app directory a Python package
from .main import app  # Import the FastAPI instance for easy access

__all__ = ["app"]