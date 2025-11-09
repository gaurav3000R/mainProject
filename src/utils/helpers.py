"""Utility helper functions."""
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.core.config import settings


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def generate_token(length: int = 32) -> str:
    """Generate a random token."""
    return secrets.token_urlsafe(length)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode JWT access token."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None


def generate_request_id() -> str:
    """Generate unique request ID."""
    return hashlib.sha256(
        f"{datetime.utcnow().isoformat()}{secrets.token_hex(16)}".encode()
    ).hexdigest()[:16]


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format datetime to ISO string."""
    if dt is None:
        dt = datetime.utcnow()
    return dt.isoformat()


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Sanitize user input."""
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length]
    
    return text
