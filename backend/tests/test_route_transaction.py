import pytest
from fastapi.testclient import TestClient
from index import app
from schemas import TransactionResponse, ItemResponse
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
def sample_item(client):
    item_payload = {
        "name": "Açúcar",
        "measure_unity": "grama",
        "amount": 1000,
        "description": "Açúcar refinado",
        "price": 5.00,
        "price_unit": "kg"
    }
    response = client.post("/api/items", json=item_payload)
    assert response.status_code == 201
    return ItemResponse.model_validate(response.json())


@pytest.mark.parametrize(
    "payload",
    [
        {
            "order_type": "compra",
            "description": "Compra de açúcar",
            "amount": 500.0,
            "price": 10.50
        },
        {
            "order_type": "venda",
            "description": "Venda de açúcar",
            "amount": 100.0,
            "price": 15.00
        },
        {
            "order_type": "ajuste",
            "description": "Ajuste de estoque",
            "amount": 50.0,
            "price": 0.0
        }
    ]
)
def test_create_transaction(client, sample_item, payload):
    payload["item_id"] = sample_item.id
    response = client.post("/api/transactions", json=payload)

    assert response.status_code == 201

    transaction_response = TransactionResponse.model_validate(response.json())

    assert transaction_response.item_id == payload["item_id"]
    assert transaction_response.order_type == payload["order_type"]
    assert transaction_response.description == payload["description"]
    assert transaction_response.amount == payload["amount"]
    assert transaction_response.price == payload["price"]
    assert transaction_response.id is not None


