from typing import List, Dict, Any
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
        """Cria uma nova receita."""
        recipe = RecipeRepository.save(db, Recipe(**request.model_dump()))
        return RecipeResponse.model_validate(recipe)

    @staticmethod
    def find_all(db: Session = Depends(get_db)):
        """Retorna todas as receitas cadastradas."""
        recipes = RecipeRepository.find_all(db)
        return [RecipeResponse.model_validate(recipe) for recipe in recipes]

    @staticmethod
    def find_by_id(id: int, db: Session = Depends(get_db)):
        """Retorna uma receita pelo seu ID."""
        recipe = RecipeRepository.find_by_id(db, id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Receita não encontrada"
            )
        return RecipeResponse.model_validate(recipe)

    @staticmethod
    def find_by_name(name: str, db: Session = Depends(get_db)):
        """Retorna receitas que correspondem ao nome fornecido."""
        recipes = RecipeRepository.find_by_name(db, name)
        return [RecipeResponse.model_validate(recipe) for recipe in recipes]

    @staticmethod
    def delete_by_id(id: int, db: Session = Depends(get_db)):
        """Remove uma receita pelo seu ID após verificar sua existência."""
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
        """Atualiza uma receita existente."""
        if not RecipeRepository.exists_by_id(db, id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receita não encontrada")
        recipe = RecipeRepository.save(db, Recipe(id=id, **request.model_dump()))
        return RecipeResponse.model_validate(recipe)
    
    @staticmethod
    def get_recipe_cost(recipe_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
        """
        Retorna o custo detalhado.
        Como não usamos Schema, o retorno é um dicionário livre.
        """
        try:
            result = RecipeRepository.find_recipe_cost(db, recipe_id)
            
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f"Receita com id {recipe_id} não encontrada."
                )
            
            return result
            
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=str(e)
            )

    @staticmethod
    def get_all_recipes_with_cost(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
        """Retorna todas as receitas com seus custos detalhados."""
        try:
            return RecipeRepository.find_all_recipes_with_cost(db)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=str(e)
            )

    @staticmethod
    def get_feasible_recipes(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
        """Retorna todas as receitas que podem ser preparadas com os ingredientes disponíveis."""
        try:
            return RecipeRepository.find_feasible_recipes(db)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=str(e)
            )

    @staticmethod
    def get_most_used_ingredients(limit: int = 10, db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
        """Retorna os ingredientes mais utilizados nas receitas."""
        try:
            return RecipeRepository.find_most_used_ingredients(db, limit)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=str(e)
            )
