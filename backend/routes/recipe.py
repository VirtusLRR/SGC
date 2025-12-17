from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from controllers import RecipeController
from schemas import RecipeResponse, RecipeRequest
from database.database import get_db

recipe_routes = APIRouter()

@recipe_routes.post("/api/recipes", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create(request: RecipeRequest, db: Session = Depends(get_db)):
    return RecipeController.create(request, db)

@recipe_routes.get("/api/recipes", response_model=list[RecipeResponse])
def find_all_or_by_name(name: str | None = None, db: Session = Depends(get_db)):
    if name:
        return RecipeController.find_by_name(name, db)
    return RecipeController.find_all(db)

@recipe_routes.get("/api/recipes/{id}", response_model=RecipeResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    return RecipeController.find_by_id(id, db)

@recipe_routes.delete("/api/recipes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    return RecipeController.delete_by_id(id, db)

@recipe_routes.put("/api/recipes/{id}", response_model=RecipeResponse)
def update(id: int, request: RecipeRequest, db: Session = Depends(get_db)):
    return RecipeController.update(id, request, db)