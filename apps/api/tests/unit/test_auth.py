import pytest
from httpx import AsyncClient
from app.main import app
from app.core.database import get_db

@pytest.mark.asyncio
async def test_health_check(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
