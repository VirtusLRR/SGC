from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    item_id: int
    order_type: str
    description: str
    create_at: Optional[datetime] = datetime.now()
    amount: float
    price: Optional[float] = 0.0

class TransactionRequest(TransactionBase):
    ...

class TransactionResponse(TransactionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
