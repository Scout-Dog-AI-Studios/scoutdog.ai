from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request
from typing import Dict
from app.auth.jwt import validate_token


class HTTPBearer401(HTTPBearer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, auto_error=False, **kwargs)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials = await super().__call__(request)
        if credentials is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return credentials


# Initialize the bearer scheme
auth_scheme = HTTPBearer401()


async def get_current_user_token_payload(
    token: HTTPAuthorizationCredentials = Depends(
        auth_scheme
    ),  # Use Depends with HTTPBearer instance
) -> Dict:
    """
    Dependency that validates the Bearer token and returns the payload.
    Raises HTTPException if validation fails.
    """
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Validate the token using the function from jwt.py
    payload = await validate_token(token.credentials)
    # You could add checks here e.g., check if user exists in DB based on payload['sub']
    return payload  # Return the validated payload
