from celery import Celery
from core.config import Settings
from fastapi import FastAPI
from providers import BaseProvider


class CeleryProvider(BaseProvider):
    def __init__(self, app: FastAPI, settings: Settings):
        self.app = app
        self.celery_client = Celery(
            broker=settings.celery.broker,
            backend=settings.celery.backend,
            app=settings.celery.app_name,
        )

    def startup(self):
        """FastAPI startup event"""
        setattr(self.app.state, "celery_provider", self.celery_client)

    def shutdown(self):
        """FastAPI shutdown event"""
        if self.celery_client:
            self.celery_client.close()
