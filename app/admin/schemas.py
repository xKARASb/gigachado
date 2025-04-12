from pydantic import BaseModel, Field, UUID4

class DepCreateForm(BaseModel):
    title: str = Field()
    
class EmployeeRegistrationForm(BaseModel):
    name: str = Field()
    last_name: str = Field()
    patronymic: str = Field()
    
    password: str = Field()
    
    email: str | None = Field()
    tg: str | None = Field()
    
    vacation_days: int = Field(default=28)
    additional_days: int = Field(default=0)

    deps_id: UUID4 = Field()
    post: str = Field()
    
    
class EmployeeRegistrationResponse(BaseModel):
    id: UUID4
    name: str
    last_name: str