from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from typing import Annotated

from pydantic import UUID4
from uuid import uuid1
from ..db import get_db
from ..db.repos import DepsRepository, EmployeeRepository, VacationRequestRepository
from ..db.schemas.employee import EmployeeOutput
from ..db.schemas.vacation import VacationRequestInput, VacationRequestOutput
from ..auth.auth import user_password_hash, get_current_active_user
from .utils import get_overlaps, export_data_xl

# from .schemas import DepCreateForm, EmployeeRegistrationForm, EmployeeRegistrationResponse

panel_router = APIRouter(
    prefix="/panel",
    tags=["panel"],
    responses={404: {"description": "Not found"}},
)

@panel_router.get("/deps/all")
async def get_all_deps(
    # user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session = Depends(get_db)
    ):
    return DepsRepository(session).get_all()

@panel_router.get("/deps/{id}")
async def get_id_deps(
    id: UUID4,
    # user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session = Depends(get_db)
    ):
    return DepsRepository(session).get_by_id(id)


@panel_router.get("/employees/all")
async def get_all_employees(
    # user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session = Depends(get_db),
    ):
    return EmployeeRepository(session).get_all()

@panel_router.get("/employees/id/{id}")
async def get_id_employees(
    id: UUID4,
    # user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session = Depends(get_db)
    ):
    return EmployeeRepository(session).get_employee(id)

@panel_router.get("/employees/deps/{id}")
async def get_deps_employees(
    id: UUID4,
    # user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session = Depends(get_db)
    ):
    return EmployeeRepository(session).get_by_dep(id)

@panel_router.post("/vacation/add")
async def vacation_add(
    data: VacationRequestInput,
    user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session=Depends(get_db)
):
    employee = EmployeeRepository(session).get_by_id(data.employee_id)
    
    if user.role == 0 and user.id != data.employee_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No permission"
        ) 
    
    if user.role == 1 and user.deps_id != data.dep_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No permission"
        ) 
        
    
    if data.start_at > data.end_at:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="start date > end date"
        )

    duration = (data.end_at - data.start_at).days + 1
    
    vacations = VacationRequestRepository(session).get_vacation_by_user(data.employee_id)
    
    durations = [(x.end_at - x.start_at).days + 1 for x in vacations]
    durations.append(duration)
    # print(durations)
    if not any([x >= 14 for x in durations]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Хотя бы один отпуск должен быть больше 14 дней"
        )
    if sum(durations) > employee.vacation_days + employee.additional_days:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недостаточно дней отпуска"
        )
    return VacationRequestRepository(session).create(data)

@panel_router.get("/vacation/employee/{employee_id}/days")
async def vacation_days(
    employee_id,
    session: Session=Depends(get_db)
):
    employee = EmployeeRepository(session).get_by_id(employee_id)
    vacations = VacationRequestRepository(session).get_vacation_by_user(employee_id)
    durations = [(x.end_at - x.start_at).days + 1 for x in vacations]
    return {"vacation_days": employee.vacation_days, "additional_days": employee.additional_days, "duration": sum(durations)}
    

@panel_router.get("/vacation/dept/{dept_id}/conflicts")
async def vacation_conflict_dept(
    dept_id: UUID4,
    session: Session=Depends(get_db)
    ):
    vacations = VacationRequestRepository(session).get_vacation_by_dep(dept_id)
    return get_overlaps(vacations)

@panel_router.post("/vacation/employee/{employee_id}/confirm")
async def confirm_employee_vacation(
    employee_id: UUID4,
    session: Session = Depends(get_db)
):
    VacationRequestRepository(session).confirm_employee_vacations(employee_id)

@panel_router.get("/vacation/export/all")
async def export_vacation(
    session: Session = Depends(get_db)
):
    vacations = VacationRequestRepository(session).get_all()
    title = f"график_отпусков_{uuid1()}"
    
    e = export_data_xl(vacations, title, session)
    if e:
        return FileResponse(e, filename=f"{title}.xlsx")
    

@panel_router.get("/vacation/all")
async def vacation_all(
    # user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session=Depends(get_db)
):
    return VacationRequestRepository(session).get_all()

@panel_router.get("/vacation/employee/{employee_id}")
async def vacation_user(
    employee_id: UUID4,
    # user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session=Depends(get_db)
):
    return VacationRequestRepository(session).get_vacation_by_user(employee_id)

@panel_router.get("/vacation/dept/{dept_id}")
async def vacation_dept(
    dept_id: UUID4,
    # user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session=Depends(get_db)
):
    return VacationRequestRepository(session).get_vacation_by_dep(dept_id)

@panel_router.get("/vacation/id/{id}")
async def vacation_id(
    id: UUID4,
    # user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session=Depends(get_db)
):
    return VacationRequestRepository(session).get_by_id(id)

