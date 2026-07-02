"""Security utilities: JWT, password hashing, OAuth."""

import secrets
import string
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union

import pyotp
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None,
    extra_claims: Optional[Dict] = None,
) -> str:
    """Create a JWT access token."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access",
        "iat": datetime.now(timezone.utc),
        "jti": secrets.token_hex(16),
    }
    
    if extra_claims:
        to_encode.update(extra_claims)
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(subject: Union[str, Any]) -> str:
    """Create a JWT refresh token."""
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh",
        "iat": datetime.now(timezone.utc),
        "jti": secrets.token_hex(16),
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str, token_type: str = "access") -> Optional[Dict]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != token_type:
            return None
        return payload
    except JWTError:
        return None


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def generate_api_key() -> str:
    """Generate a secure API key."""
    prefix = "ank_"
    key = secrets.token_urlsafe(32)
    return f"{prefix}{key}"


def generate_totp_secret() -> str:
    """Generate a TOTP secret for MFA."""
    return pyotp.random_base32(length=settings.TOTP_SECRET_LENGTH)


def verify_totp(secret: str, code: str) -> bool:
    """Verify a TOTP code."""
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)


def get_totp_uri(secret: str, email: str) -> str:
    """Get the TOTP URI for QR code generation."""
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name=settings.MFA_ISSUER)


def generate_random_password(length: int = 16) -> str:
    """Generate a random secure password."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))
