from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    ("route", "params", "json", "expected_status"),
    [
        ("/api/v1/status", None, None, HTTPStatus.OK),
        (
            "/api/v1/events",
            None,
            {
                "event_data": {"email": "123@example.com", "user_id": "4042222c-07c2-4316-8b4b-a0cbc4ece7b6"},
                "event_name": "users.created",
                "event_time": "123",
            },
            HTTPStatus.NOT_FOUND,
        ),
    ],
)
@pytest.mark.asyncio()
async def test_status(api_client, route, params, expected_status, json):
    response = await api_client.post(route, json=json)
    assert response.status_code == expected_status
