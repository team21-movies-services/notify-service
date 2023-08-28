import os

from pydantic import Field
from pydantic_settings import BaseSettings


# Название проекта. Используется в Swagger-документации
class ProjectConfig(BaseSettings):
    name: str = Field(default="notify_service_api", alias="PROJECT_NAME")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    jwt_secret_key: str = Field(default="secret_key", alias="JWT_SECRET_KEY")


class Settings(BaseSettings):
    project: ProjectConfig = ProjectConfig()


settings = Settings()

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
