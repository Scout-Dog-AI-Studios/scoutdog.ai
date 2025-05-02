import httpx  # Use httpx for async requests
from fastapi import HTTPException, status
from jose import jwt
from jose.exceptions import JOSEError, ExpiredSignatureError, JWTClaimsError
import logging  # Import logging

from app.core.config import settings

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache for JWKS
_jwks = None


async def get_jwks():
    """Fetches and caches JWKS from Auth0."""
    global _jwks
    # Basic caching - consider more robust caching later if needed
    if _jwks:
        return _jwks
    try:
        jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
        async with httpx.AsyncClient() as client:
            response = await client.get(jwks_url)
            response.raise_for_status()  # Raise HTTP errors
            _jwks = response.json()
            logger.info("Successfully fetched JWKS.")
            return _jwks
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching JWKS: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch JWKS from authentication provider.",
        )
    except Exception as e:
        logger.error(f"Error fetching JWKS: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch JWKS.",
        )


async def validate_token(token: str):
    """Validates the Auth0 JWT token."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token required",
        )

    try:
        jwks = await get_jwks()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                break  # Found the key

        if not rsa_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to find appropriate key",
            )

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=settings.AUTH0_API_AUDIENCE,
            issuer=f"https://{settings.AUTH0_DOMAIN}/",
        )
        return payload

    except ExpiredSignatureError:
        logger.warning("Token validation failed: Expired signature.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is expired"
        )
    except JWTClaimsError as e:
        logger.warning(f"Token validation failed: Invalid claims - {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid claims: {e}"
        )
    except JOSEError as e:
        logger.warning(f"Token validation failed: JOSE error - {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unable to parse authentication token: {e}",
        )
    except HTTPException:
        raise  # Propagate FastAPI HTTPExceptions as-is
    except Exception as e:
        logger.error(f"An unexpected error occurred during token validation: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to parse authentication token: {e}",
        )
