from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    name: str
    measure_unity: str
    amount: float
    description: Optional[str] = None
    price: Optional[float] = 0
    expiration_date: Optional[datetime] = None
    create_at: Optional[datetime] = datetime.now()
    update_at: Optional[datetime] = None

class ItemRequest(ItemBase):
    ...

class ItemResponse(ItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

