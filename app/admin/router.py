from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..db.repos import DepsRepository

from .schemas import DepCreateForm


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