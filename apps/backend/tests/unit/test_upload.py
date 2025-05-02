import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock
from app.main import app


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.upload.upload_file_to_r2")
def test_upload_valid_file(mock_upload_file_to_r2, tmp_path):
    from app.api.v1.endpoints import upload as upload_module

    app.dependency_overrides[upload_module.get_current_user_token_payload] = lambda: {
        "sub": "test-user"
    }
    app.dependency_overrides[upload_module.r2_client_dependency] = lambda: MagicMock()
    mock_upload_file_to_r2.return_value = "https://cdn.example.com/file.png"

    # Prepare a fake image file
    file_content = b"fake image data"
    file_name = "test.png"
    files = {"file": (file_name, file_content, "image/png")}

    transport = ASGITransport(app=app)

    async def run():
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/v1/upload", files=files)
        assert response.status_code == 200
        assert response.json() == {"file_url": "https://cdn.example.com/file.png"}
        app.dependency_overrides = {}

    import asyncio

    asyncio.run(run())


@patch("app.api.v1.endpoints.upload.upload_file_to_r2")
def test_upload_storage_error(mock_upload_file_to_r2):
    from app.api.v1.endpoints import upload as upload_module

    app.dependency_overrides[upload_module.get_current_user_token_payload] = lambda: {
        "sub": "test-user"
    }
    app.dependency_overrides[upload_module.r2_client_dependency] = lambda: MagicMock()
    mock_upload_file_to_r2.side_effect = ValueError("storage unavailable")

    file_content = b"fake image data"
    file_name = "test.png"
    files = {"file": (file_name, file_content, "image/png")}

    transport = ASGITransport(app=app)

    async def run():
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/v1/upload", files=files)
        assert response.status_code == 500
        assert "storage unavailable" in response.json()["detail"]
        app.dependency_overrides = {}

    import asyncio

    asyncio.run(run())


@patch("app.api.v1.endpoints.upload.upload_file_to_r2")
def test_upload_requires_jwt(mock_upload_file_to_r2):
    from app.api.v1.endpoints import upload as upload_module

    # Do NOT override get_current_user_token_payload (real dependency runs)
    app.dependency_overrides[upload_module.r2_client_dependency] = lambda: MagicMock()
    mock_upload_file_to_r2.side_effect = AssertionError(
        "Should not be called without JWT"
    )

    file_content = b"fake image data"
    file_name = "test.png"
    files = {"file": (file_name, file_content, "image/png")}

    transport = ASGITransport(app=app)

    async def run():
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/v1/upload", files=files)  # No auth header
        assert response.status_code == 401
        app.dependency_overrides = {}

    import asyncio

    asyncio.run(run())


@patch("app.api.v1.endpoints.upload.upload_file_to_r2")
def test_upload_file_too_large(mock_upload_file_to_r2):
    from app.api.v1.endpoints import upload as upload_module

    app.dependency_overrides[upload_module.get_current_user_token_payload] = lambda: {
        "sub": "test-user"
    }
    app.dependency_overrides[upload_module.r2_client_dependency] = lambda: MagicMock()
    mock_upload_file_to_r2.side_effect = AssertionError(
        "Should not be called if file is too large"
    )

    # Create a file just over 5MB
    file_content = b"0" * (5 * 1024 * 1024 + 1)
    file_name = "big.png"
    files = {"file": (file_name, file_content, "image/png")}

    transport = ASGITransport(app=app)

    async def run():
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/v1/upload", files=files)
        assert response.status_code == 413
        assert "File size exceeds limit" in response.json()["detail"]
        app.dependency_overrides = {}

    import asyncio

    asyncio.run(run())


@patch("app.api.v1.endpoints.upload.upload_file_to_r2")
def test_upload_missing_file(mock_upload_file_to_r2):
    from app.api.v1.endpoints import upload as upload_module

    app.dependency_overrides[upload_module.get_current_user_token_payload] = lambda: {
        "sub": "test-user"
    }
    app.dependency_overrides[upload_module.r2_client_dependency] = lambda: MagicMock()
    mock_upload_file_to_r2.side_effect = AssertionError(
        "Should not be called if no file is provided"
    )

    transport = ASGITransport(app=app)

    async def run():
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/v1/upload", files={})  # No file
        assert response.status_code == 422
        app.dependency_overrides = {}

    import asyncio

    asyncio.run(run())


@patch("app.api.v1.endpoints.upload.upload_file_to_r2")
def test_upload_disallowed_content_type(mock_upload_file_to_r2):
    from app.api.v1.endpoints import upload as upload_module

    app.dependency_overrides[upload_module.get_current_user_token_payload] = lambda: {
        "sub": "test-user"
    }
    app.dependency_overrides[upload_module.r2_client_dependency] = lambda: MagicMock()
    # upload_file_to_r2 should not be called for disallowed types
    mock_upload_file_to_r2.side_effect = AssertionError(
        "Should not be called for disallowed content type"
    )

    file_content = b"not an image"
    file_name = "test.txt"
    files = {"file": (file_name, file_content, "text/plain")}

    transport = ASGITransport(app=app)

    async def run():
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/v1/upload", files=files)
        assert response.status_code == 422  # Unprocessable Entity
        app.dependency_overrides = {}

    import asyncio

    asyncio.run(run())
