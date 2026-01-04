from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from controllers import TransactionController
from schemas import TransactionResponse, TransactionRequest
from database.database import get_db
from datetime import datetime, timedelta

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

@transaction_routes.get("/transactions/summary/{days}")
def get_transaction_summary(days: int = 10, db: Session = Depends(get_db)):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return TransactionController.get_transaction_summary_by_period(start_date=start_date, end_date=end_date, db=db)

@transaction_routes.get("/transactions/most-transacted/{limit}/{order_type}")
def get_most_transacted_items(
        order_type: str | None = None,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return TransactionController.get_most_transacted_items(order_type=order_type, limit=limit, db=db)

@transaction_routes.get("/transactions/daily/{days}")
def get_daily_transactions(days: int = 30, db: Session = Depends(get_db)):
    return TransactionController.get_daily_transactions(days=days, db=db)

@transaction_routes.get("/transactions/consumption-rate/{days}")
def get_consumption_rate(days: int = 30, db: Session = Depends(get_db)):
    return TransactionController.get_consumption_rate_by_item(db=db, days=days)

@transaction_routes.get("/transactions/price-analysis")
def get_price_analysis(db: Session = Depends(get_db)):
    return TransactionController.get_average_transaction_value_by_item(db=db)