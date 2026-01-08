from langchain.tools import tool
from sqlalchemy import func
from database.database import SessionLocal, get_db
from models.recipe import Recipe
from models.recipe_item import RecipeItem
from models.item import Item
from models.transaction import Transaction
from schemas import RecipeRequest, ItemRequest, TransactionRequest
from datetime import datetime

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
def list_all_recipes_tool() -> str:
    """
    Lista todas as receitas cadastradas no banco de dados.
    
    Returns:
        String formatada com lista de receitas
    """
    from controllers import RecipeController

    db = SessionLocal()
    try:
        recipes = RecipeController.find_all(db=db)
        
        if not recipes:
            return "Nenhuma receita cadastrada no banco de dados."
        
        resultado = f"📚 Receitas cadastradas ({len(recipes)}):\n\n"
        for idx, recipe in enumerate(recipes, 1):
            resultado += f"{idx}. {recipe.title}"
            if recipe.description:
                resultado += f" - {recipe.description}"
            resultado += "\n"
        
        return resultado
    
    except Exception as e:
        return f"Erro ao listar receitas: {str(e)}"
    finally:
        db.close()


@tool
def find_recipe_by_name_tool(recipe_name: str) -> str:
    """
    Busca receitas por nome e retorna detalhes completos.
    
    Args:
        recipe_name: Nome ou parte do nome da receita
    
    Returns:
        String com detalhes da(s) receita(s) encontrada(s)
    """
    from controllers import RecipeController

    db = SessionLocal()
    try:
        recipes = RecipeController.find_by_name(recipe_name, db=db)
        
        if not recipes:
            return f"Nenhuma receita encontrada com o nome '{recipe_name}'."
        
        resultado = ""
        for recipe in recipes:
            resultado += f"📖 **{recipe.title}**\n\n"
            if recipe.description:
                resultado += f"Descrição: {recipe.description}\n\n"
            resultado += f"Modo de Preparo:\n{recipe.steps}\n\n"
            resultado += "---\n\n"
        
        return resultado.strip()
    
    except Exception as e:
        return f"Erro ao buscar receita: {str(e)}"
    finally:
        db.close()


