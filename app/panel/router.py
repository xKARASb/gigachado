from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from typing import Annotated

from pydantic import UUID4
from ..db import get_db
from ..db.repos import DepsRepository, EmployeeRepository, VacationRequestRepository
from ..db.schemas.employee import EmployeeOutput
from ..db.schemas.vacation import VacationRequestInput, VacationRequestOutput
from ..auth.auth import user_password_hash, get_current_active_user

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
    # if user.role > 1:
    # raise HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="No permission"
    # )

@panel_router.post("/vacation/add")
async def vacation_add(
    data: VacationRequestInput,
    # user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session=Depends(get_db)
):
    user = EmployeeRepository(session).get_by_id(data.employee_id)
    
    return VacationRequestRepository(session).create(data)


@panel_router.get("/vacation/all")
async def vacation_all(
    # user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session=Depends(get_db)
):
    return VacationRequestRepository(session).get_all()

@panel_router.get("/vacation/user/{id}")
async def vacation_user(
    id: UUID4,
    # user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session=Depends(get_db)
):
    return VacationRequestRepository(session).get_vacation_by_user(id)

@panel_router.get("/vacation/dept/{id}")
async def vacation_dept(
    id: UUID4,
    # user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session=Depends(get_db)
):
    return VacationRequestRepository(session).get_vacation_by_dep(id)

@panel_router.get("/vacation/id/{id}")
async def vacation_id(
    id: UUID4,
    # user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session=Depends(get_db)
):
    return VacationRequestRepository(session).get_by_id(id)

