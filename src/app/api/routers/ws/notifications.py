import fastapi

from app.dependencies.auth import get_ws_auth_data
from app.schemas.auth import AuthData
from app.services.queue_notify import QueueNotifyServiceProtocol

router = fastapi.APIRouter(prefix="/notifications")


@router.websocket("")
async def websocket_endpoint(
    websocket: fastapi.WebSocket,
    access: tuple[AuthData | None, str] = fastapi.Depends(get_ws_auth_data),
    queue_service: QueueNotifyServiceProtocol = fastapi.Depends(),
):
    auth_data, message = access

    await websocket.accept()

    try:
        if not auth_data:
            raise fastapi.WebSocketException(code=fastapi.status.WS_1008_POLICY_VIOLATION, reason=message)

        async for message in queue_service.get_new_messages(auth_data.user_id):
            await websocket.send_text(f"{message}")

    except fastapi.WebSocketException as err:
        await websocket.close(code=err.code, reason=err.reason)
    else:
        await websocket.close()