@tool
def add_recipe_tool(nome: str, ingredientes: str, preparo: str, descricao: str = "") -> str:
    """
    Adiciona uma nova receita ao banco de dados com seus ingredientes.
    
    Args:
        nome: Título da receita
        ingredientes: String com ingredientes no formato "quantidade nome (unidade), quantidade nome (unidade), ..."
                     Ex: "2 bananas (unidade), 250 leite (ml), 1 açúcar (colher de sopa)"
        preparo: Passos para fazer a receita
        descricao: Descrição da receita (opcional)
    
    Returns:
        String com confirmação de sucesso ou mensagem de erro
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
                        description=f"Ingrediente da receita {nome}",
                        create_at=datetime.now()
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


@tool
def delete_recipe_tool(recipe_name: str) -> str:
    """
    Deleta uma receita do banco de dados por nome.
    
    Args:
        recipe_name: Nome da receita a ser deletada
    
    Returns:
        String com confirmação de sucesso ou mensagem de erro
    """
    from controllers import RecipeController

    db = SessionLocal()
    try:
        recipe = db.query(Recipe).filter(
            func.lower(Recipe.title).like(f'%{recipe_name.lower()}%')
        ).first()
        
        if not recipe:
            return f"Receita '{recipe_name}' não encontrada no banco de dados."
        
        recipe_id = recipe.id
        recipe_title = recipe.title

        RecipeController.delete_by_id(recipe_id, db=db)
        
        return f"Sucesso! A receita '{recipe_title}' foi removida do banco de dados."
    
    except Exception as e:
        return f"Erro ao deletar receita: {str(e)}"
    finally:
        db.close()


@tool
def update_recipe_tool(
    recipe_name: str, 
    new_title: str = None, 
    new_steps: str = None, 
    new_description: str = None
) -> str:
    """
    Atualiza informações de uma receita existente.
    
    Args:
        recipe_name: Nome da receita a ser atualizada
        new_title: Novo título (opcional)
        new_steps: Novo modo de preparo (opcional)
        new_description: Nova descrição (opcional)
    
    Returns:
        String com confirmação de sucesso ou mensagem de erro
    """
    from controllers import RecipeController

    db = SessionLocal()
    try:
        recipe = db.query(Recipe).filter(
            func.lower(Recipe.title).like(f'%{recipe_name.lower()}%')
        ).first()

        if not recipe:
            return f"Receita '{recipe_name}' não encontrada no banco de dados."

        old_title = recipe.title
        recipe_id = recipe.id

        update_data = {
            "title": new_title if new_title else recipe.title,
            "steps": new_steps if new_steps else recipe.steps,
            "description": new_description if new_description is not None else recipe.description
        }

        request = RecipeRequest(**update_data)
        RecipeController.update(recipe_id, request, db=db)

        updated_fields = []
        if new_title:
            updated_fields.append(f"título para '{new_title}'")
        if new_steps:
            updated_fields.append("modo de preparo")
        if new_description is not None:
            updated_fields.append("descrição")
        
        if not updated_fields:
            return "Nenhuma atualização foi especificada."
        
        updates_text = ", ".join(updated_fields)
        return f"Sucesso! Receita '{old_title}' atualizada: {updates_text}."
    
    except Exception as e:
        return f"Erro ao atualizar receita: {str(e)}"
    finally:
        db.close()

@tool
def list_all_items_tool() -> str:
    """
    Lista todos os itens do estoque.
    
    Returns:
        String formatada com lista de itens
    """
    from controllers import ItemController

    db = SessionLocal()
    try:
        items = ItemController.find_all(db=db)
        
        if not items:
            return "Estoque vazio."
        
        resultado = f"📦 Itens no estoque ({len(items)}):\n\n"
        for idx, item in enumerate(items, 1):
            resultado += f"{idx}. {item.name}: {item.amount}{item.measure_unity}"
            if item.price > 0:
                resultado += f" (R${item.price:.2f})"
            resultado += "\n"
        
        return resultado
    
    except Exception as e:
        return f"Erro ao listar itens: {str(e)}"
    finally:
        db.close()

@tool
def find_item_by_name_tool(item_name: str) -> str:
    """
    Busca item(ns) por nome e retorna detalhes.
    
    Args:
        item_name: Nome ou parte do nome do item
    
    Returns:
        String com detalhes do(s) item(ns)
    """
    from controllers import ItemController

    db = SessionLocal()
    try:
        items = ItemController.find_by_name(item_name, db=db)
        
        if not items:
            return f"Item '{item_name}' não encontrado no estoque."
        
        resultado = ""
        for item in items:
            resultado += f"📦 **{item.name}**\n"
            resultado += f"   Quantidade: {item.amount} {item.measure_unity}\n"
            if item.price > 0:
                resultado += f"   Preço: R${item.price:.2f} por {item.price_unit}\n"
            if item.description:
                resultado += f"   Descrição: {item.description}\n"
            if item.expiration_date:
                resultado += f"   Validade: {item.expiration_date.strftime('%d/%m/%Y')}\n"
            resultado += "\n"
        
        return resultado.strip()
    
    except Exception as e:
        return f"Erro ao buscar item: {str(e)}"
    finally:
        db.close()

@tool
def add_item_tool(
        name: str,
        amount: float,
        measure_unity: str,
        price: float = 0.0,
        price_unit: str = "unidade",
        description: str = "",
        expiration_date: str = None
) -> dict:
    """
    Adiciona um novo item ao estoque.
    Se o item já existe (mesmo nome + mesma unidade), ATUALIZA automaticamente somando a quantidade.

    Args:
        name: Nome do item
        amount: Quantidade a adicionar
        measure_unity: Unidade de medida
        price: Preço (opcional)
        price_unit: Unidade do preço (opcional)
        description: Descrição (opcional)
        expiration_date: Data de validade 'YYYY-MM-DD' (opcional)

    Returns:
        Dict com success, action ("created" ou "updated"), message, item_id e dados para transação
    """
    from controllers import ItemController
    from decimal import Decimal

    db = SessionLocal()
    try:
        exact_match = db.query(Item).filter(
            func.lower(Item.name) == name.lower(),
            func.lower(Item.measure_unity) == measure_unity.lower()
        ).first()

        if exact_match:
            current_amount = float(exact_match.amount)
            new_total = current_amount + amount
            current_price = float(exact_match.price) if exact_match.price else 0.0

            update_data = {
                "name": exact_match.name,
                "amount": new_total,
                "measure_unity": exact_match.measure_unity,
                "price": price if price > 0 else current_price,
                "price_unit": exact_match.price_unit,
                "description": exact_match.description or description,
                "update_at": datetime.now()
            }

            if expiration_date:
                try:
                    update_data["expiration_date"] = datetime.strptime(expiration_date, '%Y-%m-%d')
                except:
                    pass
            elif exact_match.expiration_date:
                update_data["expiration_date"] = exact_match.expiration_date

            request = ItemRequest(**update_data)
            ItemController.update(exact_match.id, request, db=db)

            return {
                "success": True,
                "action": "updated",
                "message": f"✓ Item '{name}' atualizado! Quantidade: {current_amount}{measure_unity} → {new_total}{measure_unity} (+{amount}{measure_unity}).",
                "item_id": exact_match.id,
                "item_name": name,
                "amount": amount,
                "total_amount": new_total,
                "measure_unity": measure_unity,
                "price": price if price > 0 else current_price,
                "price_unit": exact_match.price_unit
            }

        same_name_items = db.query(Item).filter(
            func.lower(Item.name) == name.lower()
        ).all()

        info_message = None
        if same_name_items:
            other_units = [item.measure_unity for item in same_name_items]
            units_text = ", ".join(other_units)
            info_message = (
                f"Nota: Já existe(m) item(ns) '{name}' em outra(s) unidade(s): {units_text}. "
                f"Criando novo item em {measure_unity}."
            )

        item_data = {
            "name": name,
            "amount": amount,
            "measure_unity": measure_unity,
            "price": price,
            "price_unit": price_unit,
            "description": description,
            "create_at": datetime.now()
        }

        if expiration_date:
            try:
                item_data["expiration_date"] = datetime.strptime(expiration_date, '%Y-%m-%d')
            except:
                pass

        request = ItemRequest(**item_data)
        result = ItemController.create(request, db=db)

        success_msg = f"✓ Item '{name}' adicionado ao estoque: {amount}{measure_unity}"
        if price > 0:
            success_msg += f" (R${price:.2f} por {price_unit})"
        success_msg += "."

        if info_message:
            success_msg = f"{info_message}\n{success_msg}"

        return {
            "success": True,
            "action": "created",
            "message": success_msg,
            "item_id": result.id,
            "item_name": name,
            "amount": amount,
            "measure_unity": measure_unity,
            "price": price,
            "price_unit": price_unit
        }

    except Exception as e:
        return {
            "success": False,
            "action": "error",
            "message": f"Erro ao adicionar item: {str(e)}"
        }
    finally:
        db.close()

@tool
def update_item_tool(
        item_name: str,
        measure_unity: str = None,
        amount_change: float = None,
        new_amount: float = None,
        new_price: float = None,
        new_expiration_date: str = None,
        operation_type: str = "uso"
) -> dict:
    """
    Atualiza um item existente.
    Retorna dict com dados para o TRANSACTION_WRITER.

    SEMPRE usa busca ILIKE com % para encontrar o item automaticamente.

    Args:
        item_name: Nome do item (busca aproximada automática)
        measure_unity: Unidade de medida (opcional, para desambiguação)
        amount_change: Mudança relativa na quantidade
        new_amount: Nova quantidade absoluta
        new_price: Novo preço
        new_expiration_date: Nova validade 'YYYY-MM-DD'
        operation_type: 'uso', 'venda', 'ajuste', 'compra'

    Returns:
        Dict com success, message e dados para transação
    """
    from controllers import ItemController
    from decimal import Decimal

    db = SessionLocal()
    try:

        # Remove espaços extras
        search_term = item_name.strip()

        items = db.query(Item).filter(
            func.lower(Item.name).like(f'%{search_term.lower()}%')
        ).all()

        if not items:
            return {
                "success": False,
                "message": f"❌ Item '{item_name}' não encontrado."
            }

        if measure_unity:
            items_filtered = [
                i for i in items
                if i.measure_unity.lower() == measure_unity.lower()
            ]

            if items_filtered:
                items = items_filtered

        if len(items) > 1:
            units_list = [f"{i.name} ({i.measure_unity})" for i in items]
            return {
                "success": False,
                "message": f"⚠️ Múltiplos itens encontrados: {', '.join(units_list)}. Especifique a unidade de medida ou use o nome completo.",
                "multiple_items": [
                    {
                        "id": i.id,
                        "name": i.name,
                        "measure_unity": i.measure_unity,
                        "amount": float(i.amount)
                    } for i in items
                ]
            }

        item = items[0]
        item_id = item.id
        old_amount = float(item.amount)
        measure_unity = item.measure_unity

        result = {
            "success": True,
            "item_id": item_id,
            "item_name": item.name,
            "measure_unity": measure_unity,
            "operation": "update"
        }

        if new_amount is not None:
            amount_diff = new_amount - old_amount
            final_amount = new_amount
        elif amount_change is not None:
            amount_diff = amount_change
            final_amount = old_amount + amount_change
        else:
            amount_diff = 0
            final_amount = old_amount

        if final_amount < 0:
            return {
                "success": False,
                "message": f"❌ Operação resultaria em quantidade negativa. Quantidade atual: {old_amount}{measure_unity}."
            }

        update_data = {
            "name": item.name,
            "amount": final_amount,
            "measure_unity": item.measure_unity,
            "price": new_price if new_price is not None else (float(item.price) if item.price else 0.0),
            "price_unit": item.price_unit,
            "description": item.description,
            "update_at": datetime.now()
        }

        if new_expiration_date:
            try:
                update_data["expiration_date"] = datetime.strptime(new_expiration_date, '%Y-%m-%d')
            except:
                pass
        elif item.expiration_date:
            update_data["expiration_date"] = item.expiration_date

        request = ItemRequest(**update_data)
        ItemController.update(item_id, request, db=db)

        result["amount_changed"] = amount_diff
        result["new_amount"] = final_amount
        result["old_amount"] = old_amount

        if operation_type == "uso":
            result["transaction_type"] = "uso"
            result["transaction_description"] = f"Uso de {item.name} - {abs(amount_diff)}{measure_unity}"
            result[
                "message"] = f"✓ {item.name} atualizado: {final_amount}{measure_unity} (usou {abs(amount_diff)}{measure_unity})."

        elif operation_type == "venda":
            result["transaction_type"] = "venda"
            result["transaction_description"] = f"Venda de {item.name} - {abs(amount_diff)}{measure_unity}"
            result[
                "message"] = f"✓ {item.name} atualizado: {final_amount}{measure_unity} (vendeu {abs(amount_diff)}{measure_unity})."

        elif operation_type == "ajuste":
            result["transaction_type"] = "ajuste"
            sinal = "+" if amount_diff > 0 else ""
            result[
                "transaction_description"] = f"Ajuste de estoque de {item.name}: de {old_amount}{measure_unity} para {final_amount}{measure_unity} ({sinal}{amount_diff}{measure_unity})"
            result[
                "message"] = f"✓ {item.name} ajustado: {final_amount}{measure_unity} ({sinal}{amount_diff}{measure_unity})."

        elif operation_type == "compra":
            result["transaction_type"] = "compra"
            result["transaction_description"] = f"Compra adicional de {item.name} - {amount_diff}{measure_unity}"
            result[
                "message"] = f"✓ {item.name} atualizado: {final_amount}{measure_unity} (adicionou {amount_diff}{measure_unity})."

        return result

    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Erro ao atualizar item: {str(e)}"
        }
    finally:
        db.close()


@tool
def delete_item_tool(item_name: str, reason: str = "perda") -> dict:
    """
    Deleta um item do estoque.
    Retorna dict com dados para o TRANSACTION_WRITER.
    
    Args:
        item_name: Nome do item
        reason: 'perda' ou 'venda'
    
    Returns:
        Dict com success, message e dados para transação
    """
    from controllers import ItemController

    db = SessionLocal()
    try:
        item = db.query(Item).filter(
            func.lower(Item.name).like(f'%{item_name.lower()}%')
        ).first()
        
        if not item:
            return {
                "success": False,
                "message": f"Item '{item_name}' não encontrado."
            }

        item_id = item.id
        item_name = item.name
        amount = float(item.amount)
        measure_unity = item.measure_unity

        ItemController.delete_by_id(item_id, db=db)

        transaction_type = reason if reason in ["perda", "venda"] else "perda"
        
        if transaction_type == "perda":
            description = f"Remoção de {item_name} do estoque - {amount}{measure_unity}"
            message = f"Sucesso! Item '{item_name}' removido do estoque ({amount}{measure_unity})."
        else:
            description = f"Venda total de {item_name} - {amount}{measure_unity}"
            message = f"Sucesso! Item '{item_name}' vendido e removido do estoque ({amount}{measure_unity})."
        
        return {
            "success": True,
            "message": message,
            "operation": "delete",
            "item_id": item_id,
            "item_name": item_name,
            "amount": amount,
            "measure_unity": measure_unity,
            "transaction_type": transaction_type,
            "transaction_description": description
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Erro ao deletar item: {str(e)}"
        }
    finally:
        db.close()

@tool
def get_low_stock_items_tool(threshold: int = 5) -> str:
    """
    Lista itens com estoque abaixo do limite.
    
    Args:
        threshold: Limite mínimo de quantidade
    
    Returns:
        String formatada com itens em falta
    """
    from controllers import ItemController

    db = SessionLocal()
    try:
        items = ItemController.get_low_stock_items(threshold, db=db)
        
        if not items:
            return f"Nenhum item com estoque abaixo de {threshold} unidades."
        
        resultado = f"⚠️ Itens com estoque baixo (menos de {threshold}):\n\n"
        for item in items:
            resultado += f"• {item.name}: {item.amount}{item.measure_unity}\n"
        
        return resultado
    
    except Exception as e:
        return f"Erro ao buscar itens: {str(e)}"
    finally:
        db.close()


@tool
def get_expired_items_tool() -> str:
    """
    Lista itens vencidos.
    
    Returns:
        String formatada com itens vencidos
    """
    from controllers import ItemController

    db = SessionLocal()
    try:
        items = ItemController.get_expired_items(db=db)
        
        if not items:
            return "Nenhum item vencido no estoque."
        
        resultado = "🚫 Itens vencidos:\n\n"
        for item in items:
            resultado += f"• {item.name}: {item.amount}{item.measure_unity} (venceu em {item.expiration_date.strftime('%d/%m/%Y')})\n"
        
        return resultado
    
    except Exception as e:
        return f"Erro ao buscar itens vencidos: {str(e)}"
    finally:
        db.close()

@tool
def add_transaction_tool(
    item_id: int,
    item_name: str,
    order_type: str,
    description: str,
    amount: float,
    price: float = None
) -> str:
    """
    Registra uma transação no histórico.
    
    Args:
        item_id: ID do item
        item_name: Nome do item
        order_type: 'compra', 'venda', 'uso', 'perda', 'ajuste'
        description: Descrição da transação
        amount: Quantidade (positivo=entrada, negativo=saída)
        price: Preço (opcional)
    
    Returns:
        String com confirmação
    """
    from controllers import TransactionController

    db = SessionLocal()
    try:
        valid_types = ['compra', 'venda', 'uso', 'perda', 'ajuste']
        if order_type not in valid_types:
            return f"Erro: tipo inválido '{order_type}'. Tipos válidos: {', '.join(valid_types)}"

        transaction_data = {
            "item_id": item_id,
            "order_type": order_type,
            "description": description,
            "create_at": datetime.now(),
            "amount": amount,
            "price": price if price else 0.0
        }
        
        request = TransactionRequest(**transaction_data)
        TransactionController.create(request, db=db)
        
        return f"✓ Transação registrada: {description}"
    
    except Exception as e:
        return f"✗ Erro ao registrar transação: {str(e)}"
    finally:
        db.close()


@tool
def get_transaction_history_tool(item_name: str = None, limit: int = 10) -> str:
    """
    Retorna histórico de transações.
    
    Args:
        item_name: Nome do item (opcional, se None retorna todas)
        limit: Número máximo de transações
    
    Returns:
        String formatada com histórico
    """
    from controllers import TransactionController

    db = SessionLocal()
    try:
        if item_name:
            item = db.query(Item).filter(
                func.lower(Item.name).like(f'%{item_name.lower()}%')
            ).first()
            
            if not item:
                return f"Item '{item_name}' não encontrado."
            
            transactions = TransactionController.find_by_item_id(item.id, db=db)
            titulo = f"Histórico de {item.name}"
        else:
            transactions = TransactionController.find_all(db=db)
            titulo = "Histórico de Transações"
        
        if not transactions:
            return "Nenhuma transação registrada."
        
        # Limitar número de transações
        transactions = transactions[:limit]
        
        resultado = f"{titulo} (últimas {len(transactions)}):\n\n"
        for trans in transactions:
            item = db.query(Item).filter(Item.id == trans.item_id).first()
            item_name = item.name if item else "Item deletado"
            
            resultado += f"{trans.create_at.strftime('%d/%m/%Y')}\n"
            resultado += f"{trans.order_type.upper()}: {trans.description}\n"
            resultado += f"Item: {item_name}\n"
            resultado += f"Quantidade: {trans.amount}\n"
            if trans.price and trans.price > 0:
                resultado += f"   Valor: R${trans.price:.2f}\n"
            resultado += "\n"
        
        return resultado.strip()
    
    except Exception as e:
        return f"Erro ao buscar histórico: {str(e)}"
    finally:
        db.close()