from fastapi import APIRouter, Depends, status

from app.api.deps import get_current_user
from app.provider.services import get_organization_service
from app.schemas.auth import CurrentUser
from app.services.organization_service import OrganizationService
from app.schemas.organizations import OrganizationResponse



organizations_router = APIRouter(prefix="/organizations", tags=["Organizations"])


@organizations_router.get(
        "/{organization_id}",
         response_model=OrganizationResponse,
         status_code=status.HTTP_200_OK
        )
async def get_organization(
    organization_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    organization_service: OrganizationService = Depends(get_organization_service)
    ):
    return organization_service.get_organization(organization_id)