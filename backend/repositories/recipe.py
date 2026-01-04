from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal

from models import Recipe, RecipeItem, Item
from utils.unit_converter import calculate_item_total_value, calculate_unit_price

class RecipeRepository:
    @staticmethod
    def find_all(db: Session) -> list[Recipe]:
        """Recupera todas as receitas do banco de dados."""
        return db.query(Recipe).all()

    @staticmethod
    def save(db: Session, recipe: Recipe) -> Recipe:
        """Salva ou atualiza uma receita no banco de dados."""
        if recipe.id:
            db.merge(recipe)
        else:
            db.add(recipe)
        db.commit()
        return recipe

    @staticmethod
    def find_by_id(db: Session, id: int) -> Recipe:
        """Recupera uma receita pelo seu ID."""
        return db.query(Recipe).filter(Recipe.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        """Verifica se uma receita existe pelo seu ID."""
        return db.query(Recipe).filter(Recipe.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        """Remove uma receita pelo seu ID."""
        recipe = db.query(Recipe).filter(Recipe.id == id).first()
        if recipe is not None:
            db.delete(recipe)
            db.commit()

    @staticmethod
    def find_by_name(db: Session, name: int) -> Recipe:
        """Recupera uma receita pelo seu nome."""
        return db.query(Recipe).filter(Recipe.name == name).first()

    @staticmethod
    def exist_by_name(db: Session, name: int) -> bool:
        """Verifica se uma receita existe pelo seu nome."""
        exist = db.query(Recipe).filter(Recipe.name == name).first()
        if exist is not None:
            return False
        else:
            return True

    @staticmethod
    def find_recipe_cost(db: Session, recipe_id: int) -> dict:
        """Calcula o custo total de uma receita baseado nos preços atuais com conversão de unidades"""
        recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not recipe:
            return None

        total_cost = Decimal('0')
        ingredients = []

        for recipe_item in recipe.recipe_itens:
            item = recipe_item.item

            unit_price = calculate_unit_price(
                item.price,
                item.price_unit,
                item.measure_unity
            )

            item_cost = recipe_item.amount * unit_price
            total_cost += item_cost

            ingredients.append({
                "item_id": item.id,
                "item_name": item.name,
                "required_amount": float(recipe_item.amount),
                "measure_unity": item.measure_unity,
                "unit_price": float(unit_price),
                "price_reference": f"{float(item.price)}/{item.price_unit}",
                "total_cost": float(item_cost)
            })

        return {
            "recipe_id": recipe.id,
            "recipe_title": recipe.title,
            "total_cost": float(total_cost),
            "ingredients": ingredients
        }

    @staticmethod
    def find_all_recipes_with_cost(db: Session) -> list[dict]:
        """Retorna todas as receitas com seus custos calculados"""
        recipes = db.query(Recipe).all()
        return [
            RecipeRepository.find_recipe_cost(db, recipe.id)
            for recipe in recipes
        ]

    @staticmethod
    def find_feasible_recipes(db: Session) -> list[dict]:
        """Retorna receitas que podem ser feitas com o estoque atual"""
        recipes = db.query(Recipe).all()
        feasible = []
        for recipe in recipes:
            can_make = True
            for recipe_item in recipe.recipe_itens:
                item = recipe_item.item
                if item.amount < recipe_item.amount:
                    can_make = False
            if can_make:
                recipe_cost = RecipeRepository.find_recipe_cost(db, recipe.id)
                feasible.append({
                    "recipe_id": recipe.id,
                    "recipe_title": recipe.title,
                    "total_cost": recipe_cost['total_cost']
                })
        return feasible

    @staticmethod
    def find_most_used_ingredients(db: Session, limit: int = 10) -> list[dict]:
        """Retorna os ingredientes mais utilizados em receitas"""
        results = db.query(
            Item.id,
            Item.name,
            func.count(RecipeItem.recipe_id).label('recipe_count'),
            func.sum(RecipeItem.amount).label('total_amount_used')
        ).join(
            RecipeItem, Item.id == RecipeItem.item_id
        ).group_by(
            Item.id, Item.name
        ).order_by(
            func.count(RecipeItem.recipe_id).desc()
        ).limit(limit).all()

        return [
            {
                "item_id": r.id,
                "item_name": r.name,
                "recipe_count": r.recipe_count,
                "total_amount_used": float(r.total_amount_used)
            }
            for r in results
        ]