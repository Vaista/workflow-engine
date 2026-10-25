from sqlalchemy.orm import Session
from fastapi import Depends

from app.repositories.workflow_repository import WorkflowRepository, WorkflowRegionRepository
from app.repositories.workflow_step_repository import WorkflowStepRepository
from app.repositories.region_repository import RegionRepository
from app.services.workflow_service import WorkflowService
from app.services.workflow_step_service import WorkflowStepService
from app.services.region_service import RegionService
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


def get_workflow_step_service(
    session: Session = Depends(get_db),
) -> WorkflowStepService:
    workflow_repository = WorkflowRepository(session)
    workflow_step_repository = WorkflowStepRepository(session)

    return WorkflowStepService(
        workflow_repository=workflow_repository,
        workflow_step_repository=workflow_step_repository,
        session=session
    )


def get_region_service(
    session: Session = Depends(get_db),
) -> RegionService:
    region_repository = RegionRepository(session)
    return RegionService(
        region_repository=region_repository,
        session=session
    )
