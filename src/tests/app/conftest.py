import pytest

from app.core.config import settings


@pytest.fixture(name="settings", scope="session")
def get_settings():
    return settings
