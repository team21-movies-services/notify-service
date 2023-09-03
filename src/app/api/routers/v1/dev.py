import logging
from typing import Any

from fastapi import APIRouter, Request, status

router = APIRouter(prefix="/dev", tags=["Dev"])

logger = logging.getLogger().getChild("dev-router")


@router.post(
    path="/debug_celery",
    status_code=status.HTTP_200_OK,
)
async def debug_celery(
    request: Request,
    task_name: str,
    args: list[Any],
):
    task = request.app.state.celery_provider.send_task(task_name, (args))
    return task.get()
