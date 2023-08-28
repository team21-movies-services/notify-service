import logging

from fastapi import FastAPI

from core.config import Settings

logger = logging.getLogger(__name__)


def setup_providers(app: FastAPI, settings: Settings):
    pass
