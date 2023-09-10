import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from tests.app.functional.mocks.queue_notify_service import (
    QueueNotifyServiceMock,
    get_queue_notify_service_mock,
)

from app.dependencies.service_dependencies.queue_notify_service import (
    create_queue_notify_service,
)
from app.main import app
from app.schemas.auth import AuthData
from app.services.queue_notify import QueueNotifyServiceProtocol


@pytest.mark.asyncio()
async def test_post_notifications(ws_client: TestClient, auth_user_ws: tuple[AuthData, str], mocker: MockerFixture):
    user_id = auth_user_ws[0].user_id
    app.dependency_overrides[QueueNotifyServiceProtocol] = get_queue_notify_service_mock
    spy = mocker.spy(QueueNotifyServiceMock, "get_new_messages")

    with ws_client.websocket_connect("/ws/notifications") as websocket:
        answer = websocket.receive_text()

    assert answer == "No new notifications"
    assert spy.call_count == 1
    assert spy.call_args.__contains__(user_id)

    app.dependency_overrides[QueueNotifyServiceProtocol] = create_queue_notify_service
