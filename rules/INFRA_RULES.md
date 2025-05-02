# Infrastructure & DevOps Rules

These rules cover monorepo management, deployment, environment configuration, and cloud services.

## 1. Monorepo Management (Turborepo)

- **Structure:** Adhere to the `apps/*` and `packages/*` structure defined by Turborepo.
  - `apps/frontend`: Next.js application.
  - `apps/backend`: FastAPI application.
  - `packages/ui`: (Optional) Shared React components.
  - `packages/config`: Shared configurations (e.g., ESLint, TSConfig).
- **Task Runner:** Use `pnpm` workspaces and `turbo` for running tasks (`build`, `dev`, `lint`, `test`) across the monorepo. Define pipelines in `turbo.json`.
- **Commands:** Prefer running tasks via `turbo run <task> --filter=<app/package>` or root `pnpm <task>` scripts that utilize `turbo`.

## 2. Version Control (Git)

- **Branching:** Use a simple Gitflow-like model:
  - `main`: Production-ready code. Deploys to production.
  - `dev`: Development integration branch. Deploys to staging/development environment.
  - `feat/...`: Feature branches branched off `dev`.
- **Commits:** Write clear, concise commit messages. Consider Conventional Commits standard.
- **Pull Requests:** Use Pull Requests for merging features into `dev` and `dev` into `main`. Require reviews if working in a team.
- **`.gitignore`:** Maintain a comprehensive root `.gitignore` file covering common files (`.env`, `node_modules`, `__pycache__`, build artifacts, OS files).

## 3. Environment Variables & Secrets

- **Source of Truth:** `.env.example` files in each app/package define _required_ variables.
- **Local Development:** Use `.env` (backend) and `.env.local` (frontend), added to `.gitignore`.
- **Deployment:** Configure environment variables and secrets _exclusively_ through the hosting platform's UI or CLI (Railway, Vercel). **Never commit secrets.**
- **Naming:** Use consistent, descriptive names for variables (e.g., `DATABASE_URL`, `AUTH0_CLIENT_ID`, `R2_BUCKET_NAME`).

## 4. CI/CD

- **Trigger:** Automate deployments based on pushes/merges to `dev` and `main` branches using GitHub Actions or platform-native deploy hooks (Railway/Vercel).
- **Pipeline Steps:** CI pipeline should typically include:
  - Checkout code.
  - Setup Node.js/pnpm.
  - **Setup Python and Poetry.**
  - Install frontend dependencies (`pnpm install`).
  - **Install backend dependencies (`cd apps/backend && poetry install --no-root --sync`)**. Use `--no-dev` for production builds.
  - Run Linters (`turbo run lint`). Optionally run backend linting directly: `cd apps/backend && poetry run ruff check . && poetry run black --check .`
  - Run Tests (`turbo run test`). Optionally run backend tests directly: `cd apps/backend && poetry run pytest`
  - Build applications (`turbo run build --filter=frontend`). Backend build might involve type checking (`cd apps/backend && poetry run mypy .`) or is handled by Docker build later.
  - Deploy to the corresponding environment (via Railway/Vercel integrations, which will often build the Docker image for the backend).
- **Turborepo Caching:** Leverage Turborepo's remote caching (if configured) to speed up CI builds.
- **Backend Docker Build:** The Dockerfile for the backend (`apps/backend/Dockerfile`) should typically:
  - Start from a standard Python base image (e.g., `python:3.10-slim`).
  - Install Poetry.
  - Set the working directory (`WORKDIR /app`).
  - Copy `pyproject.toml` and `poetry.lock`.
  - Run `poetry install --no-dev --no-root --sync` to install production dependencies based on the lock file.
  - Copy the application code (`COPY ./app /app/app`).
  - Define the `CMD` or `ENTRYPOINT` to run `uvicorn`.

## 5. Hosting (Railway / Vercel)

- **Platform Choice:** Use Railway for the FastAPI backend (and potentially database). Use Vercel or Railway for the Next.js frontend.
- **Configuration:** Configure build commands and root directories correctly for the monorepo structure.
- **Environments:** Maintain separate `dev` and `prod` environments.

## 6. Database (AstraDB)

- **Provisioning:** Provision via the DataStax Astra portal.
- **Credentials:** Store connection tokens/bundles securely in hosting platform secrets.
- **Schema Management:** For Cassandra's flexible schema:
  - Document expected table structures and types clearly.
  - Use backend application startup checks or simple migration scripts (run manually, via `poetry run python scripts/migrate.py`, or in CI) to ensure required tables/keyspaces exist.

## 7. Object Storage (Cloudflare R2)

- **Provisioning:** Create buckets via the Cloudflare dashboard.
- **Credentials:** Store Access Key ID and Secret Access Key securely in hosting platform secrets.
- **CORS:** Configure CORS policies on the bucket to allow `GET` requests from your frontend domain(s).
- **Public Access:** Ensure bucket settings allow public read access if files are intended to be served directly.

## 8. DNS & SSL (Cloudflare)

- **Management:** Manage DNS records through Cloudflare.
- **Records:** Point necessary A/CNAME records to Railway/Vercel endpoints.
- **SSL:** Use Cloudflare's Universal SSL or configure custom certificates. Ensure SSL mode is "Full (Strict)" for end-to-end encryption.

## 9. Monitoring & Logging (Sentry / Platform Logs)

- **Error Tracking:** Ensure Sentry DSNs are configured correctly in all environments via environment variables.
- **Platform Logs:** Utilize logs provided by Railway/Vercel for request tracing and basic application output.
- **Alerting:** Configure Sentry alerts for new or critical issues, potentially integrating with Slack/Email.
