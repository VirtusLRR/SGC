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