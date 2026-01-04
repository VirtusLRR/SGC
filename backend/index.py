from models import Item, Recipe, RecipeItem, Bot, Transaction
from database.database import engine, Base
from routes import bot_routes, recipe_routes, item_routes, transaction_routes, dashboard_routes
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciador de ciclo de vida do aplicativo FastAPI."""
    try:
        print("Criando tabelas no banco de dados...")
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso no banco de dados.")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    yield

app = FastAPI(
    title="SGC - Sistema de Gerenciamento de Compras",
    version="1.0.0",
    lifespan=lifespan
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
