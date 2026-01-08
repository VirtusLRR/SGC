from models import Item, Recipe, RecipeItem, Bot, Transaction
from sqlalchemy.exc import OperationalError
from database.database import engine, Base
import time

def wait_for_db(max_retries=10, delay=3):
    print("Conectando ao banco de dados...")
    for i in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("Tabelas criadas/verificadas com sucesso!")
            return
        except OperationalError:
            print(f"⚠Banco ainda não está pronto... Tentativa {i+1}/{max_retries}")
            time.sleep(delay)
    raise Exception("Não foi possível conectar ao banco de dados.")

wait_for_db()

from routes import bot_routes, recipe_routes, item_routes, transaction_routes, dashboard_routes
from fastapi import FastAPI

app = FastAPI(
    title="SGC - Sistema de Gerenciamento de Compras",
    version="1.0.0"
)

app.include_router(item_routes, tags=["Item"])
app.include_router(recipe_routes, tags=["Recipe"])
app.include_router(bot_routes, tags=["Bot"])
app.include_router(transaction_routes, tags=["Transaction"])
app.include_router(dashboard_routes, tags=["Dashboard"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "index:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
