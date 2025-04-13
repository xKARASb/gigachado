from pydantic import BaseModel
from datetime import date
from typing import Set
from ..db.schemas.vacation import VacationRequestOutput as Vacation


class VacationConflictResponse(BaseModel):
    vacation1: Vacation 
    vacation2: Vacation
    overlap: Set[date]