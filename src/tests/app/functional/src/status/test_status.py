from http import HTTPStatus

import pytest


@pytest.mark.asyncio()
async def test_status(api_client):
    response = await api_client.post('api/v1/status')
    assert response.status_code == HTTPStatus.OK
