import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock
from app.main import app


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.greet.get_greeting_message")
async def test_greet_success(mock_get_greeting_message):
    # Arrange: mock dependencies
    from app.api.v1.endpoints import greet as greet_module

    app.dependency_overrides[greet_module.get_current_user_token_payload] = lambda: {
        "sub": "test-user"
    }
    app.dependency_overrides[greet_module.get_db_session] = lambda: MagicMock()
    mock_get_greeting_message.return_value = "Hello from DB!"

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/greet")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from DB!"}
    app.dependency_overrides = {}  # Clean up overrides


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.greet.get_greeting_message")
async def test_greet_fallback_message(mock_get_greeting_message):
    """Should return fallback message when DB returns no rows."""
    from app.api.v1.endpoints import greet as greet_module

    app.dependency_overrides[greet_module.get_current_user_token_payload] = lambda: {
        "sub": "test-user"
    }
    app.dependency_overrides[greet_module.get_db_session] = lambda: MagicMock()
    mock_get_greeting_message.return_value = None  # Simulate no rows

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/greet")
    assert response.status_code == 200
    # Adjust fallback message as per your implementation
    assert response.json()["message"].lower() in [
        "no greeting found",
        "no greeting available",
    ]
    app.dependency_overrides = {}


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.greet.get_greeting_message")
async def test_greet_db_exception(mock_get_greeting_message):
    """Should handle DB exceptions and return appropriate error/log."""
    from app.api.v1.endpoints import greet as greet_module

    app.dependency_overrides[greet_module.get_current_user_token_payload] = lambda: {
        "sub": "test-user"
    }
    app.dependency_overrides[greet_module.get_db_session] = lambda: MagicMock()
    mock_get_greeting_message.side_effect = Exception("DB error")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/v1/greet")
    assert response.status_code == 500
    assert "db error" in response.json()["detail"].lower()
    app.dependency_overrides = {}
