import logging

from fastapi import FastAPI

from core.config import Settings
from providers.celery_provider import CeleryProvider
from providers.pg_providers import SQLAlchemyProvider

logger = logging.getLogger(__name__)


def setup_providers(app: FastAPI, settings: Settings):
    celery_provider = CeleryProvider(app=app, settings=settings)
    celery_provider.register_events()
    logger.info(f"Setup Celery Provider. host: {settings.celery.host}")

    sa_provider = SQLAlchemyProvider(
        app=app,
        async_dns=settings.postgres.database_url,
        echo_log=settings.postgres.echo_log,
    )
    sa_provider.register_events()
    logger.info(f"Setup SQLAlchemy Provider. DSN: {settings.postgres.database_url}")
