from .. import Base
from sqlalchemy import Column, String, Uuid

class Deps(Base):
    __tablename__ = "deps"

    id = Column(Uuid, primary_key=True)
    title = Column(String, unique=True)
