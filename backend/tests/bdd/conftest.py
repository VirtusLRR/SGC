import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database.database import Base, get_db
from index import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def pytest_configure(config):
    """Configuração adicional do pytest para BDD"""
    config.addinivalue_line(
        "markers", "bdd: marca testes BDD com pytest-bdd"
    )

@pytest.fixture(scope="function")
def db_session():
    """
    Fixture que cria as tabelas no banco em memória antes do teste
    e apaga tudo depois. Garante um banco limpo a cada cenário.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Fixture principal: Cria o cliente da API (o 'navegador' falso).
    Substitui a dependência do banco real pelo banco de teste (db_session).
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
