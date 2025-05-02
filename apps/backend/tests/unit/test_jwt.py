import pytest

from fastapi import HTTPException
from jose import jwt as jose_jwt
import asyncio

# Import the function under test
from app.auth.jwt import validate_token


@pytest.mark.asyncio
def test_validate_token_success(monkeypatch):
    """Should validate a correct JWT and return payload."""
    fake_payload = {"sub": "user123", "aud": "test-aud"}
    fake_token = "good.jwt.token"

    async def fake_get_jwks():
        return {
            "keys": [{"kid": "abc", "kty": "RSA", "use": "sig", "n": "n", "e": "e"}]
        }

    def fake_get_unverified_header(token):
        return {"kid": "abc"}

    def fake_decode(token, rsa_key, algorithms, audience, issuer):
        assert token == fake_token
        return fake_payload

    monkeypatch.setattr("app.auth.jwt.get_jwks", fake_get_jwks)
    monkeypatch.setattr(jose_jwt, "get_unverified_header", fake_get_unverified_header)
    monkeypatch.setattr(jose_jwt, "decode", fake_decode)

    result = asyncio.run(validate_token(fake_token))
    assert result == fake_payload


@pytest.mark.asyncio
def test_validate_token_expired(monkeypatch):
    """Should reject expired JWT (ExpiredSignatureError)."""
    from jose.exceptions import ExpiredSignatureError

    fake_token = "expired.jwt.token"

    async def fake_get_jwks():
        return {
            "keys": [{"kid": "abc", "kty": "RSA", "use": "sig", "n": "n", "e": "e"}]
        }

    def fake_get_unverified_header(token):
        return {"kid": "abc"}

    def fake_decode(*args, **kwargs):
        raise ExpiredSignatureError()

    monkeypatch.setattr("app.auth.jwt.get_jwks", fake_get_jwks)
    monkeypatch.setattr(jose_jwt, "get_unverified_header", fake_get_unverified_header)
    monkeypatch.setattr(jose_jwt, "decode", fake_decode)

    with pytest.raises(HTTPException) as exc_info:
        import asyncio

        asyncio.run(validate_token(fake_token))
    assert exc_info.value.status_code == 401
    assert "expired" in str(exc_info.value.detail).lower()


@pytest.mark.asyncio
def test_validate_token_invalid_claims(monkeypatch):
    """Should reject JWT with invalid claims (JWTClaimsError)."""
    from jose.exceptions import JWTClaimsError

    fake_token = "badclaims.jwt.token"

    async def fake_get_jwks():
        return {
            "keys": [{"kid": "abc", "kty": "RSA", "use": "sig", "n": "n", "e": "e"}]
        }

    def fake_get_unverified_header(token):
        return {"kid": "abc"}

    def fake_decode(*args, **kwargs):
        raise JWTClaimsError("audience mismatch")

    monkeypatch.setattr("app.auth.jwt.get_jwks", fake_get_jwks)
    monkeypatch.setattr(jose_jwt, "get_unverified_header", fake_get_unverified_header)
    monkeypatch.setattr(jose_jwt, "decode", fake_decode)

    with pytest.raises(HTTPException) as exc_info:
        import asyncio

        asyncio.run(validate_token(fake_token))
    assert exc_info.value.status_code == 401
    assert "claims" in str(exc_info.value.detail).lower()


@pytest.mark.asyncio
def test_validate_token_bad_signature(monkeypatch):
    """Should reject JWT with bad signature or malformed token (JOSEError)."""
    from jose.exceptions import JOSEError

    fake_token = "bad.jwt.token"

    async def fake_get_jwks():
        return {
            "keys": [{"kid": "abc", "kty": "RSA", "use": "sig", "n": "n", "e": "e"}]
        }

    def fake_get_unverified_header(token):
        return {"kid": "abc"}

    def fake_decode(*args, **kwargs):
        raise JOSEError("Signature verification failed")

    monkeypatch.setattr("app.auth.jwt.get_jwks", fake_get_jwks)
    monkeypatch.setattr(jose_jwt, "get_unverified_header", fake_get_unverified_header)
    monkeypatch.setattr(jose_jwt, "decode", fake_decode)

    with pytest.raises(HTTPException) as exc_info:
        import asyncio

        asyncio.run(validate_token(fake_token))
    assert exc_info.value.status_code == 401
    assert "unable to parse authentication token" in str(exc_info.value.detail).lower()


