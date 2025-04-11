from .. import Base
from sqlalchemy import Column, Uuid, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import List


class Vacation(Base):
    __tablename__ = "vacation"

    id = Column(Uuid, primary_key=True)
    deps_id = mapped_column(ForeignKey("deps.id"))
    vacation_request: Mapped[List["VacationRequest"]] = relationship(
        uselist=True
    )