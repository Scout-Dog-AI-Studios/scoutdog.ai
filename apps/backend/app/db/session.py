from cassandra.cluster import Cluster, Session
from cassandra.auth import PlainTextAuthProvider
import logging
import os  # Import os to check file path

from app.core.config import settings

logger = logging.getLogger(__name__)

# Global variable to hold the cluster and session
# In more complex apps, consider dependency injection frameworks or context managers
_cluster: Cluster | None = None
_session: Session | None = None


def connect_to_astra():
    """Initializes the connection to AstraDB and sets global session/cluster."""
    global _cluster, _session

    if not os.path.exists(settings.ASTRA_DB_SECURE_BUNDLE_PATH):
        logger.error(
            f"Astra Secure Connect Bundle not found at path: {settings.ASTRA_DB_SECURE_BUNDLE_PATH}"
        )
        raise FileNotFoundError(
            f"Astra Secure Connect Bundle not found at {settings.ASTRA_DB_SECURE_BUNDLE_PATH}"
        )

    cloud_config = {"secure_connect_bundle": settings.ASTRA_DB_SECURE_BUNDLE_PATH}
    auth_provider = PlainTextAuthProvider(
        settings.ASTRA_DB_CLIENT_ID, settings.ASTRA_DB_CLIENT_SECRET
    )

    try:
        logger.info("Attempting to connect to AstraDB...")
        _cluster = Cluster(
            cloud=cloud_config, auth_provider=auth_provider, protocol_version=4
        )
        _session = _cluster.connect(settings.ASTRA_DB_KEYSPACE)
        # Execute a simple query to confirm connection
        row = _session.execute("SELECT release_version FROM system.local").one()
        if row:
            logger.info(
                f"Successfully connected to AstraDB. Cassandra version: {row.release_version}"
            )
        else:
            logger.warning("Connected to AstraDB, but couldn't verify version.")

    except Exception as e:
        logger.exception(f"Failed to connect to AstraDB: {e}")
        # Depending on application requirements, you might want to exit or handle differently
        raise RuntimeError(f"Could not connect to AstraDB: {e}") from e


def close_astra_connection():
    """Closes the AstraDB cluster connection."""
    global _cluster, _session
    if _cluster:
        logger.info("Closing AstraDB connection...")
        _cluster.shutdown()
        _cluster = None
        _session = None
        logger.info("AstraDB connection closed.")


def get_db_session() -> Session:
    """Dependency function to get the initialized AstraDB session."""
    if _session is None:
        # This situation should ideally not happen if lifespan events are used correctly
        logger.error("Database session requested but not initialized.")
        from fastapi import HTTPException

        raise HTTPException(status_code=503, detail="Database not available")
    return _session
