import pytest
from fastapi.testclient import TestClient
from index import app
from schemas import RecipeResponse
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
        {
            "title": "Bolo de Fubá",
            "description": "Receita Típica de vovó",
            "steps": "Misture o fubá com leite e asse."
        },
        {
            "title": "Ovo Cozido",
            "description": None,
            "steps": "Cozinhe por 10 minutos."
        }
    ]
)
def test_create_recipe(client, payload):
    response = client.post("/api/recipes", json=payload)
    
    assert response.status_code == 201
    
    recipe = RecipeResponse.model_validate(response.json())
    
    assert recipe.title == payload["title"]
    assert recipe.steps == payload["steps"]
    assert recipe.id is not None
    
    if payload["description"]:
        assert recipe.description == payload["description"]
    else:
        assert recipe.description is None


def test_get_all_recipes(client):
    
    client.post("/api/recipes", json={"title": "R1", "steps": "..."})
    client.post("/api/recipes", json={"title": "R2", "steps": "..."})

    response = client.get("/api/recipes")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_find_by_id(client):
    
    create_res = client.post("/api/recipes", json={"title": "Torta", "steps": "..."})
    created_id = create_res.json()["id"]

    
    response = client.get(f"/api/recipes/{created_id}")
    
    assert response.status_code == 200
    assert response.json()["title"] == "Torta"


