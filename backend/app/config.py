"""Configuration, read from the environment (.env) at startup.

Mirrors the original Flask app's env vars (DB_*, SECRET_KEY) so nothing about
the deployment secrets changes, and adds a few new ones for the rebuild.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Postgres (mutable collection)
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_ADDRESS: str | None = None
    DB_PORT: str = "5432"
    DB_NAME: str | None = None

    # Secrets / auth
    SECRET_KEY: str = "you-will-never-guess"          # reused from Flask config
    EDIT_PASSWORD: str | None = None                  # falls back to legacy in security.py

    # SQLite reference data (read-only)
    LOCAL_DB_PATH: str = "../app/lotalf.db"

    # CORS + scanner
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"
    SCAN_SCRIPT: str = "C:/Users/Alfonso/Tools/scan_duplex.ps1"

    # OCR: Claude vision reads the administración seal off the scanned décimo
    ANTHROPIC_API_KEY: str | None = None
    ANTHROPIC_MODEL: str = "claude-opus-4-8"  # best accuracy on the faint administración seals
    # Retried ONLY when opus reads no seal — opus is conservative and returns
    # nothing on very faint stamps, where sonnet-5 will still read them. Set empty
    # to disable the fallback.
    ANTHROPIC_FALLBACK_MODEL: str = "claude-sonnet-5"

    @property
    def postgres_url(self) -> str | None:
        if not all([self.DB_USER, self.DB_PASSWORD, self.DB_ADDRESS, self.DB_NAME]):
            return None
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_ADDRESS}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def cors_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
