from http import HTTPStatus

import pytest
from tests.app.functional.utils.schemas import EventResponse


@pytest.mark.parametrize(
    ("route", "json", "expected_status"),
    [
        (
            "/api/v1/events",
            {
                "event_data": {"email": "123@example.com", "user_id": "4042222c-07c2-4316-8b4b-a0cbc4ece7b6"},
                "event_name": "users.created",
                "event_time": "123",
            },
            HTTPStatus.OK,
        ),
        (
            "/api/v1/events",
            {
                "event_data": {"film_id": "4042222c-07c2-4316-8b4b-a0cbc4ece7b3"},
                "event_name": "films.new",
                "event_time": "123",
            },
            HTTPStatus.OK,
        ),
    ],
)
@pytest.mark.asyncio()
async def test_event(api_client, fill_db, route, expected_status, json):
    response = await api_client.post(route, json=json)
    body = response.json()
    assert response.status_code == expected_status
    assert body == EventResponse(**body).model_dump()


@pytest.mark.parametrize(
    ("route", "json", "expected_status"),
    [
        (
            "/api/v1/events",
            {
                "event_data": {"email": "123@example.com", "user_id": "4042222c-07c2-4316-8b4b-a0cbc4ece7b6"},
                "event_name": "test",
                "event_time": "123",
            },
            HTTPStatus.NOT_FOUND,
        ),
    ],
)
@pytest.mark.asyncio()
async def test_unexpected_event(api_client, route, expected_status, json):
    response = await api_client.post(route, json=json)
    body = response.json()
    assert response.status_code == expected_status
    assert body == {"detail": "Notification not found"}
