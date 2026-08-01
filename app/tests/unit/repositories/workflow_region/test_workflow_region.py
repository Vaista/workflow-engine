from app.repositories.workflow_repository import WorkflowRegionRepository
from app.models.workflow import WorkflowRegion
from app.models.region import Regions

from sqlalchemy import select


def test_create_workflow_region_mapping_return_workflow_list(db_session, workflow_factory):

    workflow = workflow_factory()

    # Arrange
    region_list = [('Region 1', 'R1'), ('Region 2', 'R2'), ('Region 3', 'R3')]
    created_region_list = []

    for reg in region_list:

        created_region = Regions(name=reg[0], code=reg[1])

        db_session.add(created_region)
        db_session.commit()
        db_session.refresh(created_region)

        created_region_list.append(created_region)
    

    # Act
    repo = WorkflowRegionRepository(db_session)
    repo.create_workflow_region_mapping(workflow, created_region_list)

    stmt = (
            select(WorkflowRegion)
            .where(
                WorkflowRegion.workflow_id == workflow.id
            )
    )
    mapped_regions = db_session.execute(stmt).scalars().all()

    # Assert
    assert len(mapped_regions) == 3