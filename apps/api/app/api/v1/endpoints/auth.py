"""Authentication endpoints."""

import secrets
from datetime import datetime, timezone, timedelta
from typing import Optional

import httpx
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    get_totp_uri,
    generate_totp_secret,
    verify_password,
    verify_token,
    verify_totp,
)
from app.models.user import AuthProvider, User, UserStatus
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    TokenRefreshRequest,
    TokenRefreshResponse,
    MFASetupResponse,
    MFAVerifyRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    PasswordChangeRequest,
)
from app.services.user_service import UserService
from app.utils.email import send_verification_email, send_password_reset_email

router = APIRouter()


@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user."""
    user_service = UserService(db)
    
    # Check if email exists
    existing = await user_service.get_by_email(request.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create user
    user = await user_service.create(
        email=request.email,
        full_name=request.full_name,
        password=request.password,
    )
    
    # Send verification email in background
    verification_token = secrets.token_urlsafe(32)
    user.email_verification_token = verification_token
    await db.commit()
    background_tasks.add_task(send_verification_email, user.email, verification_token)
    
    # Generate tokens
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user_id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        mfa_required=False,
    )


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """Login with email and password."""
    user_service = UserService(db)
    
    user = await user_service.get_by_email(request.email)
    if not user or not verify_password(request.password, user.hashed_password or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    if user.status == UserStatus.SUSPENDED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account suspended",
        )
    
    # Check if MFA is required
    if user.mfa_enabled:
        if not request.totp_code:
            return LoginResponse(
                access_token="",
                refresh_token="",
                token_type="bearer",
                user_id=str(user.id),
                email=user.email,
                full_name=user.full_name,
                mfa_required=True,
            )
        
        if not verify_totp(user.mfa_secret, request.totp_code):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid MFA code",
            )
    
    # Update last login
    user.last_login_at = datetime.now(timezone.utc)
    user.status = UserStatus.ACTIVE
    await db.commit()
    
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user_id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        mfa_required=False,
    )


@router.post("/refresh", response_model=TokenRefreshResponse)
async def refresh_token(
    request: TokenRefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token."""
    import uuid
    
    payload = verify_token(request.refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    
    if not user or user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    access_token = create_access_token(subject=str(user.id))
    new_refresh_token = create_refresh_token(subject=str(user.id))
    
    return TokenRefreshResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )


@router.post("/mfa/setup", response_model=MFASetupResponse)
async def setup_mfa(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Set up MFA for the current user."""
    if current_user.mfa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA already enabled",
        )
    
    secret = generate_totp_secret()
    current_user.mfa_secret = secret
    await db.commit()
    
    uri = get_totp_uri(secret, current_user.email)
    
    return MFASetupResponse(
        secret=secret,
        uri=uri,
        qr_code_url=f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={uri}",
    )


@router.post("/mfa/verify")
async def verify_mfa(
    request: MFAVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Verify and enable MFA."""
    if not current_user.mfa_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA setup not initiated",
        )
    
    if not verify_totp(current_user.mfa_secret, request.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid TOTP code",
        )
    
    current_user.mfa_enabled = True
    await db.commit()
    
    return {"message": "MFA enabled successfully"}


@router.post("/mfa/disable")
async def disable_mfa(
    request: MFAVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Disable MFA."""
    if not current_user.mfa_enabled:
        raise HTTPException(status_code=400, detail="MFA not enabled")
    
    if not verify_totp(current_user.mfa_secret, request.code):
        raise HTTPException(status_code=400, detail="Invalid TOTP code")
    
    current_user.mfa_enabled = False
    current_user.mfa_secret = None
    await db.commit()
    
    return {"message": "MFA disabled successfully"}


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Request password reset."""
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()
    
    if user:
        token = secrets.token_urlsafe(32)
        user.password_reset_token = token
        user.password_reset_expires = datetime.now(timezone.utc) + timedelta(hours=1)
        await db.commit()
        background_tasks.add_task(send_password_reset_email, user.email, token)
    
    # Always return success to prevent email enumeration
    return {"message": "If the email exists, a reset link has been sent"}


@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """Reset password with token."""
    result = await db.execute(
        select(User).where(
            User.password_reset_token == request.token,
            User.password_reset_expires > datetime.now(timezone.utc),
        )
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    user.hashed_password = get_password_hash(request.new_password)
    user.password_reset_token = None
    user.password_reset_expires = None
    await db.commit()
    
    return {"message": "Password reset successfully"}


@router.get("/google")
async def google_auth():
    """Initiate Google OAuth flow."""
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/auth"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.NEXT_PUBLIC_API_URL}/api/v1/auth/google/callback"
        f"&response_type=code"
        f"&scope=openid email profile"
    )
    return RedirectResponse(url=google_auth_url)


@router.get("/google/callback")
async def google_callback(
    code: str,
    db: AsyncSession = Depends(get_db),
):
    """Handle Google OAuth callback."""
    async with httpx.AsyncClient() as client:
        # Exchange code for token
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": f"{settings.NEXT_PUBLIC_API_URL}/api/v1/auth/google/callback",
                "grant_type": "authorization_code",
            },
        )
        token_data = token_response.json()
        
        # Get user info
        user_info_response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
        user_info = user_info_response.json()
    
    user_service = UserService(db)
    
    # Find or create user
    user = await user_service.get_by_email(user_info["email"])
    if not user:
        user = await user_service.create(
            email=user_info["email"],
            full_name=user_info.get("name", ""),
            oauth_id=user_info["id"],
            auth_provider=AuthProvider.GOOGLE,
            avatar_url=user_info.get("picture"),
        )
        user.is_email_verified = True
        user.status = UserStatus.ACTIVE
        await db.commit()
    
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    
    # Redirect to frontend with tokens
    frontend_url = settings.NEXT_PUBLIC_APP_URL
    return RedirectResponse(
        url=f"{frontend_url}/auth/callback?access_token={access_token}&refresh_token={refresh_token}"
    )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout endpoint (client-side token invalidation)."""
    return {"message": "Logged out successfully"}


@router.get("/verify-email")
async def verify_email(
    token: str,
    db: AsyncSession = Depends(get_db),
):
    """Verify email address."""
    result = await db.execute(
        select(User).where(User.email_verification_token == token)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    
    user.is_email_verified = True
    user.email_verification_token = None
    user.status = UserStatus.ACTIVE
    await db.commit()
    
    return {"message": "Email verified successfully"}
