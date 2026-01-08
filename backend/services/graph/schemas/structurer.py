from pydantic import BaseModel
from typing import List, Optional

class IngredientItem(BaseModel):
    name: str
    amount: float
    measure_unity: str

class StructurerOutputSchema(BaseModel):
    title: str
    description: str
    steps: str
    ingredients: List[IngredientItem]

class StructurerOutputSchemaList(BaseModel): # receita
    recipes: List[StructurerOutputSchema]


class ItemDataForWriter(BaseModel):
    name: str
    amount: float
    measure_unity: str
    price: float = 0.0
    price_unit: str = "unidade"
    description: str = ""
    expiration_date: Optional[str] = None


class TransactionDataForWriter(BaseModel):
    order_type: str
    description: str
    amount: float
    price: Optional[float] = None

class ItemStructuredOutput(BaseModel):
    item_data: ItemDataForWriter
    transaction_data: TransactionDataForWriter


class ItemStructuredOutputList(BaseModel):

    items: List[ItemStructuredOutput]    
    ingredients: List[IngredientItem]

