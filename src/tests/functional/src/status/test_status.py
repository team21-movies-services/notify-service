import pytest


@pytest.mark.asyncio()
async def test_healthcheck(api_client):
    response = await api_client.post("/api/v1/status")
    assert response.status_code == 200
