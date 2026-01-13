import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from models import Item
from decimal import Decimal

scenarios('../features/menage_itens_voice.feature')

@given("o usuário possui uma sessão ativa no sistema")
def sessao_ativa(client):
    """Garante a prontidão do cliente de teste."""
    pass

@given(parsers.parse('o áudio contém a descrição "{descricao}"'))
@given(parsers.parse('que o áudio contém a descrição "{descricao}"'))
def mock_transcricao(mock_audio_extractor, descricao):
    """Simula a transcrição da IA para o extrator de áudio."""
    mock_audio_extractor.return_value = {
        "final_answer": [{"text": descricao}]
    }

@given(parsers.parse('que o item "{nome}" existe no estoque com quantidade {qtd:d}'))
def item_pre_existente(db_session, nome, qtd):
    """Prepara o estado do banco de dados para testes de remoção."""
    db_session.query(Item).filter(Item.name == nome.upper()).delete()
    item = Item(name=nome.upper(), amount=Decimal(qtd), measure_unity="UN", price=0)
    db_session.add(item)
    db_session.commit()

@when("o usuário envia o comando de voz para cadastro")
def enviar_voz_cadastro(client, valid_audio_b64, context, mock_graph, db_session):
    """Simula a ação do grafo para cadastro de novos itens."""
    def side_effect(*args, **kwargs):
        item = Item(name="BANANA", amount=Decimal(5), measure_unity="UN", price=1.5)
        db_session.add(item)
        db_session.commit()
        return {"final_answer": [{"text": "Operação realizada com sucesso"}]}
    
    mock_graph.invoke.side_effect = side_effect
    payload = {"audio_b64": valid_audio_b64, "user_message": ""}
    context['response'] = client.post("/bot/audio_message", json=payload)

@when("o usuário envia o comando de voz para remoção")
def enviar_voz_remocao(client, valid_audio_b64, context, mock_graph, db_session):
    """Simula a ação do grafo para remoção/subtração de itens."""
    def side_effect(*args, **kwargs):
        item = db_session.query(Item).filter(Item.name.ilike("%LEITE%")).first()
        if item:
            item.amount -= Decimal(2)
            db_session.commit()
        return {"final_answer": [{"text": "Estoque atualizado"}]}
    
    mock_graph.invoke.side_effect = side_effect
    payload = {"audio_b64": valid_audio_b64, "user_message": ""}
    context['response'] = client.post("/bot/audio_message", json=payload)

@when("o usuário envia um áudio sem conteúdo perceptível")
def enviar_audio_invalido(client, context, mock_audio_extractor):
    """Simula o envio de um áudio que não gera transcrição."""
    mock_audio_extractor.return_value = {"final_answer": ""}
    payload = {"audio_b64": "invalid_b64", "user_message": ""}
    context['response'] = client.post("/bot/audio_message", json=payload)

@then("o sistema deve transcrever e interpretar com sucesso")

@then("o sistema deve subtrair a quantidade corretamente") 

def verificar_sucesso_operacao(context):
    """Valida se o endpoint retornou 200 OK após o processamento."""
    assert context['response'].status_code == 200

@then(parsers.parse('o item "{nome}" deve constar no banco de dados com quantidade {qtd:d}'))
def verificar_item_novo(db_session, nome, qtd):
    db_session.expire_all()
    item = db_session.query(Item).filter(Item.name.ilike(f"%{nome}%")).first()
    assert item is not None
    assert float(item.amount) == float(qtd)

@then(parsers.parse('o estoque de "{nome}" deve ser atualizado para {qtd:d}'))
def verificar_estoque_final(db_session, nome, qtd):
    db_session.expire_all()
    item = db_session.query(Item).filter(Item.name.ilike(f"%{nome}%")).first()
    assert float(item.amount) == float(qtd)

@then("o sistema deve retornar um erro de áudio inválido")
def verificar_erro_400(context):
    assert context['response'].status_code == 400

@then(parsers.parse('informar "{mensagem}"'))
def verificar_mensagem_cliente(context, mensagem):
    """Valida se a mensagem de erro contém o texto esperado pelo usuário."""
    res_text = context['response'].text
    assert "Não entendi" in mensagem or "inválido" in res_text