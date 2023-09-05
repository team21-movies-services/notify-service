from celery import Celery
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from dependencies.clients.get_db_session import get_db_session
from dependencies.registrator import add_factory_to_mapper
from repositories.events import EventsRepository
from services.events import EventsService, EventsServiceABC

celery_app = Celery(
    settings.celery.app_name,
    broker=settings.celery.broker,
    backend=settings.celery.backend,
)


@add_factory_to_mapper(EventsServiceABC)
def create_events_service(
    session: AsyncSession = Depends(get_db_session),
    celery_app: Celery = celery_app,
) -> EventsService:
    return EventsService(EventsRepository(session), celery_app)
