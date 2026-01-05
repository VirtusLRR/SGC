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
    """Dados do item para o ITEM_WRITER inserir no banco"""
    name: str
    amount: float
    measure_unity: str
    price: float = 0.0
    price_unit: str = "unidade"
    description: str = ""
    expiration_date: Optional[str] = None  # Formato: 'YYYY-MM-DD'


class TransactionDataForWriter(BaseModel):
    """Dados da transação para o TRANSACTION_WRITER registrar no histórico"""
    order_type: str  # 'compra', 'venda', 'uso', 'perda', 'ajuste'
    description: str
    amount: float  # Quantidade (positivo para entrada, negativo para saída)
    price: Optional[float] = None  # Preço da transação (opcional)


class ItemStructuredOutput(BaseModel):
    """Saída estruturada completa para um item (com dados para 2 agentes)"""
    item_data: ItemDataForWriter
    transaction_data: TransactionDataForWriter


class ItemStructuredOutputList(BaseModel): # item
    """Lista de itens estruturados"""
    items: List[ItemStructuredOutput]    
    ingredients: List[IngredientItem]

