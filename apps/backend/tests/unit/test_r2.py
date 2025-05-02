import pytest
from fastapi import HTTPException
from unittest.mock import patch

# Import the function under test
from app.clients import r2


def test_r2_client_initializes_with_good_config(monkeypatch):
    r2._r2_client = None
    """Should initialize R2 client with correct config."""
    # Patch config to provide required values
    monkeypatch.setenv("R2_ACCESS_KEY_ID", "fake-access-key")
    monkeypatch.setenv("R2_SECRET_ACCESS_KEY", "fake-secret-key")
    monkeypatch.setenv("R2_ACCOUNT_ID", "fake-account")
    monkeypatch.setenv("R2_BUCKET_NAME", "fake-bucket")
    monkeypatch.setenv("R2_ENDPOINT_URL", "https://fake-endpoint")

    # Patch boto3 client to avoid real AWS call
    with patch("app.clients.r2.boto3.client") as mock_boto_client:
        mock_boto_client.return_value = "mock-client"
        client = r2.get_r2_client()
        assert client == "mock-client"
        mock_boto_client.assert_called_once()


def test_r2_client_raises_on_bad_config(monkeypatch):
    r2._r2_client = None
    """Should raise HTTPException on bad/missing config."""
    from app.core.config import settings

    # Patch settings attributes to None to simulate missing config
    monkeypatch.setattr(settings, "R2_ACCESS_KEY_ID", None)
    monkeypatch.setattr(settings, "R2_SECRET_ACCESS_KEY", None)
    monkeypatch.setattr(settings, "R2_ACCOUNT_ID", None)
    monkeypatch.setattr(settings, "R2_BUCKET_NAME", None)
    monkeypatch.setattr(settings, "R2_ENDPOINT_URL", None)

    with pytest.raises(HTTPException) as exc_info:
        r2.get_r2_client()
    assert exc_info.value.status_code == 500
    # Accept either 'missing' or 'None' in error message for robustness
    assert ("missing" in str(exc_info.value.detail).lower()) or (
        "none" in str(exc_info.value.detail).lower()
    )


def test_r2_client_singleton(monkeypatch):
    r2._r2_client = None
    """Should return the same client instance (singleton pattern)."""
    monkeypatch.setenv("R2_ACCESS_KEY_ID", "fake-access-key")
    monkeypatch.setenv("R2_SECRET_ACCESS_KEY", "fake-secret-key")
    monkeypatch.setenv("R2_ACCOUNT_ID", "fake-account")
    monkeypatch.setenv("R2_BUCKET_NAME", "fake-bucket")
    monkeypatch.setenv("R2_ENDPOINT_URL", "https://fake-endpoint")

    with patch("app.clients.r2.boto3.client") as mock_boto_client:
        mock_boto_client.return_value = "mock-client"
        client1 = r2.get_r2_client()
        client2 = r2.get_r2_client()
        assert client1 is client2
        mock_boto_client.assert_called_once()
