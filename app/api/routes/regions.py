from fastapi import APIRouter, Depends, status

from app.api.deps import get_current_user
from app.schemas.auth import CurrentUser
from app.schemas.region import RegionResponse
from app.services.region_service import RegionService
from app.provider.services import get_region_service


regions_router = APIRouter(prefix="/regions", tags=["Regions"])


@regions_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[RegionResponse]
)
async def get_regions(
    current_user: CurrentUser = Depends(get_current_user),
    region_service: RegionService = Depends(get_region_service)
):
    """
    Get all regions.
    """
    return region_service.get_all_regions(current_user)
