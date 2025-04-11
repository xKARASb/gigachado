from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class AccesTokenRequest(BaseModel):
    access_token: str | None = None


class RefreshTokenRequestForm(BaseModel):
    refresh_token: str
    id: str
  

class AccessTokenRequestForm(BaseModel):
    firstname: str
    lastname: str
    patronymic: str
    password: str


class EmployeeRegistrationForm(BaseModel):
    name: str = Field()
    last_name: str = Field()
    patronymic: str = Field()
    
    password: str = Field()
    
    email: str | None = Field()
    tg: str | None = Field()
    
    vacation_days: int = Field(default=28)
    additional_days: int = Field(default=0)

    dep_id: int = Field()
    post: str = Field()
    
    
class EmployeeRegistrationResponse(BaseModel):
    id: int
    name: str
    last_name: str