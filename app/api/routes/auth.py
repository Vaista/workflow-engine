from fastapi import APIRouter, Depends
from typing import Annotated

from app.api.deps import get_current_user, get_db
from app.schemas.auth import CurrentUser


router = APIRouter()


@router.get("/me")
async def me(
    user: Annotated[CurrentUser, Depends(get_current_user)],
    db: Annotated[dict, Depends(get_db)],
):
    return {
        "user": user,
        "organization": user.org_id,
        "db": db,
    }