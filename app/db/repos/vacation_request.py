from sqlalchemy.orm import Session
from ..models import VacationRequest
from ..schemas.vacation import VacationRequestInput, VacationRequestOutput
from typing import List, Optional, Type


class VacationRequestRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: VacationRequestInput) -> VacationRequestOutput:
        vac = VacationRequest(**data.model_dump(exclude_none=True))
        self.session.add(vac)
        self.session.commit()
        self.session.refresh(vac)

        return VacationRequestOutput(
            **vac.__dict__
        )
    
    def get_all(self) -> List[Optional[VacationRequestOutput]]:
        vacations = self.session.query(VacationRequest).all()
        return [VacationRequestOutput(**vacation.__dict__) for vacation in vacations]

    def get_vacation_by_user(self, id: str) -> List[VacationRequestOutput]:
        vacs = self.session.query(VacationRequest).filter_by(employee_id=id).all()
        return [VacationRequestOutput(**vac.__dict__) for vac in vacs]
    
    def get_vacation_by_dep(self, id: str) -> List[VacationRequestOutput]:
        vacs = self.session.query(VacationRequest).filter_by(dep_id=id).all()
        return [VacationRequestOutput(**vac.__dict__) for vac in vacs]

    def dep_is_approve(self, id: str) -> bool:
        vacs = self.session.query(VacationRequest).filter_by(dep_id=id).all()
        for vac in vacs:
            if not vac.is_approved:
                return False
        return True

    def get_by_id(self, id) -> VacationRequestOutput:
        vac = self.session.query(VacationRequest).filter_by(id=id).first()
        return VacationRequestOutput(**vac.__dict__)
    
    def confirm_employee_vacations(self, id):
        vacs = self.session.query(VacationRequest).filter_by(employee_id=id).all()
        
        for i in range(len(vacs)):
            vacs[i].is_approved = True
            self.session.add(vacs[i])
            
        self.session.commit()