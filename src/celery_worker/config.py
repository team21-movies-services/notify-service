import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


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
