from app.db.base import Base
from datetime import datetime
from uuid import UUID
from typing import Optional
from sqlalchemy import String, ForeignKey, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.org_id"))
    org_unit_id: Mapped[int] = mapped_column(ForeignKey("organization_units.org_unit_id"))
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(server_default=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"))
    created_on: Mapped[datetime] = mapped_column(server_default=func.now())
    is_deleted: Mapped[bool] = mapped_column(server_default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime)
    deleted_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.user_id"))