def test_find_by_id_not_found(client):

    response = client.get("/api/recipes/99999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Receita não encontrada"


def test_find_by_name(client):
    client.post("/api/recipes", json={"title": "Feijoada", "steps": "..."})
    
    response = client.get("/api/recipes", params={"title": "Feijoada"})
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Feijoada"


def test_update_recipe(client):
    
    create_res = client.post("/api/recipes", json={"title": "Pão", "steps": "Asse"})
    created_item = RecipeResponse.model_validate(create_res.json())

    
    created_item.title = "Pão Integral"
    payload = created_item.model_dump()
    
    response = client.put(f"/api/recipes/{created_item.id}", json=payload)
    
    assert response.status_code == 200
    assert response.json()["title"] == "Pão Integral"


def test_delete_recipe(client):
    
    create_res = client.post("/api/recipes", json={"title": "Apagar", "steps": "..."})
    item_id = create_res.json()["id"]

    
    response = client.delete(f"/api/recipes/{item_id}")
    assert response.status_code == 204

    
    response = client.get(f"/api/recipes/{item_id}")
    assert response.status_code == 404


def test_get_recipe_cost_structure(client):
    """
    Testa se a rota de custo retorna a estrutura correta (Dict),
    mesmo que o custo seja zero (pois não vinculamos ingredientes).
    """

    res = client.post("/api/recipes", json={"title": "Teste Custo", "steps": "..."})
    recipe_id = res.json()["id"]

    
    response = client.get(f"/recipes/cost/{recipe_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    
    assert "recipe_id" in data
    assert "total_cost" in data
    assert "ingredients" in data
    assert data["recipe_id"] == recipe_id
    assert data["total_cost"] == 0.0


def test_get_recipe_cost_not_found(client):
    response = client.get("/recipes/cost/99999")
    assert response.status_code == 404


def test_get_all_recipes_with_cost(client):
    client.post("/api/recipes", json={"title": "R3", "steps": "..."})
    
    response = client.get("/recipes/costs")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_feasible_recipes(client):
    response = client.get("/recipes/feasible")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_most_popular_ingredients(client):
    limit = 5
    response = client.get(f"/recipes/popular-ingredients/{limit}")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_recipe_with_items(client):
    """Testa a criação de uma receita com itens (recipe_itens)."""
    # Primeiro, cria os itens que serão usados na receita
    item1 = client.post("/api/items", json={
        "name": "Farinha",
        "price": 5.00,
        "price_unit": "quilograma",
        "measure_unity": "grama",
        "amount": 1000
    })
    item1_id = item1.json()["id"]
    
    item2 = client.post("/api/items", json={
        "name": "Açúcar",
        "price": 4.00,
        "price_unit": "quilograma",
        "measure_unity": "grama",
        "amount": 1000
    })
    item2_id = item2.json()["id"]
    
    # Cria a receita com os itens
    payload = {
        "title": "Bolo Simples",
        "description": "Bolo básico",
        "steps": "Misture tudo e asse",
        "recipe_itens": [
            {"item_id": item1_id, "amount": 500.0},
            {"item_id": item2_id, "amount": 200.0}
        ]
    }
    
    response = client.post("/api/recipes", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    
    # Verifica os dados da receita
    assert data["title"] == "Bolo Simples"
    assert data["id"] is not None
    
    # Verifica os itens da receita
    assert "recipe_itens" in data
    assert len(data["recipe_itens"]) == 2
    
    # Verifica que os recipe_itens contêm recipe_id (Response)
    for recipe_item in data["recipe_itens"]:
        assert "recipe_id" in recipe_item
        assert recipe_item["recipe_id"] == data["id"]
        assert "item_id" in recipe_item
        assert "amount" in recipe_item


def test_create_recipe_without_items(client):
    """Testa que é possível criar uma receita sem itens."""
    payload = {
        "title": "Receita Vazia",
        "steps": "Sem ingredientes",
        "recipe_itens": []
    }
    
    response = client.post("/api/recipes", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Receita Vazia"
    assert data["recipe_itens"] == []


def test_update_recipe_with_items(client):
    """Testa a atualização de uma receita incluindo novos itens."""
    # Cria itens
    item1 = client.post("/api/items", json={
        "name": "Ovo",
        "price": 0.80,
        "price_unit": "unidade",
        "measure_unity": "unidade",
        "amount": 12
    })
    item1_id = item1.json()["id"]
    
    item2 = client.post("/api/items", json={
        "name": "Leite",
        "price": 5.00,
        "price_unit": "litro",
        "measure_unity": "mililitro",
        "amount": 1000
    })
    item2_id = item2.json()["id"]
    
    # Cria receita inicial sem itens
    create_res = client.post("/api/recipes", json={
        "title": "Omelete",
        "steps": "Bata os ovos"
    })
    recipe_id = create_res.json()["id"]
    
    # Atualiza a receita adicionando itens
    update_payload = {
        "title": "Omelete Completa",
        "steps": "Bata os ovos com leite",
        "recipe_itens": [
            {"item_id": item1_id, "amount": 3.0},
            {"item_id": item2_id, "amount": 100.0}
        ]
    }
    
    response = client.put(f"/api/recipes/{recipe_id}", json=update_payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["title"] == "Omelete Completa"
    assert len(data["recipe_itens"]) == 2
    
    # Verifica que todos os items têm recipe_id
    for recipe_item in data["recipe_itens"]:
        assert recipe_item["recipe_id"] == recipe_id
        assert recipe_item["item_id"] in [item1_id, item2_id]


def test_get_recipe_with_items_by_id(client):
    """Testa que ao buscar uma receita por ID, os itens são retornados corretamente."""
    # Cria item e receita
    item = client.post("/api/items", json={
        "name": "Café",
        "price": 20.00,
        "price_unit": "quilograma",
        "measure_unity": "grama",
        "amount": 500
    })
    item_id = item.json()["id"]
    
    create_res = client.post("/api/recipes", json={
        "title": "Café Simples",
        "steps": "Passe o café",
        "recipe_itens": [{"item_id": item_id, "amount": 50.0}]
    })
    recipe_id = create_res.json()["id"]
    
    # Busca a receita
    response = client.get(f"/api/recipes/{recipe_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["title"] == "Café Simples"
    assert len(data["recipe_itens"]) == 1
    assert data["recipe_itens"][0]["recipe_id"] == recipe_id
    assert data["recipe_itens"][0]["item_id"] == item_id
    assert data["recipe_itens"][0]["amount"] == 50.0


def test_recipe_cost_with_items(client):
    """Testa o cálculo de custo de uma receita com itens."""
    # Cria itens com preços conhecidos
    item1 = client.post("/api/items", json={
        "name": "Tomate",
        "price": 10.00,
        "price_unit": "quilograma",
        "measure_unity": "grama",
        "amount": 2000
    })
    item1_id = item1.json()["id"]
    
    # Cria receita usando 500g de tomate (custo esperado: 5.00)
    recipe_res = client.post("/api/recipes", json={
        "title": "Molho de Tomate",
        "steps": "Cozinhe os tomates",
        "recipe_itens": [{"item_id": item1_id, "amount": 500.0}]
    })
    recipe_id = recipe_res.json()["id"]
    
    # Busca o custo
    response = client.get(f"/recipes/cost/{recipe_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["recipe_id"] == recipe_id
    assert data["total_cost"] == 5.0
    assert len(data["ingredients"]) == 1
    assert data["ingredients"][0]["item_id"] == item1_id
    assert data["ingredients"][0]["required_amount"] == 500.0