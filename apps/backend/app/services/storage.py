from typing import Any
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import UploadFile, HTTPException, status
import logging
import uuid  # To generate unique filenames
import os  # To get file extension

from app.core.config import settings

logger = logging.getLogger(__name__)


def upload_file_to_r2(
    r2_client: Any,  # Boto3 client, type as Any for mypy compatibility
    file: UploadFile,
    allowed_content_types: list[str] | None = None,  # Optional validation
) -> str:
    """
    Uploads a file to the configured R2 bucket and returns its public URL.

    Args:
        r2_client: Initialized Boto3 S3 client.
        file: FastAPI UploadFile object.
        allowed_content_types: Optional list of allowed MIME types.

    Returns:
        The public URL of the uploaded file.

    Raises:
        HTTPException: If upload fails or file type is not allowed.
    """
    logger.info(f"Uploading file: {file.filename}")
    if allowed_content_types and file.content_type not in allowed_content_types:
        logger.warning(f"File type {file.content_type} not allowed.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not allowed.",
        )
    try:
        filename = file.filename if file.filename is not None else ""
        ext = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4()}{ext}"
        file_content = file.file.read()
        r2_client.put_object(
            Bucket=settings.R2_BUCKET_NAME,
            Key=unique_filename,
            Body=file_content,
            ContentType=file.content_type,
        )
        public_url = f"{settings.R2_PUBLIC_URL_BASE}/{unique_filename}"
        logger.info(f"File uploaded successfully: {public_url}")
        return public_url
    except (BotoCoreError, ClientError) as e:
        logger.exception(f"Failed to upload file to R2: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to upload file to object storage.",
        )
    except Exception as e:
        logger.exception(f"Unexpected error during file upload: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error during file upload.",
        )
