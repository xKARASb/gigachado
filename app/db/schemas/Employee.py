from pydantic import BaseModel, Field
    
        
class EmployeeInput(BaseModel):
    name: str = Field()
    last_name: str = Field()
    patronymic: str = Field()
    
    password: str = Field()
    
    email: str | None = Field()
    tg: str | None = Field()
    
    vacation_days: int = Field(default=28)
    additional_days: int = Field(default=0)


class EmployeeOutput(BaseModel):
    id: int
    name: str
    last_name: str
    patronymic: str
    
    password: str
    refresh_token: str | None = None
    
    email: str | None
    tg: str | None
    
    vacation_days: int
    additional_days: int