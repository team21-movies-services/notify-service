import logging
from uuid import UUID
from fastapi import APIRouter, Depends, status, Request

from app.schemas.response.status import StatusResponse
from app.services.status import StatusServiceABC

router = APIRouter(prefix="/status", tags=["Status"])

logger = logging.getLogger().getChild("status-router")


@router.post(
    "",
    summary="Получить статус API",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
)
async def _get_api_status(
    status_service: StatusServiceABC = Depends(),
) -> StatusResponse:
    logger.debug("Get api status")
    return await status_service.get_api_status()


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
)
async def get_template(request: Request, get_template: UUID):
    task = request.app.state.celery_provider.send_task("get_template", (get_template,))
    return task.get()
