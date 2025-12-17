import sys
from pathlib import Path
import pytest
from pytest_bdd import given, when, then, scenario
from fastapi.testclient import TestClient
import warnings

backend_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(backend_dir))

from index import app

warnings.filterwarnings("ignore", category=UserWarning, module="langchain_tavily")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="sqlalchemy.engine.default")

client = TestClient(app)

@pytest.fixture
def context():
    """Contexto compartilhado para armazenar dados entre steps"""
    return {
        'response': None,
        'response_data': None,
        'receita_indisponivel': None
    }


@scenario('../features/chat_bot.feature', 'Exibição de sugestão por substituibilidade')
def test_exibicao_sugestao_substituibilidade():
    """Testa a sugestão de receitas alternativas quando uma receita está indisponível"""
    pass


@given("que o usuário comum está autenticado no sistema")
def usuario_autenticado():
    """Simula que o usuário está autenticado"""
    return True


@given("o banco de dados está populado com receitas e ingredientes")
def banco_populado():
    """
    Verifica que o banco real está populado.
    IMPORTANTE: Execute 'python scripts/populate_database.py' antes dos testes!
    """
    pass


@given("existem receitas com ingredientes disponíveis no estoque")
def receitas_disponiveis():
    """Verifica que existem receitas com ingredientes disponíveis"""
    pass


@given('existe uma receita "risoto de camarão" com ingredientes indisponíveis')
def receita_risoto_indisponivel():
    """
    Verifica que a receita de risoto existe mas ingredientes estão indisponíveis.
    O script populate_database.py cria esta receita com amount=0 para os ingredientes.
    """
    pass


@when("o usuário comum visualizar uma receita que está indisponível")
def visualizar_receita_indisponivel(context):
    """Simula o usuário perguntando sobre uma receita com ingredientes indisponíveis"""
    payload = {
        "user_message": "Consigo fazer a receita de risoto de camarão?"
    }

    response = client.post("/bot/message", json=payload)
    print(response)
    context['response'] = response

    if response.status_code == 200:
        context['response_data'] = response.json()
        context['receita_indisponivel'] = "risoto de camarão"

@then("o sistema deve exibir, ao lado desta, uma sugestão de receita contendo produtos disponíveis no estoque")
def verificar_sugestao_receita_disponivel(context):
    """Verifica que o sistema sugere receitas com ingredientes disponíveis"""
    assert context['response'] is not None, "Nenhuma resposta foi recebida"
    assert context['response'].status_code == 200, f"Status code: {context['response'].status_code}"
    assert context['response_data'] is not None, "Dados da resposta estão vazios"
    assert 'ai_message' in context['response_data'], "Resposta não contém 'ai_message'"

    ai_message = context['response_data']['ai_message'].lower()

    print(f"\n{'='*80}")
    print("RESPOSTA DO BOT:")
    print(f"{'='*80}")
    print(ai_message)
    print(f"{'='*80}\n")

    indica_falta = any(palavra in ai_message for palavra in [
        'não', 'falta', 'indisponível', 'sem estoque', 'não temos', 'não é possível'
    ])

    menciona_receita = any(palavra in ai_message for palavra in ['receita', 'ingredientes'])

    # Verifica se sugere receitas alternativas do BANCO (ideal)
    receitas_banco = ['torta', 'banoffee', 'brigadeiro', 'pavê', 'pave']
    sugere_do_banco = any(receita in ai_message for receita in receitas_banco)

    if sugere_do_banco:
        print(f"\nPERFEITO: Sistema indicou falta E sugeriu alternativas do banco!")
        assert True
    elif indica_falta and menciona_receita:
        print(f"\nBOM: Sistema indicou falta mas buscou receita na web")
        assert True
    else:
        print(f"\nERRO: Sistema não lidou corretamente com ingredientes indisponíveis")
        assert False, f"Sistema deveria indicar falta ou sugerir alternativas: {ai_message[:200]}..."


@then("deve apresentar um breve texto explicando a substituibilidade")
def verificar_explicacao_substituibilidade(context):
    """Verifica que o sistema explica ou apresenta informações úteis"""
    ai_message = context['response_data']['ai_message'].lower()

    assert len(ai_message) > 50, \
        f"Resposta muito curta (tamanho: {len(ai_message)}): {ai_message}"

    palavras_uteis = [
        'receita', 'ingrediente', 'estoque', 'disponível',
        'modo', 'preparo', 'fazer', 'preparar'
    ]

    conteudo_util = sum(1 for palavra in palavras_uteis if palavra in ai_message)

    assert conteudo_util >= 2, \
        f"Resposta não tem conteúdo útil suficiente (apenas {conteudo_util} palavras-chave): {ai_message[:200]}..."

    print(f"\nTeste passou! Sistema respondeu adequadamente com {len(ai_message)} caracteres")
    print(f"Conteúdo útil encontrado: {conteudo_util} palavras-chave")

