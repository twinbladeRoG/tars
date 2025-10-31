import warnings
from typing import Annotated, Any, Literal

from pydantic import (
    AnyUrl,
    BeforeValidator,
    PostgresDsn,
    SecretStr,
    computed_field,
    model_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    SECRET_KEY: str = "change_this"

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.CORS_ORIGINS]

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "change_this"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field
    @property
    def CELERY_BACKEND_URI(self) -> str:
        uri = MultiHostUrl.build(
            scheme="db+postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path="celery",
        )
        return str(uri)

    LOCAL_LLM_HOST: str = "http://localhost:8090"
    LOCAL_LLM_SECRET: SecretStr = SecretStr("sk-no-key-required")

    EMBEDDING_MODEL_NAME: str = "bge-large-en-v1.5_fp32"
    EMBEDDING_MODEL_HOST: str = "http://localhost:9090"
    EMBEDDING_MODEL_SECRET: SecretStr = SecretStr("sk-no-key-required")

    OPEN_API_KEY: SecretStr = SecretStr("sk-no-key-required")

    VECTOR_DB_URL: str = "http://localhost:6333"

    REDIS_URL: str = "redis://localhost:6379"

    LOG_LEVEL: Literal["INFO", "DEBUG", "ERROR", "WARNING", "CRITICAL"] = "INFO"

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "change_this":
            message = (
                f'The value of {var_name} is "change_this", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)

        return self


settings = Settings()
