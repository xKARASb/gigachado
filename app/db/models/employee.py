from .. import Base
from sqlalchemy import Column, String, Integer, Uuid, ForeignKey
from sqlalchemy.orm import mapped_column
from uuid import uuid4


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Uuid, primary_key=True, default=uuid4)
    password = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)
    
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String)
    tabel_number = Column(Integer, nullable=False)
    
    email = Column(String)
    tg = Column(String)
    
    role = Column(Integer, default=0)
    vacation_days = Column(Integer, default=28)
    additional_days = Column(Integer, default=0)

    deps_id = mapped_column(ForeignKey("deps.id"), nullable=False)
    post = Column(String, nullable=False)
