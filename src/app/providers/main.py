import logging

from fastapi import FastAPI

from core.config import Settings
from providers.admin_provider import AdminProvider
from providers.celery_provider import CeleryProvider

logger = logging.getLogger(__name__)


def setup_providers(app: FastAPI, settings: Settings):
    celery_provider = CeleryProvider(app=app, settings=settings)
    celery_provider.register_events()
    logger.info(f"Setup Celery Provider. host: {settings.celery.host}")

    admin_provider = AdminProvider(app=app, settings=settings.admin)
    admin_provider.register_events()
    logger.info("Setup Admin Provider.")
