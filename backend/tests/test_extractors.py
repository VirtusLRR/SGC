import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import base64
import os
from index import app
from schemas import BotResponse
from conftest import db_session
from database.database import get_db


def override_get_db(db_session):
    yield db_session


@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def valid_image_b64():
    """Carrega a imagem de teste e converte para base64"""
    image_path = os.path.join(os.path.dirname(__file__), "image_test.jpg")
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        return base64.b64encode(image_data).decode("utf-8")


@pytest.fixture
def valid_audio_b64():
    """Carrega o áudio de teste e converte para base64"""
    audio_path = os.path.join(os.path.dirname(__file__), "audio_test.m4a")
    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()
        return base64.b64encode(audio_data).decode("utf-8")


@pytest.fixture
def mock_optical_extractor():
    """Mock do extrator óptico"""
    with patch("controllers.bot.optical_extractor") as mock:
        mock.return_value = {
            "final_answer": "Adicionar 5 bananas ao estoque"
        }
        yield mock


@pytest.fixture
def mock_audio_extractor():
    """Mock do extrator de áudio"""
    with patch("controllers.bot.audio_extractor") as mock:
        mock.return_value = {
            "final_answer": "Cadastrar receita de bolo de chocolate"
        }
        yield mock


@pytest.fixture
def mock_graph():
    """Mock do grafo de processamento"""
    with patch("services.graph.graph.graph") as mock:
        mock.invoke.return_value = {
            "final_answer": [{"text": "Operação realizada com sucesso"}],
            "create_at": None
        }
        yield mock


# ==================== TESTES PARA /bot/image_message ====================

def test_process_image_message_success(client, valid_image_b64, mock_optical_extractor, mock_graph):
    """Testa o processamento bem-sucedido de uma mensagem com imagem"""
    payload = {
        "user_message": "",
        "image_b64": valid_image_b64
    }
    
    response = client.post("/bot/image_message", json=payload)
    
    assert response.status_code == 200
    bot_response = BotResponse.model_validate(response.json())
    
    assert bot_response.id is not None
    assert bot_response.thread_id is not None
    assert bot_response.user_message == "Adicionar 5 bananas ao estoque"
    assert bot_response.ai_message == "Operação realizada com sucesso"
    
    # Verifica se o extrator foi chamado com a imagem
    mock_optical_extractor.assert_called_once_with(valid_image_b64)
    
    # Verifica se o grafo foi invocado
    mock_graph.invoke.assert_called_once()


def test_process_image_message_with_thread_id(client, valid_image_b64, mock_optical_extractor, mock_graph):
    """Testa o processamento de imagem com thread_id fornecido"""
    thread_id = "test-thread-123"
    payload = {
        "user_message": "",
        "image_b64": valid_image_b64,
        "thread_id": thread_id
    }
    
    response = client.post("/bot/image_message", json=payload)
    
    assert response.status_code == 200
    bot_response = BotResponse.model_validate(response.json())
    
    assert bot_response.thread_id == thread_id


