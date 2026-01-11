from pydantic import BaseModel, ConfigDict
from typing import Optional
from schemas.recipe_item import RecipeItemRequest, RecipeItemResponse

class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    steps: str
    recipe_itens: Optional[list[RecipeItemRequest]] = []

class RecipeRequest(RecipeBase):
    ...

class RecipeResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    steps: str
    recipe_itens: Optional[list[RecipeItemResponse]] = []

    model_config = ConfigDict(from_attributes=True)
