import pytest
import sys
from pathlib import Path
from unittest.mock import patch
import warnings
import time

warnings.filterwarnings("ignore", category=UserWarning, module="langchain_tavily")

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from services.graph.graph import graph
from conftest import populated_db_session
from database.database import get_db

@pytest.fixture
def mock_db(populated_db_session):
    def mock_get_db():
        try:
            yield populated_db_session
        except:
            pass
    with patch('database.database.get_db', mock_get_db):
        yield populated_db_session

@pytest.mark.parametrize(
    "user_input, expected_agent, description",
    [
        ("Oi, tudo bem??", "TRIVIAL", "Pergunta de saudação."),
        ("O que você pode fazer?", "TRIVIAL", "Pergunta sobre o sistema."),
        ("Como funciona esse sistema?", "TRIVIAL", "Pergunta sobre o sistema"),
    ]
)
def test_trivial_agent(mock_db, user_input, expected_agent, description):
    time.sleep(10)  # Pequena pausa para evitar sobrecarga
    print("\n-------------------------------------")
    print(f"Executando teste: {description}")
    print(f"Input do usuário: {user_input}")
    print(f"Agente esperado: {expected_agent}")
    print("---------------------------------------")
    thread = {"configurable": {"thread_id": "test_thread"}}

    response = graph.invoke({'user_input': user_input}, thread)

    assert response["next_agent"] == expected_agent, f"Falha no teste: {description}"

@pytest.mark.parametrize(
    "user_input, expected_agent, description",
    [
        ("Quantos itens de bananas temos em estoque?", "FINALIZAR", "Consulta SQL com sucesso - quantidade em estoque"),
        ("Qual o preço do doce de leite?", "FINALIZAR", "Consulta SQL com sucesso - preço do item"),
        ("Temos biscoito maisena em estoque?", "FINALIZAR", "Consulta SQL com sucesso - verificação de disponibilidade"),
        ("Quantas receitas temos cadastradas?", "FINALIZAR", "Consulta SQL com sucesso - contagem de receitas"),
    ]
)
def test_sql_agent_success(mock_db, user_input, expected_agent, description):
    time.sleep(10)  # Pequena pausa para evitar sobrecarga
    print("\n-------------------------------------")
    print(f"Executando teste: {description}")
    print(f"Input do usuário: {user_input}")
    print(f"Agente esperado após revisor: {expected_agent}")
    print("---------------------------------------")
    thread = {"configurable": {"thread_id": "test_thread_sql_success"}}

    response = graph.invoke({'user_input': user_input}, thread)

    print(f"Next agent final: {response.get('next_agent', 'N/A')}")
    print(f"Resposta SQL: {response.get('sql_response', 'N/A')[:200]}...")
    print("---------------------------------------")

    assert response["next_agent"] == expected_agent, f"Falha no teste: {description} - Esperava {expected_agent}, recebeu {response['next_agent']}"

@pytest.mark.parametrize(
    "user_input, expected_agent, description",
    [
        ("Quais receitas tem abacaxi?", "WEB", "SQL não encontrou - Revisor manda para WEB buscar receitas com abacaxi"),
        ("Mostre receitas de lasanha", "WEB", "SQL não encontrou - Revisor manda para WEB buscar receitas de lasanha"),
        ("Como fazer parmegiana?", "WEB", "SQL não encontrou - Revisor manda para WEB buscar receita de parmegiana"),
    ]
)
def test_sql_to_web_flow(mock_db, user_input, expected_agent, description):
    time.sleep(10)  # Pequena pausa para evitar sobrecarga
    print("\n-------------------------------------")
    print(f"Executando teste: {description}")
    print(f"Input do usuário: {user_input}")
    print(f"Agente esperado após revisor: {expected_agent}")
    print("---------------------------------------")
    thread = {"configurable": {"thread_id": "test_thread_sql_to_web"}}

    response = graph.invoke({'user_input': user_input}, thread)

    print(f"Next agent final: {response.get('next_agent', 'N/A')}")
    print(f"Resposta SQL: {response.get('sql_response', 'N/A')[:200]}...")
    print(f"Resposta final: {response.get('final_answer', 'N/A')[:200]}...")
    print("---------------------------------------")

    assert response["next_agent"] == expected_agent, f"Falha no teste: {description} - Esperava {expected_agent}, recebeu {response['next_agent']}"