@pytest.mark.parametrize(
    "payload",
    [
        {
            "order_type": "compra",
            "description": "Compra sem item_id",
            "amount": 500.0,
            "price": 10.50
        }
    ]
)
def test_create_transaction_missing_mandatory_args(client, payload):
    response = client.post("/api/transactions", json=payload)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "payload",
    [
        {
            "item_id": 999,
            "order_type": "compra",
            "description": "Compra com item inexistente",
            "amount": 500.0,
            "price": 10.50
        }
    ]
)
def test_create_transaction_with_non_existent_item(client, payload):
    response = client.post("/api/transactions", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Item não encontrado"


@pytest.mark.parametrize(
    "payload",
    [
        {
            "order_type": "",
            "description": "Compra com tipo vazio",
            "amount": 500.0,
            "price": 10.50
        },
        {
            "order_type": "compra",
            "description": "",
            "amount": 500.0,
            "price": 10.50
        }
    ]
)
def test_create_transaction_with_empty_mandatory_args(client, sample_item, payload):
    payload["item_id"] = sample_item.id
    response = client.post("/api/transactions", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Campo obrigatório vazio"


@pytest.mark.parametrize(
    "payload",
    [
        {
            "order_type": "compra",
            "description": "Compra com preço negativo",
            "amount": 500.0,
            "price": -10.50
        }
    ]
)
def test_create_transaction_illegal_price(client, sample_item, payload):
    payload["item_id"] = sample_item.id
    response = client.post("/api/transactions", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "O preço não pode ser negativo"


@pytest.mark.parametrize(
    "payload",
    [
        {
            "order_type": "compra",
            "description": "Compra com quantidade negativa",
            "amount": -100.0,
            "price": 10.50
        },
        {
            "order_type": "compra",
            "description": "Compra com quantidade zero",
            "amount": 0.0,
            "price": 10.50
        }
    ]
)
def test_create_transaction_illegal_amount(client, sample_item, payload):
    payload["item_id"] = sample_item.id
    response = client.post("/api/transactions", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "A quantidade deve ser maior que zero"


def test_get_all_transactions(client, sample_item):
    transactions_data = [
        {
            "item_id": sample_item.id,
            "order_type": "compra",
            "description": "Primeira compra",
            "amount": 500.0,
            "price": 10.50
        },
        {
            "item_id": sample_item.id,
            "order_type": "venda",
            "description": "Primeira venda",
            "amount": 100.0,
            "price": 15.00
        }
    ]

    created_transactions = []
    for transaction_data in transactions_data:
        response = client.post("/api/transactions", json=transaction_data)
        assert response.status_code == 201
        created_transactions.append(TransactionResponse.model_validate(response.json()))

    response = client.get("/api/transactions")
    assert response.status_code == 200

    transactions = [TransactionResponse.model_validate(t) for t in response.json()]
    assert len(transactions) >= 2


def test_get_transaction_by_id(client, sample_item):
    transaction_data = {
        "item_id": sample_item.id,
        "order_type": "compra",
        "description": "Compra para teste de busca por ID",
        "amount": 300.0,
        "price": 12.00
    }

    response = client.post("/api/transactions", json=transaction_data)
    assert response.status_code == 201
    created_transaction = TransactionResponse.model_validate(response.json())

    response = client.get(f"/api/transactions/{created_transaction.id}")
    assert response.status_code == 200

    found_transaction = TransactionResponse.model_validate(response.json())
    assert found_transaction.id == created_transaction.id
    assert found_transaction.description == transaction_data["description"]


def test_get_transaction_by_item_id(client, sample_item):
    transactions_data = [
        {
            "item_id": sample_item.id,
            "order_type": "compra",
            "description": "Compra 1",
            "amount": 500.0,
            "price": 10.50
        },
        {
            "item_id": sample_item.id,
            "order_type": "compra",
            "description": "Compra 2",
            "amount": 300.0,
            "price": 11.00
        }
    ]

    for transaction_data in transactions_data:
        response = client.post("/api/transactions", json=transaction_data)
        assert response.status_code == 201

    response = client.get(f"/api/transactions?item_id={sample_item.id}")
    assert response.status_code == 200

    transactions = [TransactionResponse.model_validate(t) for t in response.json()]
    assert len(transactions) >= 2
    assert all(t.item_id == sample_item.id for t in transactions)


def test_update_transaction(client, sample_item):
    transaction_data = {
        "item_id": sample_item.id,
        "order_type": "compra",
        "description": "Compra inicial",
        "amount": 500.0,
        "price": 10.50
    }

    response = client.post("/api/transactions", json=transaction_data)
    assert response.status_code == 201
    created_transaction = TransactionResponse.model_validate(response.json())

    update_data = {
        "item_id": sample_item.id,
        "order_type": "compra",
        "description": "Compra atualizada",
        "amount": 600.0,
        "price": 12.00
    }

    response = client.put(f"/api/transactions/{created_transaction.id}", json=update_data)
    assert response.status_code == 200

    updated_transaction = TransactionResponse.model_validate(response.json())
    assert updated_transaction.description == "Compra atualizada"
    assert updated_transaction.amount == 600.0
    assert updated_transaction.price == 12.00


def test_delete_transaction(client, sample_item):
    transaction_data = {
        "item_id": sample_item.id,
        "order_type": "compra",
        "description": "Compra para deletar",
        "amount": 500.0,
        "price": 10.50
    }

    response = client.post("/api/transactions", json=transaction_data)
    assert response.status_code == 201
    created_transaction = TransactionResponse.model_validate(response.json())

    response = client.delete(f"/api/transactions/{created_transaction.id}")
    assert response.status_code == 204

    response = client.get(f"/api/transactions/{created_transaction.id}")
    assert response.status_code == 404


def test_get_non_existent_transaction(client):
    response = client.get("/api/transactions/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Transação não encontrada"


def test_update_non_existent_transaction(client, sample_item):
    update_data = {
        "item_id": sample_item.id,
        "order_type": "compra",
        "description": "Tentativa de atualizar inexistente",
        "amount": 500.0,
        "price": 10.50
    }

    response = client.put("/api/transactions/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Transação não encontrada"


def test_delete_non_existent_transaction(client):
    response = client.delete("/api/transactions/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Transação não encontrada"


def test_get_transaction_summary(client, sample_item):
    from datetime import datetime, timedelta

    transactions_data = [
        {
            "item_id": sample_item.id,
            "order_type": "entrada",
            "description": "Compra de açúcar",
            "amount": 1000.0,
            "price": 5.00
        },
        {
            "item_id": sample_item.id,
            "order_type": "saída",
            "description": "Uso em receita",
            "amount": 200.0,
            "price": None
        }
    ]

    for transaction_data in transactions_data:
        response = client.post("/api/transactions", json=transaction_data)
        assert response.status_code == 201

    response = client.get("/transactions/summary/30")
    assert response.status_code == 200

    summary = response.json()
    assert "period" in summary
    assert "entries" in summary
    assert "exits" in summary
    assert "balance" in summary
    assert summary["entries"]["count"] >= 1
    assert summary["exits"]["count"] >= 1


def test_get_most_transacted_items(client, sample_item):
    transactions_data = [
        {
            "item_id": sample_item.id,
            "order_type": "entrada",
            "description": "Compra 1",
            "amount": 500.0,
            "price": 5.00
        },
        {
            "item_id": sample_item.id,
            "order_type": "entrada",
            "description": "Compra 2",
            "amount": 300.0,
            "price": 5.50
        },
        {
            "item_id": sample_item.id,
            "order_type": "saída",
            "description": "Venda 1",
            "amount": 100.0,
            "price": 8.00
        }
    ]

    for transaction_data in transactions_data:
        response = client.post("/api/transactions", json=transaction_data)
        assert response.status_code == 201

    response = client.get("/transactions/most-transacted/10/entrada")
    assert response.status_code == 200

    items = response.json()
    assert len(items) >= 1
    assert "transaction_count" in items[0]
    assert "total_amount" in items[0]
    assert "total_value" in items[0]


def test_get_daily_transactions(client, sample_item):
    transactions_data = [
        {
            "item_id": sample_item.id,
            "order_type": "entrada",
            "description": "Compra diária 1",
            "amount": 500.0,
            "price": 5.00
        },
        {
            "item_id": sample_item.id,
            "order_type": "saída",
            "description": "Saída diária 1",
            "amount": 100.0,
            "price": None
        }
    ]

    for transaction_data in transactions_data:
        response = client.post("/api/transactions", json=transaction_data)
        assert response.status_code == 201

    response = client.get("/transactions/daily/30")
    assert response.status_code == 200

    daily_data = response.json()
    assert len(daily_data) >= 1
    assert "date" in daily_data[0]
    assert "order_type" in daily_data[0]
    assert "count" in daily_data[0]
    assert "total_amount" in daily_data[0]


def test_get_consumption_rate(client, sample_item):
    transactions_data = [
        {
            "item_id": sample_item.id,
            "order_type": "saída",
            "description": "Consumo 1",
            "amount": 200.0,
            "price": None
        },
        {
            "item_id": sample_item.id,
            "order_type": "saída",
            "description": "Consumo 2",
            "amount": 150.0,
            "price": None
        }
    ]

    for transaction_data in transactions_data:
        response = client.post("/api/transactions", json=transaction_data)
        assert response.status_code == 201

    response = client.get("/transactions/consumption-rate/30")
    assert response.status_code == 200

    consumption_data = response.json()
    assert len(consumption_data) >= 1
    assert "current_stock" in consumption_data[0]
    assert "total_consumed" in consumption_data[0]
    assert "daily_average" in consumption_data[0]


def test_get_price_analysis(client, sample_item):
    transactions_data = [
        {
            "item_id": sample_item.id,
            "order_type": "entrada",
            "description": "Compra 1",
            "amount": 500.0,
            "price": 5.00
        },
        {
            "item_id": sample_item.id,
            "order_type": "entrada",
            "description": "Compra 2",
            "amount": 500.0,
            "price": 5.50
        },
        {
            "item_id": sample_item.id,
            "order_type": "entrada",
            "description": "Compra 3",
            "amount": 500.0,
            "price": 4.80
        }
    ]

    for transaction_data in transactions_data:
        response = client.post("/api/transactions", json=transaction_data)
        assert response.status_code == 201

    response = client.get("/transactions/price-analysis")
    assert response.status_code == 200

    price_data = response.json()
    assert len(price_data) >= 1
    assert "avg_price" in price_data[0]
    assert "min_price" in price_data[0]
    assert "max_price" in price_data[0]
    assert "transaction_count" in price_data[0]