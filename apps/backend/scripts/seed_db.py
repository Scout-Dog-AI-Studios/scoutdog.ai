import sys
import os
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import logging
import uuid

# Load .env from the parent directory (apps/backend/.env)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
# Add the app directory to the Python path to import config etc.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Try to import settings; handle potential import error if script run standalone
try:
    from app.core.config import settings
except ImportError:
    print(
        "Error: Could not import settings. Make sure PYTHONPATH is set or run via 'poetry run'."
    )
    print(
        "Attempting to load settings from environment variables directly (if needed)..."
    )
    exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_data():
    """Connects to AstraDB and inserts initial data."""
    cluster = None  # Initialize cluster to None
    try:
        logger.info("Seeding script started.")
        bundle_path = settings.ASTRA_DB_SECURE_BUNDLE_PATH
        if not os.path.isabs(bundle_path):
            bundle_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", bundle_path)
            )
        if not os.path.exists(bundle_path):
            logger.error(
                f"Astra Secure Connect Bundle not found at path: {bundle_path}"
            )
            raise FileNotFoundError(
                f"Astra Secure Connect Bundle not found at {bundle_path}"
            )

        cloud_config = {"secure_connect_bundle": bundle_path}
        auth_provider = PlainTextAuthProvider(
            settings.ASTRA_DB_CLIENT_ID, settings.ASTRA_DB_CLIENT_SECRET
        )
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        session = cluster.connect(settings.ASTRA_DB_KEYSPACE)
        logger.info("Connected to AstraDB for seeding.")

        # Prepare insert statement (Parameterized is safer)
        insert_cql = f"INSERT INTO {settings.ASTRA_DB_KEYSPACE}.greetings (id, message) VALUES (?, ?)"
        prepared = session.prepare(insert_cql)
        greetings = [
            "Hello from AstraDB!",
            "Welcome to the Hello World backend!",
            "Database integration successful!",
        ]
        for msg in greetings:
            session.execute(prepared, (uuid.uuid4(), msg))
            logger.info(f"Inserted greeting: {msg}")
        logger.info("Seeding completed successfully.")
    except Exception as e:
        logger.exception(f"Error during seeding: {e}")
    finally:
        if cluster:
            cluster.shutdown()
            logger.info("AstraDB cluster connection closed.")


if __name__ == "__main__":
    seed_data()
