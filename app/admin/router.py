from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..db.repos import DepsRepository, EmployeeRepository
from ..db.schemas.employee import EmployeeInput
from ..auth import user_password_hash

from .schemas import DepCreateForm, EmployeeRegistrationForm, EmployeeRegistrationResponse

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

@admin_router.post("/new/dep")
async def new_dep(
    data: DepCreateForm,
    session: Session = Depends(get_db)
):
    dep = DepsRepository(session).create(
        data
    )
    return dep

@admin_router.post("/new/user", response_model=EmployeeRegistrationResponse)
async def new_user(
    data: EmployeeRegistrationForm, 
    session: Session = Depends(get_db)
):
    new_user = EmployeeInput(
        **data.model_dump()
    )
    user = EmployeeRepository(session).create(await user_password_hash(new_user))
    return EmployeeRegistrationResponse(
        id=user.id,
        name=user.name,
        last_name=user.last_name
    )