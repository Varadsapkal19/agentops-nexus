"""Authentication Pydantic schemas."""

from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    totp_code: Optional[str] = None


class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user_id: str
    email: str
    full_name: str
    mfa_required: bool = False


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class TokenRefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class MFASetupResponse(BaseModel):
    secret: str
    uri: str
    qr_code_url: str


class MFAVerifyRequest(BaseModel):
    code: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
