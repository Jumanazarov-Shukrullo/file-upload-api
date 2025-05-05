import pytest
from httpx import AsyncClient
from main import app
from db.session import Base, engine
from core.config import settings
from jose import jwt

@pytest.fixture(scope="module", autouse=True)

def setup():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.mark.asyncio
async def test_upload(tmp_path, monkeypatch):
    # Create dummy file
    file_path = tmp_path / "test.txt"
    file_path.write_bytes(b"hello world")

    token = jwt.encode({"sub": "test"}, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/upload",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("test.txt", open(file_path, "rb"), "text/plain")}
        )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["url"].startswith("http://")