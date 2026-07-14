from sqlalchemy.orm import Session
from fastapi import Depends

from app.repositories.workflow_repository import WorkflowRepository, WorkflowRegionRepository
from app.repositories.region_repository import RegionRepository
from app.services.workflow_service import WorkflowService
from app.api.deps import get_db


def get_workflow_service(
    session: Session = Depends(get_db),
) -> WorkflowService:
    workflow_repository = WorkflowRepository(session)
    workflow_region_repository = WorkflowRegionRepository(session)
    region_repository = RegionRepository(session)

    return WorkflowService(
        workflow_repository=workflow_repository,
        workflow_region_repository=workflow_region_repository,
        region_repository=region_repository,
        session=session,
    )