@pytest.mark.asyncio
def test_validate_token_jwks_fetch_failure(monkeypatch):
    """Should handle JWKS fetch failure gracefully."""
    fake_token = "any.jwt.token"

    async def fake_get_jwks():
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch JWKS from authentication provider.",
        )

    monkeypatch.setattr("app.auth.jwt.get_jwks", fake_get_jwks)

    with pytest.raises(HTTPException) as exc_info:
        import asyncio

        asyncio.run(validate_token(fake_token))
    assert exc_info.value.status_code == 500
    assert "jwks" in str(exc_info.value.detail).lower()

    """Should reject JWT with bad signature or malformed token (JOSEError)."""
    from jose.exceptions import JOSEError

    fake_token = "bad.jwt.token"

    async def fake_get_jwks():
        return {
            "keys": [{"kid": "abc", "kty": "RSA", "use": "sig", "n": "n", "e": "e"}]
        }

    def fake_get_unverified_header(token):
        return {"kid": "abc"}

    def fake_decode(*args, **kwargs):
        raise JOSEError("Signature verification failed")

    monkeypatch.setattr("app.auth.jwt.get_jwks", fake_get_jwks)
    monkeypatch.setattr(jose_jwt, "get_unverified_header", fake_get_unverified_header)
    monkeypatch.setattr(jose_jwt, "decode", fake_decode)

    with pytest.raises(HTTPException) as exc_info:
        import asyncio

        asyncio.run(validate_token(fake_token))
    assert exc_info.value.status_code == 401
    assert "unable to parse authentication token" in str(exc_info.value.detail).lower()

    """Should reject JWT with invalid claims (JWTClaimsError)."""
    from jose.exceptions import JWTClaimsError

    fake_token = "badclaims.jwt.token"

    async def fake_get_jwks():
        return {
            "keys": [{"kid": "abc", "kty": "RSA", "use": "sig", "n": "n", "e": "e"}]
        }

    def fake_get_unverified_header(token):
        return {"kid": "abc"}

    def fake_decode(*args, **kwargs):
        raise JWTClaimsError("audience mismatch")

    monkeypatch.setattr("app.auth.jwt.get_jwks", fake_get_jwks)
    monkeypatch.setattr(jose_jwt, "get_unverified_header", fake_get_unverified_header)
    monkeypatch.setattr(jose_jwt, "decode", fake_decode)

    with pytest.raises(HTTPException) as exc_info:
        import asyncio

        asyncio.run(validate_token(fake_token))
    assert exc_info.value.status_code == 401
    assert "claims" in str(exc_info.value.detail).lower()

    """Should reject expired JWT (ExpiredSignatureError)."""
    from jose.exceptions import ExpiredSignatureError

    fake_token = "expired.jwt.token"

    async def fake_get_jwks():
        return {
            "keys": [{"kid": "abc", "kty": "RSA", "use": "sig", "n": "n", "e": "e"}]
        }

    def fake_get_unverified_header(token):
        return {"kid": "abc"}

    def fake_decode(*args, **kwargs):
        raise ExpiredSignatureError()

    monkeypatch.setattr("app.auth.jwt.get_jwks", fake_get_jwks)
    monkeypatch.setattr(jose_jwt, "get_unverified_header", fake_get_unverified_header)
    monkeypatch.setattr(jose_jwt, "decode", fake_decode)

    with pytest.raises(HTTPException) as exc_info:
        import asyncio

        asyncio.run(validate_token(fake_token))
    assert exc_info.value.status_code == 401
    assert "expired" in str(exc_info.value.detail).lower()
