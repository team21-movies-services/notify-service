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


class NotificationsConfig(BaseSettings):
    user_api: str = Field(default="https://d90746a7-1563-46ce-9a3d-8d173a6f8bda.mock.pstmn.io")

    @property
    def users_list_url(self) -> str:
        return self.user_api + "/api/v1/notifications/users/?event_name={event_name}"

    @property
    def user_info_url(self) -> str:
        return self.user_api + "/api/v1/notifications/users/?user_id={user_id}"
