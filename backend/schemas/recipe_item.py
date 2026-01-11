from pydantic import BaseModel, ConfigDict

class RecipeItemRequest(BaseModel):
    """Schema para criação de itens de receita (sem recipe_id)."""
    item_id: int
    amount: float

class RecipeItemResponse(BaseModel):
    """Schema para resposta de itens de receita (com recipe_id)."""
    recipe_id: int
    item_id: int
    amount: float

    model_config = ConfigDict(from_attributes=True)