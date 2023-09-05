from celery import Celery
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.dependencies.clients.get_db_session import get_db_session
from app.dependencies.registrator import add_factory_to_mapper
from app.repositories.events import EventsRepository
from app.services.events import EventsService, EventsServiceABC

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
