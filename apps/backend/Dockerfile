# Copy the virtual environment with dependencies created by Poetry from the builder stage
# Poetry installs venvs in a specific location, often /root/.cache/pypoetry/virtualenvs/
# We need to find the correct venv path or configure Poetry to create it locally.
# Safer approach: Copy the installed packages directly from site-packages

# Let's configure poetry to create the venv inside the project directory in the builder stage
# Add this config command BEFORE poetry install in the builder stage:
# RUN poetry config virtualenvs.in-project true

# --- Re-run the builder stage with the venv config ---

# Corrected Stage 1 (Builder) with venv config:
    FROM python:3.10-slim as builder

    RUN apt-get update && \
        apt-get install -y --no-install-recommends python3-pip python3-venv git curl && \
        rm -rf /var/lib/apt/lists/*
    
    RUN python3 -m pip install --upgrade pip
    RUN python3 -m pip install pipx
    RUN python3 -m pipx ensurepath
    ENV PATH="/root/.local/bin:$PATH"
    
    RUN pipx install poetry
    
    WORKDIR /app
    COPY pyproject.toml poetry.lock* ./
    
    # Configure Poetry to create the virtual environment inside the project directory
    RUN poetry config virtualenvs.in-project true
    
    # Now install dependencies - this will create a .venv directory in /app
    RUN poetry install --no-root --only main --no-interaction --no-ansi
    
    
    # Corrected Stage 2 (Runtime):
    FROM python:3.10-slim
    
    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1
    WORKDIR /app
    
    # Copy the virtual environment created locally by Poetry in the builder stage
    COPY --from=builder /app/.venv /app/.venv
    
    # Copy the application code
    COPY ./app /app/app
    
    # Activate the virtual environment by setting PATH
    ENV PATH="/app/.venv/bin:$PATH"
    
    # Expose the port the app runs on
    EXPOSE 8000
    ENV PORT=8000
    CMD ["bash","-c","uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]