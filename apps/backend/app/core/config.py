from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Auth0 Variables
    AUTH0_DOMAIN: str
    AUTH0_API_AUDIENCE: str

    # AstraDB Config
    ASTRA_DB_SECURE_BUNDLE_PATH: str
    ASTRA_DB_CLIENT_ID: str
    ASTRA_DB_CLIENT_SECRET: str
    ASTRA_DB_KEYSPACE: str

    # R2 Cloudflare Variables
    R2_BUCKET_NAME: str
    R2_ACCOUNT_ID: str
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str
    R2_ENDPOINT_URL: str
    R2_PUBLIC_URL_BASE: str

    # Load from .env file if present
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore
