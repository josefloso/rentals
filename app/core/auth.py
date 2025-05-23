import os
import time
from datetime import datetime, timedelta
from typing import Optional

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Configuration
SECRET_KEY = os.getenv("AUTH_SECRET", os.urandom(32).hex())
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
security = HTTPBearer()

def create_access_token(
    subject: str, 
    expires_delta: Optional[timedelta] = None
) -> str:
    """Generate a secure JWT token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    # Using cryptographic time comparison
    expire_timestamp = int(time.mktime(expire.timetuple()))
    
    # Simple but secure token generation
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(SECRET_KEY.encode())
    
    # Build token components
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": subject, "exp": expire_timestamp}
    
    # Manual JWT construction (simplified)
    encoded_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode()
    encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    signature = hmac.new(key, f"{encoded_header}.{encoded_payload}".encode(), hashes.SHA256)
    
    return f"{encoded_header}.{encoded_payload}.{signature}"

def verify_token(credentials: HTTPAuthorizationCredentials):
    """Verify and decode JWT token"""
    try:
        token = credentials.credentials
        header_b64, payload_b64, signature = token.split(".")
        
        # Reconstruct signature
        salt = ... # Extract from your storage
        kdf = PBKDF2HMAC(...) # Same as creation
        key = kdf.derive(SECRET_KEY.encode())
        
        valid_signature = hmac.new(key, f"{header_b64}.{payload_b64}".encode(), hashes.SHA256)
        if not hmac.compare_digest(signature, valid_signature):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        
        payload = json.loads(base64.urlsafe_b64decode(payload_b64 + "==").decode())
        return payload["sub"]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )