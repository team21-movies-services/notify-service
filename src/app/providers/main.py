import logging

from core.config import Settings
from fastapi import FastAPI

logger = logging.getLogger(__name__)


def setup_providers(app: FastAPI, settings: Settings):
    pass
