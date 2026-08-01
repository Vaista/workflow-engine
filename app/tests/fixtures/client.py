import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.deps import get_current_user
from app.api.deps import get_db


@pytest.fixture
def client(db_session, current_user):

    def override_get_db():
        yield db_session

    async def override_current_user():
        return current_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_current_user

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()