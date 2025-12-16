from models.recipe import Recipe
from models.item import Item
from models.recipe_item import RecipeItem
from tests.conftest import db_session 

def test_insert_item(db_session):
    
    farinha = Item(
        name="Farinha",
        measure_unity="g",
        amount=1000,
        description="Farinha de trigo"
    )

    db_session.add(farinha)
    db_session.commit()

    assert farinha.id is not None
    
    filtered_item = db_session.query(Item).filter_by(name="Farinha").first()
    assert filtered_item.name == farinha.name

def test_insert_recipe(db_session):

    recipe = Recipe(
        title="Bolo simples",
        steps="Misture tudo e asse",
        description="Bolo básico"
    )

    db_session.add(recipe)
    db_session.commit()

    assert recipe.id is not None

    filtered_recipe = db_session.query(Recipe).filter_by(title="Bolo simples").first()
    assert filtered_recipe.title == recipe.title
    
def test_insert_recipe_item(db_session):

    farinha = Item(
        name="Farinha",
        measure_unity="g",
        amount=1000,
        description="Farinha de trigo"
    )

    recipe = Recipe(
        title="Bolo simples",
        steps="Misture tudo e asse",
        description="Bolo básico"
    )

    db_session.add(farinha)
    db_session.commit()

    recipe.recipe_itens.append(
        RecipeItem(item=farinha, amount=200)
    )

    db_session.add(recipe)
    db_session.commit()

    assert recipe.id is not None
    assert farinha.id is not None
    assert len(recipe.recipe_itens) == 1

    itens_name = [ri.item.name for ri in recipe.recipe_itens]
    assert "Farinha" in itens_name
    
    amount = {ri.item.name: ri.amount for ri in recipe.recipe_itens}
    assert amount["Farinha"] == 200

    filtered_recipe = db_session.query(Recipe).filter_by(title="Bolo simples").first()
    assert filtered_recipe.title == recipe.title