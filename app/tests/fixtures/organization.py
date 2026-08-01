import pytest

from app.models.organization import Organizations, OrganizationUnits


@pytest.fixture
def organization(db_session):
    
    org = Organizations(
        name="Test org",
        address="Test address"
    )

    db_session.add(org)
    db_session.commit()

    db_session.refresh(org)

    return org


@pytest.fixture
def organization_unit(db_session, organization, region):

    org_unit = OrganizationUnits(
        org_id=organization.org_id,
        region_id=region.region_id,
        name="Test APAC",
        address="Test APAC unit address"
    )

    db_session.add(org_unit)
    db_session.commit()

    db_session.refresh(org_unit)

    return org_unit