from fastapi.testclient import TestClient
from unittest.mock import patch
import pytest
import sys

sys.path.insert(0, '/backend')

with patch('index.wait_for_db'):
    from index import app

print(f"App importado com sucesso de index.py")

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "bdd: marca testes BDD com pytest-bdd"
    )

@pytest.fixture(scope="session")
def client():
    """Cria uma instância do TestClient que será reutilizada."""
    with TestClient(app) as client:
        yield client

@pytest.fixture
def context():
    return {}