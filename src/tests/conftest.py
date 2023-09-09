import asyncio

import pytest

pytest_plugins = ("tests.functional.plugins.api_client",)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
