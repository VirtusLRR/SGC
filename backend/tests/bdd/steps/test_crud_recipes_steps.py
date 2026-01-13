import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Aponta para o arquivo de feature
scenarios('../features/crud_recipes.feature')

# NOTA: Não precisamos definir 'client' nem 'context' aqui,
# pois eles já vêm do conftest.py!

# --- STEPS ---

@given('o usuário está autenticado no sistema')
def usuario_autenticado():
    pass

@given('acessa a página de receitas')
def acessa_pagina_receitas():
    pass

# --- Cenário 1: Receita Viável ---

@given(parsers.parse('que existe uma receita "{nome_receita}" cadastrada e viável'))
def criar_receita_viavel(client, context, nome_receita):
    context["recipe_title"] = nome_receita
    
    # 1. Cria Ingrediente
    ing_payload = {
        "name": f"Ingrediente {nome_receita}",
        "price": 5.0,
        "amount": 1000.0,
        "measure_unity": "kg",
        "price_unit": "kg",
        "expiration_date": "2025-12-31"
    }
    resp_ing = client.post("/api/items", json=ing_payload)
    
    if resp_ing.status_code == 201:
        ing_id = resp_ing.json()["id"]
    else:
        items = client.get("/api/items").json()
        ing_id = items[0]["id"] if items else 1

    # 2. Cria Receita
    rec_payload = {
        "title": nome_receita,
        "steps": "1. Misturar. 2. Assar.",
        "description": "Receita viável",
        "recipe_itens": [ 
            {"item_id": ing_id, "amount": 1.0}
        ]
    }
    client.post("/api/recipes", json=rec_payload)

@when(parsers.parse('o usuário pesquisa o nome "{termo_busca}"'))
def pesquisar_receita(client, context, termo_busca):
    response = client.get("/api/recipes", params={"name": termo_busca})
    context["response"] = response

@then(parsers.parse('o sistema deve exibir a receita "{nome_esperado}" na lista'))
def verifica_receita_na_lista(context, nome_esperado):
    response_json = context["response"].json()
    assert isinstance(response_json, list)
    
    found = any(r.get("title") == nome_esperado for r in response_json)
    assert found is True, f"A receita '{nome_esperado}' não foi encontrada."

# --- Cenário 2: Receita Inviável ---

@given(parsers.parse('que existe uma receita "{nome_receita}" que necessita de "{nome_ingrediente}"'))
def criar_receita_com_ingrediente(client, context, nome_receita, nome_ingrediente):
    context["recipe_title"] = nome_receita
    
    # 1. Cria ingrediente
    ing_payload = {
        "name": nome_ingrediente,
        "price": 10.0,
        "amount": 5.0,
        "measure_unity": "kg",
        "price_unit": "kg",
        "expiration_date": "2025-12-31"
    }
    resp_ing = client.post("/api/items", json=ing_payload)
    
    if resp_ing.status_code == 201:
        ing_id = resp_ing.json()["id"]
    else:
        items = client.get("/api/items").json()
        target = next((i for i in items if i["name"] == nome_ingrediente), None)
        ing_id = target["id"] if target else 1
        
    context["ingredient_id"] = ing_id

    # 2. Cria Receita (Inviável)
    rec_payload = {
        "title": nome_receita,
        "steps": "Passos...",
        "description": "Receita inviável",
        "recipe_itens": [
            {"item_id": ing_id, "amount": 2.0}
        ]
    }
    client.post("/api/recipes", json=rec_payload)

@given(parsers.parse('o estoque de "{nome_ingrediente}" está zerado'))
def zerar_estoque(client, context, nome_ingrediente):
    ing_id = context.get("ingredient_id")
    current = client.get(f"/api/items/{ing_id}").json()
    current["amount"] = 0.0
    client.put(f"/api/items/{ing_id}", json=current)

@then(parsers.parse('o sistema deve exibir a mensagem "{mensagem_erro}"'))
def verifica_mensagem_inviabilidade(client, context, mensagem_erro):
    assert context["response"].status_code == 200
    
    resp_feasible = client.get("/recipes/feasible")
    feasible_list = resp_feasible.json()
    
    nome_receita = context["recipe_title"]
    esta_viavel = any(r.get("recipe_title") == nome_receita for r in feasible_list)
    
    if "não é viável" in mensagem_erro:
        assert esta_viavel is False, f"Erro: '{nome_receita}' apareceu como viável com estoque zero."