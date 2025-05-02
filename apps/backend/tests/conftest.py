import pytest
import pytest_asyncio  # Import the asyncio plugin decorator

from httpx import AsyncClient  # Import AsyncClient for async testing
import sys
import os

# Add the 'app' directory to the Python path so modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the FastAPI app instance from your main application file
# Ensure this import path matches your project structure
from app.main import app as fastapi_app  # Rename to avoid conflict

# Note: Database/External Service setup/mocking fixtures would also go here later


@pytest.fixture(scope="session")  # Use session scope for app instance
def test_app_instance():
    """Yields the FastAPI app instance for testing setup."""
    # Any setup specific to the app instance before yielding can go here
    yield fastapi_app
    # Any teardown after tests run can go here


@pytest_asyncio.fixture(
    scope="function"
)  # Use function scope for client - ensures isolation
async def test_client(test_app_instance):
    """
    Creates an async TestClient instance for making requests to the app.
    Uses function scope for test isolation.
    """
    # Base URL is important for async client
    # Use 'http://testserver' as it's commonly used by TestClient/httpx for testing
    async with AsyncClient(
        app=test_app_instance, base_url="http://testserver"
    ) as client:
        yield client


# Example of a synchronous client fixture if needed (less common for async FastAPI)
# @pytest.fixture(scope="function")
# def sync_test_client(test_app_instance):
#     """Creates a synchronous TestClient instance."""
#     with TestClient(test_app_instance) as client:
#         yield client
