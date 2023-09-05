from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.clients.get_db_session import get_db_session
from dependencies.registrator import add_factory_to_mapper
from repositories.events import EventsRepository
from services.events import EventsService, EventsServiceABC


@add_factory_to_mapper(EventsServiceABC)
def create_events_service(session: AsyncSession = Depends(get_db_session)) -> EventsService:
    return EventsService(EventsRepository(session))
