from langchain.tools import tool
from sqlalchemy import func
from database.database import SessionLocal
from models.recipe import Recipe
from models.recipe_item import RecipeItem
from models.item import Item


@tool
def check_recipe_availability(recipe_name: str) -> str:
    """
    Verifica se uma receita pode ser feita com os ingredientes disponíveis no estoque.
    Retorna quais ingredientes faltam e sugere receitas alternativas se houver falta.

    Use esta ferramenta SEMPRE que o usuário perguntar:
    - "Consigo fazer X?"
    - "Posso fazer Y?"
    - "Dá pra fazer Z?"
    - "Tem como fazer W?"

    Args:
        recipe_name: Nome da receita que o usuário quer fazer

    Returns:
        String com status de disponibilidade, lista de ingredientes faltantes e sugestões de receitas alternativas
    """
    db = SessionLocal()

    try:
        recipe = db.query(Recipe).filter(
            func.lower(Recipe.title).like(f'%{recipe_name.lower()}%')
        ).first()

        if not recipe:
            return f"Receita '{recipe_name}' não encontrada no banco de dados."

        recipe_items = db.query(
            Item.name,
            RecipeItem.amount.label('necessario'),
            Item.amount.label('estoque'),
            Item.measure_unity
        ).join(
            RecipeItem, RecipeItem.item_id == Item.id
        ).filter(
            RecipeItem.recipe_id == recipe.id
        ).all()

        if not recipe_items:
            return f"Receita '{recipe.title}' não tem ingredientes cadastrados."

        faltando = []
        disponiveis = []

        for item in recipe_items:
            if item.estoque < item.necessario:
                faltando.append({
                    'nome': item.name,
                    'necessario': item.necessario,
                    'disponivel': item.estoque,
                    'unidade': item.measure_unity
                })
            else:
                disponiveis.append({
                    'nome': item.name,
                    'quantidade': item.necessario,
                    'unidade': item.measure_unity
                })

        if not faltando:
            ingredientes_texto = ", ".join([
                f"{d['quantidade']}{d['unidade']} de {d['nome']}"
                for d in disponiveis
            ])
            return (
                f"SIM! Você pode fazer '{recipe.title}'!\n\n"
                f"Ingredientes disponíveis:\n{ingredientes_texto}"
            )

        receitas_alternativas = db.query(Recipe).filter(
            Recipe.id != recipe.id
        ).all()

        alternativas_disponiveis = []

        for alt_recipe in receitas_alternativas:
            alt_items = db.query(
                Item.amount,
                RecipeItem.amount
            ).join(
                RecipeItem, RecipeItem.item_id == Item.id
            ).filter(
                RecipeItem.recipe_id == alt_recipe.id
            ).all()

            if all(item[0] >= item[1] for item in alt_items):
                alternativas_disponiveis.append({
                    'titulo': alt_recipe.title,
                    'descricao': alt_recipe.description or ''
                })

                if len(alternativas_disponiveis) >= 3:
                    break

        faltando_texto = "\n".join([
            f"  - {f['nome']}: necessário {f['necessario']}{f['unidade']}, disponível {f['disponivel']}{f['unidade']}"
            for f in faltando
        ])

        resposta = (
            f"Infelizmente NÃO é possível fazer '{recipe.title}' no momento.\n\n"
            f"Faltam os seguintes ingredientes:\n{faltando_texto}\n"
        )

        if alternativas_disponiveis:
            resposta += "\nMas posso sugerir estas receitas alternativas que você PODE fazer com os ingredientes disponíveis:\n\n"
            for idx, alt in enumerate(alternativas_disponiveis, 1):
                resposta += f"{idx}. {alt['titulo']}"
                if alt['descricao']:
                    resposta += f" - {alt['descricao']}"
                resposta += "\n"
            resposta += "\nGostaria de saber mais sobre alguma dessas receitas?"
        else:
            resposta += "\nInfelizmente não há receitas alternativas disponíveis no momento com os ingredientes do estoque."

        return resposta

    except Exception as e:
        return f"Erro ao verificar disponibilidade: {str(e)}"

    finally:
        db.close()


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


