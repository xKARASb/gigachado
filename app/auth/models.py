from pydantic import BaseModel


class TokenData(BaseModel):
    id: str
    
    
class User(BaseModel):
    full_name: str | None = None
    