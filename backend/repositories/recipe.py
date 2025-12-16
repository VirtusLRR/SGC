from sqlalchemy.orm import Session

from models import Recipe

class RecipeRepository:
    @staticmethod
    def find_all(db: Session) -> list[Recipe]:
        return db.query(Recipe).all()

    @staticmethod
    def save(db: Session, recipe: Recipe) -> Recipe:
        if recipe.id:
            db.merge(recipe)
        else:
            db.add(recipe)
        db.commit()
        return recipe

    @staticmethod
    def find_by_id(db: Session, id: int) -> Recipe:
        return db.query(Recipe).filter(Recipe.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Recipe).filter(Recipe.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        recipe = db.query(Recipe).filter(Recipe.id == id).first()
        if recipe is not None:
            db.delete(recipe)
            db.commit()
    
    @staticmethod
    def find_by_name(db: Session, name: int) -> Recipe:
        return db.query(Recipe).filter(Recipe.name == name).first()

    @staticmethod
    def exist_by_name(db: Session, name: int) -> bool:
        exist = db.query(Recipe).filter(Recipe.name == name).first()
        if exist is not None:
            return False
        else:
            return True

        