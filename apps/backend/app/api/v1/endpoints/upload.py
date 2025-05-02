from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from pydantic import BaseModel, HttpUrl
import logging

from app.api.v1.dependencies import get_current_user_token_payload
from app.clients.r2 import r2_client_dependency
from app.services.storage import upload_file_to_r2

router = APIRouter()
logger = logging.getLogger(__name__)


class UploadResponse(BaseModel):
    file_url: HttpUrl


@router.post("/upload", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    payload=Depends(get_current_user_token_payload),
    r2_client=Depends(r2_client_dependency),
):
    """
    Secured endpoint to upload a file to Cloudflare R2. Only allows certain image types.
    Returns the public URL of the uploaded file.
    """
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    if file.content_type not in allowed_types:
        logger.warning(f"Disallowed content type: {file.content_type}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Content type '{file.content_type}' is not allowed.",
        )
    # Check file size (read into memory, then seek back to 0)
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        logger.warning(f"File too large: {len(contents)} bytes")
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds limit of {MAX_FILE_SIZE // (1024*1024)}MB.",
        )
    await file.seek(0)  # Reset pointer for downstream use
    try:
        public_url = upload_file_to_r2(
            r2_client=r2_client, file=file, allowed_content_types=allowed_types
        )
        logger.info(f"File uploaded successfully. URL: {public_url}")
        return UploadResponse(file_url=public_url)  # type: ignore
    except ValueError as ve:
        logger.error(f"Configuration error during upload: {ve}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ve)
        )
    # HTTPException raised by the service will be passed through
