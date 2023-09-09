from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CeleryConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CELERY_")
    user: str = Field(default="guest")
    password: str = Field(default="guest")
    host: str = Field(default="notify-service-rabbitmq")
    app_name: str = Field(default="notify")

    @property
    def broker(self) -> str:
        return f"pyamqp://{self.user}:{self.password}@{self.host}"

    @property
    def backend(self) -> str:
        return f"rpc://{self.user}:{self.password}@{self.host}"


# Настройки Sentry
class SentryConfig(BaseSettings):
    dsn: str = Field(default="dsn", alias='SENTRY_DSN')
    enable: bool = Field(default=True, alias='SENTRY_ENABLE')


# Настройки PostgreSQL
class PostgresConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='postgres_')
    host: str = Field(default='localhost')
    port: int = Field(default=5432)
    db: str = Field(default='notify_database')
    user: str = Field(default='notify')
    password: str = Field(default='notify')
    echo_log: bool = Field(default=False)

    @property
    def database_url(self):
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class UsersApiConfig(BaseSettings):
    host: str = Field(default="https://d90746a7-1563-46ce-9a3d-8d173a6f8bda.mock.pstmn.io")

    @property
    def list_uri(self) -> str:
        return self.host + "/api/v1/notifications/users/?event_name={event_name}"

    @property
    def info_uri(self) -> str:
        return self.host + "/api/v1/notifications/users/?user_id={user_id}"

    @property
    def get_confirmation_uri(self) -> str:
        return self.host + "/api/v1/notifications/confirm/?user_id={user_id}"


class FilmsApiConfig(BaseSettings):
    host: str = Field(default="https://d90746a7-1563-46ce-9a3d-8d173a6f8bda.mock.pstmn.io")

    @property
    def new_uri(self) -> str:
        return self.host + "/api/v1/films/new?from_date={from_date}"


class TinyUrlApiConfig(BaseSettings):
    host: str = Field(default="https://api.tinyurl.com")
    token: str = Field(default="ihDsRF83DjIczDPSS2e2ozKByQEd655xQFqFW4jG9v8vdQvEeXFh2pk3QH1j")

    @property
    def shortener_uri(self) -> str:
        return self.host + "/create"


class EmailProvidersConfig(BaseSettings):
    host: str = Field(default="https://aaddb410-31ce-4f81-8ff2-d1d8114cfc6b.mock.pstmn.io")
    token: str = Field(default="123456")

    def send_email_uri(self):
        return self.host + "/send-email"


# Настройки внешних API
class APIsConfig(BaseSettings):
    users: UsersApiConfig = UsersApiConfig()
    films: FilmsApiConfig = FilmsApiConfig()
    tinyurl: TinyUrlApiConfig = TinyUrlApiConfig()
    email_providers: EmailProvidersConfig = EmailProvidersConfig()
