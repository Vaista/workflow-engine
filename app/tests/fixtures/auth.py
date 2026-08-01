import pytest

from app.schemas.auth import CurrentUser


@pytest.fixture
def current_user(user):

    return CurrentUser(
        user_id=user.user_id,
        org_id=user.org_id,
        org_unit_id=user.org_unit_id,
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        roles=[],
        permissions=[],
    )