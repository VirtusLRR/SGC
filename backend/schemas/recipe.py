from pydantic import BaseModel
from typing import Optional

class RecipeBase(BaseModel):
    title: str
    steps: str
    description: Optional[str] = None

class RecipeRequest(RecipeBase):
    ...

class RecipeResponse(RecipeBase):
    id: int

    class Config:
        orm_mode = True
