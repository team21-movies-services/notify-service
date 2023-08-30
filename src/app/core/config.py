import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Название проекта. Используется в Swagger-документации
class ProjectConfig(BaseSettings):
    name: str = Field(default="notify_service_api", alias="PROJECT_NAME")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    jwt_secret_key: str = Field(default="secret_key", alias="JWT_SECRET_KEY")


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


class Settings(BaseSettings):
    project: ProjectConfig = ProjectConfig()
    celery: CeleryConfig = CeleryConfig()


settings = Settings()

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
