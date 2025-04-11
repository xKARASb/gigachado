from pydantic import BaseModel


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
