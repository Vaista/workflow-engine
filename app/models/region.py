from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR


class Regions(Base):
    __tablename__ = "regions"

    region_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(60), nullable=False, unique=True)
    code: Mapped[str] = mapped_column(VARCHAR(10), nullable=False, unique=True)