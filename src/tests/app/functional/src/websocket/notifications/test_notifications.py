import pytest
from fastapi import WebSocketDisconnect
from fastapi.testclient import TestClient


@pytest.mark.asyncio()
async def test_post_notifications_not_auth(ws_client: TestClient):
    with ws_client.websocket_connect("/ws/notifications") as websocket:
        with pytest.raises(WebSocketDisconnect) as exc_info:
            _ = websocket.receive_json()

        assert exc_info.value.code == 1008
        assert exc_info.value.reason == "UNAUTHORIZED"
