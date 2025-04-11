from sqlalchemy.orm import Session
from ..models import Employee
from ..schemas.employee import EmployeeInput, EmployeeOutput
from typing import List, Optional, Type


class EmployeeRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: EmployeeInput) -> EmployeeOutput:
        employee = Employee(**data.model_dump(exclude_none=True))
        print(employee)
        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)
        return EmployeeOutput(
            **employee.__dict__
        )

    def get_all(self) -> List[Optional[EmployeeOutput]]:
        Employees = self.session.query(Employee).all()
        return [EmployeeOutput(**Employee.__dict__) for Employee in Employees]

    def get_by_fullname(self, first_name: str, last_name: str, patronymic: str) -> EmployeeOutput:
        Employees = self.session.query(Employee).filter_by(name=first_name, last_name=last_name, patronymic=patronymic).all()
        return [EmployeeOutput(**Employee.__dict__) for Employee in Employees]
        
    def get_employee(self, _id: int) -> EmployeeOutput:
        employee = self.session.query(Employee).filter_by(id=_id).first()
        return EmployeeOutput(**employee.__dict__)

    def get_by_id(self, _id: int) -> Type[Employee]:
        return self.session.query(Employee).filter_by(id=_id).first()

    def Employee_exists_by_id(self, _id: int) -> bool:
        employee = self.session.query(Employee).filter_by(id=_id).first()
        return employee is not None

    def update_refresh_token(self, _id: int, token: str) -> EmployeeOutput:
        employee = self.session.query(Employee).filter_by(id=_id).first()
        employee.refresh_token = token
        self.session.commit()
        self.session.refresh(employee)
        return EmployeeInput(**employee.__dict__)

    def delete(self, Employee: Type[Employee]) -> bool:
        self.session.delete(Employee)
        self.session.commit()
        return True