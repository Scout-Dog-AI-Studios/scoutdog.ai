# Backend Development Rules & Guidelines (FastAPI + Poetry)

These rules ensure consistency, performance, and maintainability in the backend application (`apps/backend`).

## 1. Framework & Structure

- **Framework:** Utilize **FastAPI**.
- **Language:** Use **Python 3.10+**.
- **Structure:** Organize the application logically:
  - `app/`: Main application directory.
  - `app/main.py`: FastAPI application instance creation and middleware setup.
  - `app/api/`: API endpoint definitions.
    - `app/api/v1/`: Version 1 of the API.
    - `app/api/v1/endpoints/`: Individual endpoint files (e.g., `auth.py`, `greet.py`, `upload.py`) using `APIRouter`.
    - `app/api/v1/dependencies.py`: Reusable API dependencies.
  - `app/core/`: Core logic, configuration, settings.
    - `app/core/config.py`: Environment variable loading (using Pydantic Settings).
  - `app/models/` or `app/schemas/`: Pydantic models for request/response validation and data structures.
  - `app/services/`: Business logic layer (optional for simple endpoints, crucial for complex ones).
  - `app/db/`: Database connection and interaction logic (e.g., AstraDB client setup).
  - `tests/`: Pytest tests.
- **Entrypoint:** Use `uvicorn` for running the ASGI application (e.g., `poetry run uvicorn app.main:app --reload`).

## 2. Dependencies & Environment

- **Management:** Use **Poetry** to manage dependencies and the virtual environment via `pyproject.toml`.
- **Initialization:** Use `poetry init` to create `pyproject.toml` and `poetry add <package>` to add dependencies.
- **Locking:** Always commit the lock file (`poetry.lock`) to ensure reproducible builds.
- **Environment:** Poetry manages a virtual environment automatically. Activate it with `poetry shell` for interactive sessions or run commands directly via `poetry run <command>`.
- **Minimality:** Keep dependencies lean; only add what is necessary. Separate development dependencies (`poetry add --group dev <package>`).

## 3. Typing & Validation

- **Type Hints:** **Mandatory**. Use Python type hints for all function signatures, variables, and class attributes. Run `mypy` or similar type checkers in CI (`poetry run mypy .`).
- **Data Validation:** Use **Pydantic** models extensively for:
  - Request body validation.
  - Query parameter validation.
  - Response models (`response_model` in route decorators) for consistent output and auto-documentation.

## 4. API Design

- **RESTful Principles:** Adhere to REST conventions (proper HTTP methods, status codes, resource-based URLs).
- **Versioning:** Include API versioning in the URL path (e.g., `/api/v1/...`).
- **Naming:** Use `snake_case` for Python code (variables, functions, modules). Pydantic models can automatically handle conversion to `camelCase` for JSON payloads if needed via aliases.
- **Documentation:** Leverage FastAPI's automatic OpenAPI (`/docs`) and ReDoc (`/redoc`) documentation. Write clear Pydantic model descriptions and route summaries/descriptions.

## 5. Database Interaction (AstraDB)

- **Driver:** Use the official `cassandra-driver` (add via `poetry add cassandra-driver`).
- **Connection:** Manage the database session/client lifecycle appropriately. Use FastAPI's dependency injection (`Depends`) to provide sessions to API routes.
- **Abstraction:** Consider a thin abstraction layer or service functions for database operations rather than direct driver calls within endpoint functions.
- **Models:** Define Pydantic models that correspond to database table structures for clarity, even though Cassandra is schemaless.

## 6. Configuration & Environment Variables

- **Loading:** Use Pydantic's `BaseSettings` to load configuration from environment variables. Add `python-dotenv` (`poetry add python-dotenv`) if loading from `.env` files locally is desired.
- **Files:** Use `.env` for local development (add to `.gitignore`).
- **Schema:** Document all required environment variables in `.env.example`.
- **Secrets:** Never commit secrets directly into the codebase. Load from environment variables provided by the hosting platform (Railway).

## 7. Authentication & Authorization

- **Mechanism:** Secure endpoints using JWT validation middleware compatible with Auth0 (e.g., using `python-jose`). Add via `poetry add "python-jose[cryptography]"`.
- **Dependencies:** Use FastAPI's dependency injection system to handle token validation and retrieval of authenticated user information.
- **Scopes/Permissions:** Implement scope/permission checks if needed beyond simple authentication.

## 8. Error Handling

- **Custom Exceptions:** Define custom exception classes for specific application errors.
- **Exception Handlers:** Use FastAPI's `@app.exception_handler` to catch custom exceptions and standard HTTPExceptions, returning consistent JSON error responses.
- **Validation Errors:** Rely on FastAPI's default handling for Pydantic validation errors, which returns informative 422 responses.

## 9. Logging & Monitoring

- **Logging:** Use Python's standard `logging` module. Configure it for appropriate levels and formats.
- **Sentry:** Integrate the Sentry SDK (`poetry add "sentry-sdk[fastapi]"`) early for error reporting. Configure the DSN via environment variables.
- **Request Logging:** Consider middleware for logging basic request/response information if not adequately provided by the platform.

## 10. Testing

- **Framework:** Use `pytest` (`poetry add --group dev pytest`).
- **Client:** Use FastAPI's `TestClient` or `httpx` for testing API endpoints (`poetry add --group dev httpx`).
- **Execution:** Run tests via `poetry run pytest`.
- **Coverage:** Aim for good test coverage, especially for business logic (services) and critical API endpoints.
- **Database:** Mock database interactions or use a test database/keyspace where appropriate.
