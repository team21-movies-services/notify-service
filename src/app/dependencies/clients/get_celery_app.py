from celery import Celery
from fastapi import FastAPI, Request


def get_celery_app(
    request: Request,
) -> Celery:
    app: FastAPI = request.app
    celery_app: Celery = app.state.celery_provider
    return celery_app
