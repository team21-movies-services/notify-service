import os

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


# Название проекта. Используется в Swagger-документации
class ProjectConfig(BaseSettings):
    name: str = Field(default="notify_service_api", alias="PROJECT_NAME")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    jwt_secret_key: str = Field(default="secret_key", alias="JWT_SECRET_KEY")


# Настройки PostgreSQL
class PostgresConfig(BaseSettings):
    host: str = Field(default='localhost', alias='POSTGRES_HOST')
    port: int = Field(default=5432, alias='POSTGRES_HOST')
    db: str = Field(default='tasks', alias='POSTGRES_DB')
    user: str = Field(default='postgres', alias='POSTGRES_USER')
    password: str = Field(default='postgres', alias='POSTGRES_PASSWORD')

    @property
    def dsn(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=self.user,
            password=self.password,
            host=self.host,
            port=str(self.port),
            path=f"/{self.db}",
        )


class Settings(BaseSettings):
    project: ProjectConfig = ProjectConfig()
    postgres: PostgresConfig = PostgresConfig()


settings = Settings()

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
