from fastapi import APIRouter

from .dev import router as dev_router
from .events import router as events_router
from .status import router as status_router
from .templates import router as template_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(status_router)
v1_router.include_router(template_router)
v1_router.include_router(dev_router)
v1_router.include_router(events_router)
