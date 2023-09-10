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


@pytest.mark.asyncio()
async def test_post_notifications_forbidden(ws_client: TestClient, forbidden_access_token: str):
    headers = {'Authorization': forbidden_access_token}

    with ws_client.websocket_connect("/ws/notifications", headers=headers) as websocket:
        with pytest.raises(WebSocketDisconnect) as exc_info:
            _ = websocket.receive_json()

        assert exc_info.value.code == 1008
        assert exc_info.value.reason == "FORBIDDEN"


@pytest.mark.asyncio()
async def test_post_notifications_expire_token(ws_client: TestClient, expire_access_token: str):
    headers = {'Authorization': expire_access_token}

    with ws_client.websocket_connect("/ws/notifications", headers=headers) as websocket:
        with pytest.raises(WebSocketDisconnect) as exc_info:
            _ = websocket.receive_json()

        assert exc_info.value.code == 1008
        assert exc_info.value.reason == "TOKEN EXPIRED"
