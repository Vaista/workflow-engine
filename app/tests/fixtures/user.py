import pytest

from app.models.user import Users


@pytest.fixture
def user(db_session, organization_unit):

    user = Users(
        org_id=organization_unit.org_id,
        org_unit_id=organization_unit.org_unit_id,
        name="Test User",
        email="test@email.com",
        password_hash="Password Hash",
        contact="contact number",
        country="India"
    )

    db_session.add(user)
    db_session.commit()

    db_session.refresh(user)

    return user
