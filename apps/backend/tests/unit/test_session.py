import pytest

from unittest.mock import patch, MagicMock
from app.db import session

import os


def setup_module(module):
    # Reset global state before each test module
    session._cluster = None
    session._session = None


def teardown_module(module):
    session._cluster = None
    session._session = None


def test_connect_to_astra_success(monkeypatch):
    """Should connect to AstraDB with valid config and log version."""
    session._cluster = None
    session._session = None
    # Patch os.path.exists to True
    monkeypatch.setattr(os.path, "exists", lambda path: True)
    # Patch Cluster and session
    mock_cluster = MagicMock()
    mock_session = MagicMock()
    mock_cluster.connect.return_value = mock_session
    mock_session.execute.return_value.one.return_value = MagicMock(
        release_version="4.0.0"
    )
    with patch("app.db.session.Cluster", return_value=mock_cluster) as mock_cls, patch(
        "app.db.session.PlainTextAuthProvider"
    ):
        session.connect_to_astra()
        mock_cls.assert_called_once()
        assert session._session is mock_session
        assert session._cluster is mock_cluster


def test_connect_to_astra_bundle_missing(monkeypatch):
    """Should raise FileNotFoundError if secure bundle is missing."""
    session._cluster = None
    session._session = None
    monkeypatch.setattr(os.path, "exists", lambda path: False)
    with pytest.raises(FileNotFoundError):
        session.connect_to_astra()


def test_connect_to_astra_connection_failure(monkeypatch):
    """Should raise RuntimeError if connection fails."""
    session._cluster = None
    session._session = None
    monkeypatch.setattr(os.path, "exists", lambda path: True)
    with patch("app.db.session.Cluster", side_effect=Exception("fail connect")), patch(
        "app.db.session.PlainTextAuthProvider"
    ):
        with pytest.raises(RuntimeError) as exc_info:
            session.connect_to_astra()
        assert "Could not connect to AstraDB" in str(exc_info.value)


def test_close_astra_connection(monkeypatch):
    """Should close connection cleanly."""
    mock_cluster = MagicMock()
    session._cluster = mock_cluster
    session._session = MagicMock()
    session.close_astra_connection()
    mock_cluster.shutdown.assert_called_once()
    assert session._cluster is None
    assert session._session is None
