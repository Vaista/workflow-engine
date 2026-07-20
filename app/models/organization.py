from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, ForeignKey, UniqueConstraint


class Organizations(Base):
    __tablename__ = "organizations"

    org_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(40), nullable=False, unique=True)
    address: Mapped[str | None] = mapped_column(VARCHAR(60), nullable=True)


class OrganizationUnits(Base):
    __tablename__ = "organization_units"

    org_unit_id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.org_id"))
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.region_id"))
    name: Mapped[str] = mapped_column(VARCHAR(40), nullable=False)
    address: Mapped[str] = mapped_column(VARCHAR(120), nullable=True)


    __table_args__ = (
        UniqueConstraint(
            "org_id",
            "name",
            name="uq_org_unit_org_id_name",
        ),
    )