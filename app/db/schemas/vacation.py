from pydantic import BaseModel, Field, UUID4
import datetime as dt

class VacationRequestInput(BaseModel):
    start_at: dt.date = Field()
    end_at: dt.date = Field()

    is_approved: bool = Field(default=False)
    manager_comment: str = Field(default="")
    
    employee_id: UUID4 = Field()
    dep_id: UUID4 = Field()


class VacationRequestOutput(BaseModel):
    id: UUID4
    start_at: dt.date
    end_at: dt.date

    is_approved: bool
    manager_comment: str
    
    employee_id: UUID4
    dep_id: UUID4