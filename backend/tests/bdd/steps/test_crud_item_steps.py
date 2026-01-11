import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
from datetime import datetime

scenarios('../features/crud_item.feature')

@pytest.fixture
def context():
    return {
        "payload": {},
        "response": None
    }
    
@given('o usuário está autenticado no sistema')
def usuario_autenticado():
    pass

@given('acessa a página de cadastro de itens')
def acessa_pagina_cadastro(context):
    context["payload"] = {
        "measure_unity": "unidade", 
        "price_unit": "R$",
        "expiration_date": None
    }

@when(parsers.parse('o usuário informa o nome "{nome}"'))
def informa_nome(context, nome):
    context["payload"]["name"] = nome

@when('o usuário deixa o campo nome em branco')
def nome_em_branco(context):
    context["payload"]["name"] = ""

@when(parsers.parse('o preço "{preco}"'))
def informa_preco(context, preco):
    context["payload"]["price"] = float(preco)

@when(parsers.parse('a quantidade "{qtd}"'))
def informa_quantidade(context, qtd):
    context["payload"]["amount"] = float(qtd)

@when(parsers.parse('a validade "{data}"'))
def informa_validade(context, data):
    dia, mes = data.split('/')
    ano_atual = datetime.now().year
    data_iso = f"{ano_atual}-{mes}-{dia}"
    context["payload"]["expiration_date"] = data_iso

@when('confirma o cadastro')
def confirma_cadastro(client, context):
    response = client.post("/api/items", json=context["payload"])
    context["response"] = response

@then(parsers.parse('o sistema deve retornar status {status_code}'))
def verifica_status(context, status_code):
    if "ou" in status_code:
        codigos_validos = [int(code.strip()) for code in status_code.split('ou')]
        assert context["response"].status_code in codigos_validos
    else:
        assert context["response"].status_code == int(status_code)

@then(parsers.parse('o sistema deve exibir a mensagem "{mensagem}"'))
def verifica_mensagem(context, mensagem):
    response_json = context["response"].json()
    if context["response"].status_code == 201:
        
        if "cadastrado com sucesso" in mensagem:
            assert response_json["name"] == context["payload"]["name"]
            return
            
    detail = response_json.get("detail", "")
    
    if isinstance(detail, list):
        detail = str(detail)
    
    assert mensagem.lower() in str(detail).lower()

@then(parsers.parse('o produto "{nome_produto}" deve aparecer na lista de produtos'))
def verifica_lista(client, nome_produto):
    response = client.get("/api/items")
    items = response.json()
    item_encontrado = any(i['name'] == nome_produto for i in items)
    assert item_encontrado is True
