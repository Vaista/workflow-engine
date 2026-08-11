from app.db.base import Base
from datetime import datetime
from uuid import UUID
from typing import Optional
from sqlalchemy import String, Integer, JSON, ForeignKey, func, DateTime, sql, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.org_id"))
    org_unit_id: Mapped[int] = mapped_column(ForeignKey("organization_units.org_unit_id"))
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(server_default=sql.expression.false())
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"))
    created_on: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.user_id"))
    updated_on: Mapped[datetime | None] = mapped_column(DateTime, onupdate=func.now())
    is_deleted: Mapped[bool] = mapped_column(server_default=sql.expression.false())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime)
    deleted_by: Mapped[UUID | None] = mapped_column(ForeignKey("users.user_id"))


class WorkflowRegion(Base):
    __tablename__ = "workflow_regions"

    id: Mapped[int] = mapped_column(primary_key=True)
    workflow_id: Mapped[int] = mapped_column(ForeignKey("workflows.id"))
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.region_id"))

    __table_args__ = (
            UniqueConstraint(
                "workflow_id",
                "region_id",
                name="uq_workflow_region_ids",
            ),
        )


class WorkflowStep(Base):
    __tablename__ = "workflow_steps"

    id: Mapped[int] = mapped_column(primary_key=True)
    workflow_id: Mapped[int] = mapped_column(ForeignKey("workflows.id"))
    step_number: Mapped[int] = mapped_column(Integer, nullable=False)
    step_name: Mapped[str] = mapped_column(String(30), nullable=False)
    step_description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    step_config: Mapped[dict] = mapped_column(JSON)

    __table_args__ = (
        UniqueConstraint(
            "workflow_id",
            "step_number",
            name="uq_workflow_step_number",
        ),
    )