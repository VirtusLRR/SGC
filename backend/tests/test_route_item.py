import pytest
from fastapi.testclient import TestClient
from index import app
from schemas import ItemResponse
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

@pytest.mark.parametrize(
    "payload",
    [
        {"name": "Notebook", "price": 1500.0, "measure_unity": "Unity", "amount": 10},
        {"name": "Mouse", "price": 30.50, "measure_unity": "Unity", "amount": 10},
    ]
)
def test_create_item(client, payload):
    response = client.post("/api/items", json=payload)

    assert response.status_code == 201

    item_response = ItemResponse.model_validate(response.json())

    assert item_response.name == payload["name"]
    assert item_response.price == payload["price"]
    assert item_response.measure_unity == payload["measure_unity"]
    assert item_response.amount == payload["amount"]
    assert item_response.id is not None

@pytest.mark.parametrize(
    "payload",
    [
        {"name": "Notebook", "price": 1500.0, "measure_unity": "Unity", "amount": 10},
        {"name": "Mouse", "price": 30.50, "measure_unity": "Unity", "amount": 10},
    ]
)
def test_update_item(client, payload):
    response = client.post("/api/items", json=payload)
    assert response.status_code == 201

    created_item = ItemResponse.model_validate(response.json())
    old_item_id = created_item.id

    created_item.name = "Notebook Acer"
    update_payload = created_item.model_dump()

    for key in ["create_at", "update_at", "expiration_date"]:
        if update_payload.get(key):
            update_payload[key] = update_payload[key].isoformat()

    ItemResponse.model_validate(update_payload)
    response = client.put(f"/api/items/{old_item_id}", json=update_payload)
    assert response.status_code == 200

    updated_item = ItemResponse.model_validate(response.json())
    assert updated_item.id == old_item_id
    assert updated_item.name == "Notebook Acer"
    assert updated_item.price == payload["price"]
    assert updated_item.measure_unity == payload["measure_unity"]
    assert updated_item.amount == payload["amount"]


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "Notebook", "price": 1500.0, "measure_unity": "Unity", "amount": 10},
        {"name": "Mouse", "price": 30.50, "measure_unity": "Unity", "amount": 10},
    ]
)
def test_delete_item(client, payload):
    response = client.post("/api/items", json=payload)
    assert response.status_code == 201

    created_item = ItemResponse.model_validate(response.json())

    response = client.get(f"/api/items/{created_item.id}")
    assert response.status_code == 200

    response = client.delete(f"/api/items/{created_item.id}")
    assert response.status_code == 204

    response = client.get(f"/api/items/{created_item.id}")
    assert response.status_code == 404


def test_get_all_items(client):
    payload = [
        {"name": "Notebook", "price": 1500.0, "measure_unity": "Unity", "amount": 10},
        {"name": "Mouse", "price": 30.50, "measure_unity": "Unity", "amount": 10},
    ]
    response_1 = client.post("/api/items", json=payload[0])
    assert response_1.status_code == 201
    response_2 = client.post("/api/items", json=payload[1])
    assert response_2.status_code == 201

    response = client.get("/api/items")
    assert response.status_code == 200

    items = [ItemResponse.model_validate(item) for item in response.json()]
    for i in range(len(payload)):
        assert items[i].name == payload[i]["name"]
        assert items[i].price == payload[i]["price"]
        assert items[i].measure_unity == payload[i]["measure_unity"]
        assert items[i].amount == payload[i]["amount"]
        assert items[i].id is not None


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "Notebook", "price": 1500.0, "measure_unity": "Unity", "amount": 10},
        {"name": "Mouse", "price": 30.50, "measure_unity": "Unity", "amount": 10},
    ]
)
def test_get_by_id(client, payload):
    response = client.post("/api/items", json=payload)
    assert response.status_code == 201

    inserted_item = ItemResponse.model_validate(response.json())

    response = client.get(f"/api/items/{inserted_item.id}")
    assert response.status_code == 200

    filtered_item = ItemResponse.model_validate(response.json())

    assert inserted_item.name == filtered_item.name
    assert inserted_item.price == filtered_item.price
    assert inserted_item.measure_unity == filtered_item.measure_unity
    assert inserted_item.amount == filtered_item.amount
    assert inserted_item.id is not None

@pytest.mark.parametrize(
    "payload",
    [
        {"name": "Notebook", "price": 1500.0, "measure_unity": "Unity", "amount": 10},
        {"name": "Mouse", "price": 30.50, "measure_unity": "Unity", "amount": 10},
    ]
)
def test_get_by_name(client, payload):
    response = client.post("/api/items", json=payload)
    assert response.status_code == 201

    inserted_item = ItemResponse.model_validate(response.json())

    response = client.get(f"/api/items", params={"name": inserted_item.name})
    assert response.status_code == 200

    filtered_items = [ItemResponse.model_validate(item) for item in response.json()]

    assert len(filtered_items) == 1

    filtered_item = filtered_items[0]

    assert inserted_item.name == filtered_item.name
    assert inserted_item.price == filtered_item.price
    assert inserted_item.measure_unity == filtered_item.measure_unity
    assert inserted_item.amount == filtered_item.amount
    assert inserted_item.id is not None

def test_delete_empty_item(client):
    response = client.delete("/api/items/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item não encontrado"


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "Notebook", "price": 1500.0, "measure_unity": "Unity", "amount": 10},
        {"name": "Mouse", "price": 30.50, "measure_unity": "Unity", "amount": 10},
    ]
)
def test_update_empty_item(client, payload):
    response = client.put("/api/items/1", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Item não encontrado"