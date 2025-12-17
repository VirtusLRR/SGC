from langchain.tools import tool
from sqlalchemy import inspect, text
from database.database import engine, SessionLocal
from models.recipe import Recipe
from models.recipe_item import RecipeItem
from models.item import Item

@tool
def add_recipe_tool(nome: str, ingredientes: str, preparo: str, descricao: str = ""):
    """
    Adiciona uma nova receita ao banco de dados com seus ingredientes.
    Use esta ferramenta quando o usuário pedir para salvar ou gravar uma receita.

    Args:
        nome: Título da receita
        ingredientes: String com ingredientes no formato "quantidade nome (unidade), quantidade nome (unidade), ..."
                     Ex: "2 bananas (unidade), 250 leite (ml), 1 açúcar (colher de sopa)"
        preparo: Passos para fazer a receita
        descricao: Descrição da receita (opcional)
    """
    db = SessionLocal()

    try:
        new_recipe = Recipe(
            title=nome,
            steps=preparo,
            description=descricao
        )

        db.add(new_recipe)
        db.flush()

        ingredients_list = [ing.strip() for ing in ingredientes.split(',')]

        for ingredient_str in ingredients_list:
            try:
                parts = ingredient_str.strip().split()
                if len(parts) < 2:
                    continue

                quantity_str = parts[0]
                remainder = ' '.join(parts[1:])

                if '(' in remainder:
                    item_name = remainder.split('(')[0].strip()
                    unity = remainder.split('(')[1].replace(')', '').strip()
                else:
                    item_name = remainder.strip()
                    unity = "unidade"

                quantity = float(quantity_str)

                item = db.query(Item).filter(Item.name == item_name).first()

                if not item:
                    item = Item(
                        name=item_name,
                        measure_unity=unity,
                        amount=0,
                        description=f"Ingrediente da receita {nome}"
                    )
                    db.add(item)
                    db.flush()

                recipe_item = RecipeItem(
                    recipe_id=new_recipe.id,
                    item_id=item.id,
                    amount=quantity
                )
                db.add(recipe_item)

            except Exception as e:
                continue

        db.commit()
        return f"Sucesso! A receita '{nome}' foi salva no banco de dados com seus ingredientes."

    except Exception as e:
        db.rollback()
        return f"Erro ao salvar receita: {str(e)}"

    finally:
        db.close()


