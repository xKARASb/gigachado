from sqlalchemy.orm import Session
from ..models import Deps
from ..schemas.deps import DepInput, DepOutput


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
    
    def get_all(self) -> DepOutput:
        deps = self.session.query(Deps).all()
        return [DepOutput(**dep.__dict__) for dep in deps]

    def get_by_id(self, id) -> DepOutput | None:
        return self.session.query(Deps).filter_by(id=id).first()
        