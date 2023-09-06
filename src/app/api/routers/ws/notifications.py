import fastapi

from app.dependencies.auth import get_ws_auth_data
from app.schemas.auth import AuthData

router = fastapi.APIRouter(prefix="/notifications")


@router.websocket("")
async def websocket_endpoint(
    websocket: fastapi.WebSocket,
    access: tuple[AuthData | None, str] = fastapi.Depends(get_ws_auth_data),
):
    auth_data, message = access

    await websocket.accept()

    try:
        if not auth_data:
            raise fastapi.WebSocketException(code=fastapi.status.WS_1008_POLICY_VIOLATION, reason=message)
        while True:
            _ = await websocket.receive_text()
            await websocket.send_text(f"user_id: {auth_data.user_id}")
    except (fastapi.WebSocketDisconnect, fastapi.WebSocketException) as err:
        await websocket.close(code=err.code, reason=err.reason)