def test_process_image_message_invalid_base64(client):
    """Testa o processamento de imagem com base64 inválido"""
    payload = {
        "user_message": "",
        "image_b64": "invalid-base64-string!!!"
    }
    
    response = client.post("/bot/image_message", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Imagem inválida"


def test_process_image_message_missing_image(client):
    """Testa o processamento sem imagem fornecida"""
    payload = {
        "user_message": ""
    }
    
    response = client.post("/bot/image_message", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Imagem inválida"


def test_process_image_message_empty_image(client):
    """Testa o processamento com string de imagem vazia"""
    payload = {
        "user_message": "",
        "image_b64": ""
    }
    
    response = client.post("/bot/image_message", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Imagem inválida"


def test_process_image_message_extractor_returns_empty(client, valid_image_b64, mock_graph):
    """Testa quando o extrator retorna string vazia"""
    with patch("controllers.bot.optical_extractor") as mock_extractor:
        mock_extractor.return_value = {
            "final_answer": ""
        }
        
        payload = {
            "user_message": "",
            "image_b64": valid_image_b64
        }
        
        response = client.post("/bot/image_message", json=payload)
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Imagem inválida"
        
        # Garante que o grafo NÃO foi invocado
        mock_graph.invoke.assert_not_called()


def test_process_image_message_extractor_returns_list(client, valid_image_b64, mock_graph):
    """Testa quando o extrator retorna uma lista com texto"""
    with patch("controllers.bot.optical_extractor") as mock_extractor:
        mock_extractor.return_value = {
            "final_answer": [{"text": "Adicionar 3 ovos"}]
        }
        
        payload = {
            "user_message": "",
            "image_b64": valid_image_b64
        }
        
        response = client.post("/bot/image_message", json=payload)
        
        assert response.status_code == 200
        bot_response = BotResponse.model_validate(response.json())
        
        assert bot_response.user_message == "Adicionar 3 ovos"


def test_process_image_message_database_insertion(client, db_session, valid_image_b64):
    """Testa se a mensagem processada da imagem foi realmente inserida no banco de dados (usando serviços reais)"""
    payload = {
        "user_message": "",
        "image_b64": valid_image_b64
    }
    
    # Conta quantos registros existem antes
    response = client.get("/api/items")
    assert response.status_code == 200
    items = [ItemResponse.model_validate(item) for item in response.json()]
    
    count = len(items)

    response = client.post("/bot/image_message", json=payload)
    
    assert response.status_code == 200
    bot_response = BotResponse.model_validate(response.json())
    print(bot_response.user_message)
    print(bot_response.ai_message)
    # Verificação
    response = client.get("/api/items")
    assert response.status_code == 200
    items = [ItemResponse.model_validate(item) for item in response.json()]
    
    assert count < len(items)
    


# ==================== TESTES PARA /bot/audio_message ====================

def test_process_audio_message_success(client, valid_audio_b64, mock_audio_extractor, mock_graph):
    """Testa o processamento bem-sucedido de uma mensagem com áudio"""
    payload = {
        "user_message": "",
        "audio_b64": valid_audio_b64
    }
    
    response = client.post("/bot/audio_message", json=payload)
    
    assert response.status_code == 200
    bot_response = BotResponse.model_validate(response.json())
    
    assert bot_response.id is not None
    assert bot_response.thread_id is not None
    assert bot_response.user_message == "Cadastrar receita de bolo de chocolate"
    assert bot_response.ai_message == "Operação realizada com sucesso"
    
    # Verifica se o extrator foi chamado com o áudio
    mock_audio_extractor.assert_called_once_with(valid_audio_b64)
    
    # Verifica se o grafo foi invocado
    mock_graph.invoke.assert_called_once()


def test_process_audio_message_with_thread_id(client, valid_audio_b64, mock_audio_extractor, mock_graph):
    """Testa o processamento de áudio com thread_id fornecido"""
    thread_id = "test-thread-audio-456"
    payload = {
        "user_message": "",
        "audio_b64": valid_audio_b64,
        "thread_id": thread_id
    }
    
    response = client.post("/bot/audio_message", json=payload)
    
    assert response.status_code == 200
    bot_response = BotResponse.model_validate(response.json())
    
    assert bot_response.thread_id == thread_id


def test_process_audio_message_invalid_base64(client):
    """Testa o processamento de áudio com base64 inválido"""
    payload = {
        "user_message": "",
        "audio_b64": "invalid-base64-string!!!"
    }
    
    response = client.post("/bot/audio_message", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Áudio inválido"


def test_process_audio_message_missing_audio(client):
    """Testa o processamento sem áudio fornecido"""
    payload = {
        "user_message": ""
    }
    
    response = client.post("/bot/audio_message", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Áudio inválido"


def test_process_audio_message_empty_audio(client):
    """Testa o processamento com string de áudio vazia"""
    payload = {
        "user_message": "",
        "audio_b64": ""
    }
    
    response = client.post("/bot/audio_message", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Áudio inválido"


def test_process_audio_message_extractor_returns_empty(client, valid_audio_b64, mock_graph):
    """Testa quando o extrator retorna string vazia"""
    with patch("controllers.bot.audio_extractor") as mock_extractor:
        mock_extractor.return_value = {
            "final_answer": ""
        }
        
        payload = {
            "user_message": "",
            "audio_b64": valid_audio_b64
        }
        
        response = client.post("/bot/audio_message", json=payload)
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Áudio inválido"
        
        # Garante que o grafo NÃO foi invocado
        mock_graph.invoke.assert_not_called()


def test_process_audio_message_extractor_returns_list(client, valid_audio_b64):
    """Testa quando o extrator retorna uma lista com texto"""
    with patch("controllers.bot.audio_extractor") as mock_extractor:
        mock_extractor.return_value = {
            "final_answer": [{"text": "Remover 2 litros de leite"}]
        }
        
        payload = {
            "user_message": "",
            "audio_b64": valid_audio_b64
        }
        
        response = client.post("/bot/audio_message", json=payload)
        
        assert response.status_code == 200
        bot_response = BotResponse.model_validate(response.json())
        
        assert bot_response.user_message == "Remover 2 litros de leite"


# ==================== TESTES COMPARATIVOS E DE INTEGRAÇÃO ====================

def test_both_endpoints_generate_different_threads(client, valid_image_b64, valid_audio_b64, mock_optical_extractor, mock_audio_extractor, mock_graph):
    """Testa que cada endpoint gera threads diferentes quando não fornecido"""
    payload_image = {
        "user_message": "",
        "image_b64": valid_image_b64
    }
    
    payload_audio = {
        "user_message": "",
        "audio_b64": valid_audio_b64
    }
    
    response1 = client.post("/bot/image_message", json=payload_image)
    response2 = client.post("/bot/audio_message", json=payload_audio)
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    bot_response1 = BotResponse.model_validate(response1.json())
    bot_response2 = BotResponse.model_validate(response2.json())
    
    # Threads devem ser diferentes
    assert bot_response1.thread_id != bot_response2.thread_id


def test_image_and_audio_with_same_thread(client, valid_image_b64, valid_audio_b64, mock_optical_extractor, mock_audio_extractor, mock_graph):
    """Testa que mensagens de imagem e áudio podem compartilhar o mesmo thread"""
    thread_id = "shared-thread-789"
    
    payload_image = {
        "user_message": "",
        "image_b64": valid_image_b64,
        "thread_id": thread_id
    }
    
    payload_audio = {
        "user_message": "",
        "audio_b64": valid_audio_b64,
        "thread_id": thread_id
    }
    
    response1 = client.post("/bot/image_message", json=payload_image)
    response2 = client.post("/bot/audio_message", json=payload_audio)
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    bot_response1 = BotResponse.model_validate(response1.json())
    bot_response2 = BotResponse.model_validate(response2.json())
    
    # Threads devem ser iguais
    assert bot_response1.thread_id == thread_id
    assert bot_response2.thread_id == thread_id
