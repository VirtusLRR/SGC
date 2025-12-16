from fastapi import FastAPI
from routes import item_routes

app = FastAPI(
    title="Minha API",
    version="1.0.0"
)

app.include_router(item_routes, tags=["Item"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "index:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
