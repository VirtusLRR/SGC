from pydantic import BaseModel, ConfigDict
from typing import Optional


class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    steps: str

class RecipeRequest(RecipeBase):
    ...

class RecipeResponse(RecipeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
