from sqlalchemy.orm import Session
from sqlalchemy import select

from app.schemas.workflows import WorkflowFetch
from app.models.workflow import Workflow, WorkflowRegion
from app.models.region import Regions
from app.utils.pagination import SortField, SortOrder


class WorkflowRepository:
    """Workflow repository logic"""

    def __init__(self, session: Session):
        self.session = session

    def create_new_workflow(self, workflow: Workflow):
        # Create a new workflow
        self.session.add(workflow)
        self.session.flush()
        return workflow

    def get_workflow_by_id(self, workflow_id: int):
        # Retrieve a workflow by its ID
        stmt = select(Workflow).where(Workflow.id == workflow_id, Workflow.is_deleted==False)
        result = self.session.execute(stmt).scalar_one_or_none()
        return result

    def list_all_workflows(self):
        "Fetch all the workflows"
        stmt = select(Workflow).where(Workflow.is_deleted==False)
        result = self.session.execute(stmt).scalars().all()
        return result

    def update(self):
        pass

    def get_workflow_by_name_and_org_unit(self, name: str, org_unit_id: int):
        "Retrieve the workflow by name and org_unit_id"
        stmt = (
            select(Workflow)
            .where(
                Workflow.name == name,
                Workflow.org_unit_id == org_unit_id, 
                Workflow.is_deleted == False
            )
        )
        result = self.session.execute(stmt).scalar_one_or_none()
        return result

    def fetch_workflow_by_search_criteria(self, workflow: WorkflowFetch):
        # Fetch workflow by search criteria
        query = select(Workflow).distinct().where(Workflow.org_id == workflow.org_id)

        if workflow.org_unit_id:
            query = query.where(Workflow.org_unit_id == workflow.org_unit_id)

        if workflow.name:
            query = query.where(Workflow.name.ilike(f"%{workflow.name}%"))

        if workflow.created_by:
            query = query.where(Workflow.created_by == workflow.created_by)

        query = query.where(Workflow.is_deleted.is_(False))

        if workflow.region:
            query = (
                query
                .join(WorkflowRegion, Workflow.id == WorkflowRegion.workflow_id)
                .join(Regions, WorkflowRegion.region_id == Regions.region_id)
                .where(Regions.code.in_(workflow.region))
            )

        if workflow.order_by:
            for item in workflow.order_by:
                if item.field == SortField.NAME:
                    column = Workflow.name
                elif item.field == SortField.CREATED_ON:
                    column = Workflow.created_on

                if item.order == SortOrder.ASC:
                    query = query.order_by(column.asc())
                else:
                    query = query.order_by(column.desc())
        else:
            # Default created_on ordering
            query = query.order_by(Workflow.created_on.desc())

        # Pagination
        query = query.offset(workflow.offset).limit(workflow.limit)

        return self.session.execute(query).scalars().all()

    def delete_workflow(self, workflow_id: int):
        pass


class WorkflowRegionRepository:
    """Workflow Region Mapping"""

    def __init__(self, session: Session):
        self.session = session

    def create_workflow_region_mapping(self, workflow: Workflow, regions: list[Regions]):
        
        for region in regions:
            workflow_region = WorkflowRegion(workflow_id = workflow.id, region_id=region.region_id)
            self.session.add(workflow_region)
        
        self.session.flush()