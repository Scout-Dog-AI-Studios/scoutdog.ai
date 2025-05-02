from fastapi import APIRouter, Depends
from typing import Dict  # For type hinting the payload

# Import the dependency that validates the token
from app.api.v1.dependencies import get_current_user_token_payload

router = APIRouter()


@router.get("/secure-ping", response_model=Dict)  # Specify response model if desired
async def secure_ping(
    # Use Depends to inject the validated payload
    payload: Dict = Depends(get_current_user_token_payload),
):
    """
    A test endpoint that requires a valid JWT token.
    Returns a success message along with the token payload.
    """
    # The code here only runs if get_current_user_token_payload succeeds
    return {"message": "Secure Pong!", "user_payload": payload}
