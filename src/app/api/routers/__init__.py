from fastapi import APIRouter

from .v1 import v1_router
from .ws import websocket

api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)

router = APIRouter()
router.include_router(api_router)
router.include_router(websocket)
