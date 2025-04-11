from sqlalchemy.orm import Session
from ..models import Deps
from ..schemas.deps import DepInput, DepOutput
# from typing import List, Optional, Type


class DepsRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def create(self, data: DepInput) -> DepOutput:
        dep = Deps(**data.model_dump(exclude_none=True))
        print(dep)
        self.session.add(dep)
        self.session.commit()
        self.session.refresh(dep)
        return DepOutput(
            **dep.__dict__
        )