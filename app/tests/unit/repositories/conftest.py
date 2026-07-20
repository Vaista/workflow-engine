from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pytest

from app.db.base import Base
from app.models.organization import Organizations, OrganizationUnits
from app.models.region import Regions
from app.models.user import Users
from app.models.workflow import Workflow
from app.tests.config import TEST_DATABASE_URL


engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


@pytest.fixture
def db_session():

    with engine.connect() as conn:
        conn.execute(text('CREATE EXTENSION IF NOT EXISTS "pgcrypto"'))
        conn.commit()
    
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    yield session

    session.close()

    Base.metadata.drop_all(bind=engine)


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
def region(db_session):

    new_region = Regions(
        name="Asia Pacific",
        code="APAC"
    )

    db_session.add(new_region)
    db_session.commit()

    db_session.refresh(new_region)

    return new_region


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


@pytest.fixture
def workflow(db_session, user):
    
    new_workflow = Workflow(
        org_id = user.org_id,
        org_unit_id = user.org_unit_id,
        name = "Test Workflow",
        description = "Test Workflow Description",
        created_by = user.user_id,
        is_deleted=True
    )

    db_session.add(new_workflow)
    db_session.commit()

    db_session.refresh(new_workflow)

    return new_workflow


