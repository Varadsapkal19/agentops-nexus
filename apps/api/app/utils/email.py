"""Email utility functions."""

import structlog
from app.core.config import settings

logger = structlog.get_logger()


async def send_verification_email(email: str, token: str) -> None:
    """Send email verification email."""
    verify_url = f"{settings.NEXT_PUBLIC_APP_URL}/auth/verify-email?token={token}"
    logger.info("Sending verification email", email=email, url=verify_url)
    # In production, integrate with your email provider (SendGrid, SES, etc.)
    # For now, log the URL
    print(f"[DEV] Verify email: {verify_url}")


async def send_password_reset_email(email: str, token: str) -> None:
    """Send password reset email."""
    reset_url = f"{settings.NEXT_PUBLIC_APP_URL}/auth/reset-password?token={token}"
    logger.info("Sending password reset email", email=email)
    print(f"[DEV] Reset password: {reset_url}")


async def send_alert_email(email: str, alert_title: str, alert_message: str) -> None:
    """Send alert notification email."""
    logger.info("Sending alert email", email=email, alert=alert_title)
    print(f"[DEV] Alert email to {email}: {alert_title}")
