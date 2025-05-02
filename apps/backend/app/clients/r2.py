import boto3
from botocore.client import Config
from fastapi import HTTPException, status
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Global variable for the client
_r2_client = None


def get_r2_client():
    """
    Returns a singleton boto3 client configured for Cloudflare R2.
    Raises HTTPException if configuration is missing or client creation fails.
    """
    global _r2_client
    if _r2_client is not None:
        return _r2_client
    # Explicit config validation
    required = [
        settings.R2_ACCESS_KEY_ID,
        settings.R2_SECRET_ACCESS_KEY,
        settings.R2_ACCOUNT_ID,
        settings.R2_BUCKET_NAME,
        settings.R2_ENDPOINT_URL,
    ]
    if not all(required):
        logger.error("Missing one or more required R2 configuration values.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Missing one or more required R2 configuration values.",
        )
    try:
        logger.info("Initializing Cloudflare R2 client...")
        _r2_client = boto3.client(
            "s3",
            endpoint_url=settings.R2_ENDPOINT_URL,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4"),
            region_name="auto",  # R2 uses 'auto' region
        )
        logger.info("Cloudflare R2 client initialized.")
        return _r2_client
    except Exception as e:
        logger.exception(f"Failed to initialize R2 client: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize R2 client: {e}",
        )


# Dependency for FastAPI


def r2_client_dependency():
    return get_r2_client()
