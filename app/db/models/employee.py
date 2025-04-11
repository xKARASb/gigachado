from .. import Base
from sqlalchemy import Column, String, Integer, Uuid, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Uuid, primary_key=True)
    password = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)
    
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String)
    
    email = Column(String)
    tg = Column(String, unique=True)
    
    is_admin = Column(Boolean, default=False)
    vacation_days = Column(Integer, default=28)
    additional_days = Column(Integer, default=0)

    dept_id = mapped_column(ForeignKey("deps.id"), nullable=False)
    post = Column(String, nullable=False)
