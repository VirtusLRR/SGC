from fastapi import Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.database import get_db
from models import Recipe
from repositories import RecipeRepository
from schemas import RecipeResponse, RecipeRequest

class RecipeController:
    @staticmethod
    def create(request: RecipeRequest, db: Session = Depends(get_db)):
        recipe = RecipeRepository.save(db, Recipe(**request.model_dump()))
        return RecipeResponse.model_validate(recipe)
        

    @staticmethod
    def find_all(db: Session = Depends(get_db)):
        recipes = RecipeRepository.find_all(db)
        return [RecipeResponse.model_validate(recipe) for recipe in recipes]

    @staticmethod
    def find_by_id(id: int, db: Session = Depends(get_db)):
        recipe = RecipeRepository.find_by_id(db, id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Receita não encontrada"
            )
        return RecipeResponse.model_validate(recipe)

    @staticmethod
    def find_by_name(name: str, db: Session = Depends(get_db)):
        recipes = RecipeRepository.find_by_name(db, name)
        return [RecipeResponse.model_validate(recipe) for recipe in recipes]

    @staticmethod
    def delete_by_id(id: int, db: Session = Depends(get_db)):
        if not RecipeRepository.exists_by_id(db, id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Receita não encontrada"
            )
        RecipeRepository.delete_by_id(db, id)
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT, 
            content={"message": "Receita removida com sucesso", "id": id}
        )

    @staticmethod
    def update(id: int, request: RecipeRequest, db: Session = Depends(get_db)):
        if not RecipeRepository.exists_by_id(db, id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receita não encontrada")
        recipe = RecipeRepository.save(db, Recipe(id=id, **request.model_dump()))
        return RecipeResponse.model_validate(recipe)
