from aio_pika import connect
from fastapi import FastAPI

from app.core.config import AMPQConfig
from app.providers import BaseProvider


class AMPQProvider(BaseProvider):
    def __init__(self, app: FastAPI, settings: AMPQConfig):
        self.app = app
        self.connection = connect(settings.broker)

    async def startup(self):
        """FastAPI startup event"""
        self.connection = await self.connection  # type: ignore
        setattr(self.app.state, "ampq_connection", self.connection)

    async def shutdown(self):
        """FastAPI shutdown event"""
        await self.connection.close()  # type: ignore
