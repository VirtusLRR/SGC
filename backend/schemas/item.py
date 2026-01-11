from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, ClassVar
from datetime import datetime

class ItemBase(BaseModel):
    name: str
    measure_unity: str
    amount: float
    description: Optional[str] = None
    price: Optional[float] = 0
    price_unit: Optional[str] = 'unidade'
    expiration_date: Optional[datetime] = None
    create_at: Optional[datetime] = Field(default_factory=datetime.now) 
    update_at: Optional[datetime] = None

class ItemRequest(ItemBase):
    ...

class ItemResponse(ItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

