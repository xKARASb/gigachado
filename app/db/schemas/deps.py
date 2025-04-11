from pydantic import BaseModel, UUID4
        
class DepInput(BaseModel):
    title: str

class DepOutput(BaseModel):
    id: UUID4
    title: str