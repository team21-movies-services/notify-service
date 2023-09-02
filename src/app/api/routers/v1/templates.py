import logging
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse

from services.templates import TemplatesServiceABC

router = APIRouter(prefix="/templates", tags=["Templates"])

logger = logging.getLogger().getChild("templates-router")


@router.get(
    "/{template_id}/show",
    summary="Посмотреть шаблон",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
async def _show_template(
    template_id: UUID,
    template_service: TemplatesServiceABC = Depends(),
):
    logger.debug(f"Get template {template_id}")

    return await template_service.render_template(template_id)
