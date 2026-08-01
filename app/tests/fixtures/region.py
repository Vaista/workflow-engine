import pytest

from app.models.region import Regions


@pytest.fixture
def region(db_session):

    new_region = Regions(
        name="Asia Pacific",
        code="APAC"
    )

    db_session.add(new_region)
    db_session.commit()

    db_session.refresh(new_region)

    return new_region