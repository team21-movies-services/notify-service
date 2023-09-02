from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from providers import BaseProvider


class SQLAlchemyProvider(BaseProvider):
    def __init__(
        self,
        app: FastAPI,
        async_dns: str,
        echo_log: bool = False,
    ):
        self.app = app
        self.async_dns = async_dns
        self.echo_log = echo_log

    async def startup(self):
        """FastAPI startup event"""
        self.async_engine = create_async_engine(
            self.async_dns,
            echo=self.echo_log,
            max_overflow=20,
            pool_size=10,
        )
        setattr(self.app.state, "async_engine", self.async_engine)

        self.async_session_maker = async_sessionmaker(
            self.async_engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
        )

        setattr(self.app.state, "async_session_maker", self.async_session_maker)

    async def shutdown(self):
        """FastAPI shutdown event"""
        if self.async_engine:
            await self.async_engine.dispose()
