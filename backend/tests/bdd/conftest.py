import pytest
import sys
import os
from fastapi.testclient import TestClient

# --- BLOCO DE IMPORTAÇÃO ROBUSTO (Serve para todos os testes) ---
# Adiciona a raiz do projeto ao Python Path
sys.path.append(os.getcwd())

# Tenta encontrar a instância 'app' do FastAPI
try:
    from main import app
except ImportError:
    try:
        from app.main import app
    except ImportError:
        try:
            from src.main import app
        except ImportError:
            # Se cair aqui, precisamos investigar o nome do seu arquivo
            raise ImportError("CRÍTICO: Não foi possível encontrar 'main.py' ou 'app.py' na raiz do projeto.")
# ---------------------------------------------------------------

# Configuração do BDD (que você já tinha)
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "bdd: marca testes BDD com pytest-bdd"
    )

# --- FIXTURE DO CLIENTE (Disponível para TODOS os testes) ---
@pytest.fixture(scope="session") # Scope session para criar o app uma vez só
def client():
    """
    Cria uma instância do TestClient que será reutilizada.
    """
    with TestClient(app) as client:
        yield client

# --- FIXTURE DE CONTEXTO (Para passar dados entre steps do BDD) ---
@pytest.fixture
def context():
    return {}