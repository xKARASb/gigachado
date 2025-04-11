from .. import Base
from sqlalchemy import Column, Uuid, Boolean, ForeignKey, Date, Text, DateTime
from sqlalchemy.orm import mapped_column
from datetime import datetime as dt
from uuid import uuid4

class VacationRequest(Base):
    __tablename__ = "vacation_request"

    id = Column(Uuid, primary_key=True, default=uuid4)

    start_at = Column(Date, nullable=False)
    end_at = Column(Date, nullable=False)
    is_approved = Column(Boolean, default=0)
    manager_comment = Column(Text, nullable=True)
    employee_id = mapped_column(ForeignKey("employee.id"))
    dep_id = mapped_column(ForeignKey("deps.id"))
    vacation_id = mapped_column(ForeignKey("vacation.id"))

    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, default=dt.now, onupdate=dt.now)