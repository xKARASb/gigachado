from pydantic import BaseModel, Field

class DepCreateForm(BaseModel):
    title: str = Field()