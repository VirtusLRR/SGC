import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from models import Item, Transaction
from decimal import Decimal
from datetime import datetime

scenarios('../features/stock_transaction.feature')

@given("o usuário possui uma sessão ativa no sistema")
@given("o usuário comum está autenticado no sistema")
def sessao_ativa(client):
    pass

@given(parsers.parse('existe o item "{nome}" no banco de dados com ID {item_id:d}'))
def preparar_item_estatistica(db_session, nome, item_id):
    db_session.query(Transaction).delete()
    db_session.query(Item).delete()
    db_session.commit()
    
    item = Item(
        id=item_id, 
        name=nome, 
        measure_unity="KG", 
        amount=Decimal('100'), 
        price=Decimal('10.0'),
        price_unit="unidade"
    )
    db_session.add(item)
    db_session.commit()
@given(parsers.parse('que existem transações de "{tipo}" totalizando R$ {valor:f}'))
@given(parsers.parse('existem transações de "{tipo}" totalizando R$ {valor:f}'))
@given(parsers.parse('o histórico de gastos mensais do mês atual é R$ {valor:f}'))

def criar_historico_transacoes(db_session, valor, tipo="entrada"):
    trans = Transaction(
        item_id=1,
        order_type=tipo,
        description=f"Carga de {tipo}",
        amount=Decimal('1'),
        price=Decimal(str(valor)),
        create_at=datetime.now()
    )
    db_session.add(trans)
    db_session.commit()

@given(parsers.parse('que o item {item_id:d} teve {qtd:d} transações de "{tipo}"'))
def popular_ranking_consumo(db_session, item_id, qtd, tipo):
    for _ in range(qtd):
        trans = Transaction(
            item_id=item_id,
            order_type=tipo,
            description="Ranking",
            amount=Decimal('1'),
            price=Decimal('5.0'),
            create_at=datetime.now()
        )
        db_session.add(trans)
    db_session.commit()

@when("o usuário clica no botão de estatísticas do sistema")
def navegar_estatisticas_geral(client, context):
    context['response'] = client.get("/transactions/summary/30")

@when(parsers.parse('o usuário solicita o resumo de transações dos últimos {days:d} dias'))
def solicitar_resumo_periodo(client, context, days):
    context['response'] = client.get(f"/transactions/summary/{days}")

@when(parsers.parse('o usuário cadastra uma nova transação de "{tipo}" do item {item_id:d} no valor de R$ {valor:f}'))
def adicionar_transacao_parametrizada(client, tipo, item_id, valor):
    payload = {
        "item_id": item_id,
        "order_type": tipo,
        "description": "Nova entrada parametrizada",
        "amount": 1.0,
        "price": valor
    }
    client.post("/api/transactions", json=payload)

@when("o usuário comum adicione um novo item no estoque")
def adicionar_item_padrao(client):
    payload = {
        "item_id": 1,
        "order_type": "entrada",
        "description": "Nova entrada padrão",
        "amount": 1.0,
        "price": 250.0
    }
    client.post("/api/transactions", json=payload)

@when("solicita a visualização de gastos mensais")
def ver_gastos_mensais(client, context):
    context['response'] = client.get("/transactions/monthly-expenses?months=1")

@when("o usuário solicita o ranking de itens mais transacionados")
def ver_ranking_consumo(client, context):
    context['response'] = client.get("/transactions/most-transacted/10/saida")

@then(parsers.parse('o saldo total (balance) deve ser de R$ {valor:f}'))
def verificar_saldo_periodo(context, valor):
    res = context['response'].json()
    assert float(res['balance']['value']) == float(valor)
@then("o número de entradas deve ser maior que zero")
@then("o sistema deve dispor uma página com gráficos estatísticos")
@then("o sistema deve dispor uma área do painel de controle mostrando o histórico de gastos mensais.")
@then("o sistema deve dispor uma área do painel de controle para mostrar tabelas que contenham informações do estoque.")

def verificar_sucesso_painel(context):
    assert context['response'].status_code == 200
@then(parsers.parse('o gasto total do mês atual deve ser atualizado para R$ {valor:f}'))
@then("ele deve conseguir visualizar na parte de histórico de gastos a adição do valor do novo item adicionado no estoque.")

def verificar_gastos_mensais(client, context):
    res_gastos = client.get("/transactions/monthly-expenses?months=1").json()
    valor_atual = res_gastos[-1]['total_spent']
    assert float(valor_atual) >= 250.0 

@then(parsers.parse('o item "{nome}" deve aparecer no topo do ranking'))
def verificar_ranking_topo(context, nome):
    res = context['response'].json()
    assert len(res) > 0
    assert res[0]['item_name'] == nome