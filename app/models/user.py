import uuid
from datetime import datetime

from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, ForeignKey, VARCHAR, Text, Boolean, func, text


class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.org_id"))
    org_unit_id: Mapped[int] = mapped_column(ForeignKey("organization_units.org_unit_id"))
    name: Mapped[str] = mapped_column(VARCHAR(60), nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    password_hash: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    contact: Mapped[str | None] = mapped_column(VARCHAR(20), nullable=True)
    country: Mapped[str | None] = mapped_column(VARCHAR(20), nullable=True)
    is_active: Mapped[Boolean] = mapped_column(Boolean, default=True)
    created_on: Mapped[datetime] = mapped_column(server_default=func.now()) 
    