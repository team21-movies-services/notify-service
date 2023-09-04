from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")
    host: str = Field(default='localhost')
    port: int = Field(default=5432)
    db: str = Field(default='test')
    user: str = Field(default='leonid')
    password: str = Field(default='AcidMac12')

    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db,
        )


# Настройки Celery
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


class ProjectConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SCHEDULER_")
    log_level: str = Field(default="INFO")
    check_interval: int = Field(default=60)


class Settings(BaseModel):
    project: ProjectConfig = ProjectConfig()
    postgres: PostgresConfig = PostgresConfig()
    celery: CeleryConfig = CeleryConfig()


settings = Settings()
