from .. import Base
from sqlalchemy import Column, String, Uuid
from uuid import uuid4



class Deps(Base):
    __tablename__ = "deps"

    id = Column(Uuid, primary_key=True, default=uuid4)
    title = Column(String, unique=True)
