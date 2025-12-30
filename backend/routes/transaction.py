from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from controllers import TransactionController
from schemas import TransactionResponse, TransactionRequest
from database.database import get_db

transaction_routes = APIRouter()

@transaction_routes.post("/api/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create(request: TransactionRequest, db: Session = Depends(get_db)):
    return TransactionController.create(request, db)

@transaction_routes.get("/api/transactions", response_model=list[TransactionResponse])
def find_all_or_by_item_id(item_id: int | None = None, db: Session = Depends(get_db)):
    if item_id:
        return TransactionController.find_by_item_id(item_id, db)
    return TransactionController.find_all(db)

@transaction_routes.get("/api/transactions/{id}", response_model=TransactionResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    return TransactionController.find_by_id(id, db)


@transaction_routes.delete("/api/transactions/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    return TransactionController.delete_by_id(id, db)

@transaction_routes.put("/api/transactions/{id}", response_model=TransactionResponse)
def update(id: int, request: TransactionRequest, db: Session = Depends(get_db)):
    return TransactionController.update(id, request, db)
