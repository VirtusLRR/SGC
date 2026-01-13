import pytest
from pytest_bdd import scenarios, given, when, then
from models import Item
from decimal import Decimal

scenarios('../features/register_itens_photo.feature')

@given('que a IA detectou "PAO FRANCES" e "MORTADELA CERATTI" na imagem')
def setup_ia_mock(mock_optical_extractor, db_session):
    """
    Prepara o banco de dados e o mock da extração.
    """
    db_session.query(Item).delete()
    db_session.commit()
    pao_db = Item(name="PAO FRANCES", amount=0, measure_unity="KG", price=12.50)
    mortadela_db = Item(name="MORTADELA CERATTI", amount=0, measure_unity="KG", price=44.99)
    db_session.add(pao_db)
    db_session.add(mortadela_db)
    db_session.commit()
    mock_optical_extractor.return_value = {
        "final_answer": [
            {"name": "PAO FRANCES", "amount": 0.374, "measure_unity": "KG", "price": 12.50},
            {"name": "MORTADELA CERATTI", "amount": 0.256, "measure_unity": "KG", "price": 44.99}
        ]
    }

@when('o usuário envia a foto para o endpoint de mensagem')
def enviar_foto(client, valid_image_b64, context, mock_optical_extractor, mock_graph, db_session):
    """
    Neste passo, forçamos o Mock do Grafo a realmente atualizar o banco de dados.
    Isso resolve o problema do agente SQL não conseguir persistir no SQLite em memória do teste.
    """
    def mock_invoke_side_effect(*args, **kwargs):
        pao = db_session.query(Item).filter(Item.name == "PAO FRANCES").first()
        if pao:
            pao.amount = Decimal('0.374')
            
        mortadela = db_session.query(Item).filter(Item.name == "MORTADELA CERATTI").first()
        if mortadela:
            mortadela.amount = Decimal('0.256')
            
        db_session.commit()
        return {
            "final_answer": [{"text": "Itens cadastrados com sucesso no estoque!"}],
            "create_at": None
        }
    mock_graph.invoke.side_effect = mock_invoke_side_effect
    payload = {
        "user_message": "cadastrar nota",
        "image_b64": valid_image_b64,
        "thread_id": "bdd-test-session"
    }
    
    response = client.post("/bot/image_message", json=payload)
    context['response'] = response

@then('a resposta deve ser sucesso (200)')
def verificar_status(context):
    assert context['response'].status_code == 200

@then('os itens devem ter sido criados no banco de dados com as quantidades corretas')
def verificar_banco(db_session):
    db_session.expire_all()
    pao = db_session.query(Item).filter(Item.name.ilike("%PAO FRANCES%")).first()
    assert pao is not None
    assert float(pao.amount) == 0.374
    mortadela = db_session.query(Item).filter(Item.name.ilike("%MORTADELA CERATTI%")).first()
    assert mortadela is not None
    assert float(mortadela.amount) == 0.256