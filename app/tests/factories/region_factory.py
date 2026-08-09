import pytest

from app.models.region import Regions


@pytest.fixture
def region_factory(db_session):
    """
    Factory for creating Region model instances.

    Usage:
        region = region_factory()
        region = region_factory(name="Region 1", code="R1")
    """

    def create_region(**kwargs):

        data = {
            "name": "Region 1",
            "code": "R1",
        }

        data.update(kwargs)

        region = Regions(**data)

        db_session.add(region)

        # Writes to DB without committing.
        db_session.flush()

        # Populates generated fields like id.
        db_session.refresh(region)

        return region

    return create_region