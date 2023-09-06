from fastapi import APIRouter

from .notifications import router as notification_websocket

websocket = APIRouter(prefix="/ws")

websocket.include_router(notification_websocket)
