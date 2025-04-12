from pydantic import BaseModel, Field, UUID4
    
        
class EmployeeInput(BaseModel):
    name: str = Field()
    last_name: str = Field()
    patronymic: str = Field()
    
    password: str = Field()
    
    email: str | None = Field()
    tg: str | None = Field()
    role: int = Field(default=0)
    
    vacation_days: int = Field(default=28)
    additional_days: int = Field(default=0)

    deps_id: UUID4 = Field()
    post: str = Field()


class EmployeeOutput(BaseModel):
    id: UUID4
    name: str
    last_name: str
    patronymic: str
    
    password: str
    refresh_token: str | None = None
    role: int
    
    email: str | None
    tg: str | None
    
    vacation_days: int
    additional_days: int
    
    deps_id: UUID4 = Field()
    post: str = Field()