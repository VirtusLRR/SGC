from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from controllers import ItemController, TransactionController, RecipeController
from datetime import datetime, timedelta

dashboard_routes = APIRouter()

@dashboard_routes.get("/dashboard")
def get_dashboard_data(db: Session = Depends(get_db)):
    """Retorna dados consolidados para dashboard"""
    return {
        "inventory": ItemController.get_inventory_summary(db),
        "transactions_30d": TransactionController.get_transaction_summary_by_period(
            datetime.now() - timedelta(days=30),
            datetime.now(),
            db
        ),
        "low_stock_count": len(ItemController.get_low_stock_items(5, db)),
        "expiring_soon_count": len(ItemController.get_items_near_expiration(7, db)),
        "feasible_recipes_count": len(RecipeController.get_feasible_recipes(db))
    }