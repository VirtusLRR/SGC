from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pytest
import sys
import os
import base64
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime

sys.path.append(os.getcwd())
sys.path.insert(0, '/backend')

from database.database import Base, get_db

with patch('index.wait_for_db'):
    try:
        from index import app
    except ImportError:
        try:
            from main import app
        except ImportError:
            try:
                from app.main import app
            except ImportError:
                try:
                    from src.main import app
                except ImportError:
                    raise ImportError("CRÍTICO: Não foi possível encontrar 'main.py' ou 'app.py'")

print(f"App importado com sucesso.")

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

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Cria tabelas no banco em memória antes do teste e apaga depois.
    Isso garante isolamento mesmo usando o client global.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def override_dependency(db_session):
    """
    Substitui automaticamente a dependência get_db do FastAPI 
    pelo banco em memória durante os testes.
    """
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def valid_image_b64():
    """Busca a imagem na pasta pai (tests/) e converte para Base64."""
    base_path = os.path.dirname(__file__) 
    image_path = os.path.abspath(os.path.join(base_path, "..", "image_test.jpg"))
    if not os.path.exists(image_path):
        print(f"ERRO: Arquivo não encontrado em {image_path}")
        return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

@pytest.fixture
def mock_optical_extractor():
    """Mock do OCR para não chamar API externa"""
    with patch("controllers.bot.optical_extractor") as mock:
        yield mock

@pytest.fixture
def mock_graph():
    """Mock do LangChain/Graph"""
    with patch("services.graph.graph.graph") as mock:
        mock.invoke.return_value = {
            "final_answer": [{"text": "Processamento OK"}],
            "create_at": None
        }
        yield mock

@pytest.fixture
def valid_audio_b64():
    """Busca o áudio na pasta pai (tests/) e converte para Base64."""
    base_path = os.path.dirname(__file__)
    audio_path = os.path.abspath(os.path.join(base_path, "..", "audio_test.m4a"))

    if os.path.exists(audio_path):
        with open(audio_path, "rb") as audio_file:
            return base64.b64encode(audio_file.read()).decode("utf-8")
    return "base64_fake_audio_data"

@pytest.fixture
def mock_audio_extractor():
    """Mock do extrator de áudio"""
    with patch("controllers.bot.audio_extractor") as mock:
        yield mock

@pytest.fixture(autouse=True)
def setup_statistics_db(db_session):
    """
    Garante que o banco de dados esteja limpo antes de cada teste de estatística.
    O autouse=True faz com que o pytest rode isso automaticamente.
    """
    from models import Transaction, Item, Recipe, RecipeItem
    db_session.query(Transaction).delete()
    db_session.query(RecipeItem).delete()
    db_session.query(Recipe).delete()
    db_session.query(Item).delete()
    db_session.commit()

@pytest.fixture
def mock_datetime_now():
    """
    Útil para testes de estatísticas que dependem da data atual.
    Permite 'congelar' o tempo se necessário.
    """
    with patch('sqlalchemy.sql.functions.now') as mock_now:
        mock_now.return_value = datetime(2026, 1, 13)
        yield mock_now