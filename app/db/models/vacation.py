from .. import Base
from sqlalchemy import Column, Uuid, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import List
from uuid import uuid4

class Vacation(Base):
    __tablename__ = "vacation"

    id = Column(Uuid, primary_key=True, default=uuid4)
    deps_id = mapped_column(ForeignKey("deps.id"))
    vacation_requests: Mapped[List["VacationRequest"]] = relationship(
        uselist=True
    )