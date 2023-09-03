from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.clients.get_db_session import get_db_session
from app.dependencies.registrator import add_factory_to_mapper
from app.repositories.templates import TemplatesRepository
from app.services.templates import TemplatesService, TemplatesServiceABC


@add_factory_to_mapper(TemplatesServiceABC)
def create_templates_service(session: AsyncSession = Depends(get_db_session)) -> TemplatesService:
    return TemplatesService(TemplatesRepository(session))
