from models.receita import Receita
from models.item import Item
from models.receita_item import ReceitaItem
from tests.conftest import db_session 

def test_insert_item(db_session):
    
    farinha = Item(
        name="Farinha",
        measure_unity="g",
        amount=1000,
        description="Farinha de trigo"
    )

    db_session.add(farinha)
    db_session.commit()

    assert farinha.id is not None
    
    item = db_session.query(Item).filter_by(name="Farinha").first()
    assert item.name == farinha.name

def test_insert_receita(db_session):

    receita = Receita(
        title="Bolo simples",
        steps="Misture tudo e asse",
        description="Bolo básico"
    )

    db_session.add(receita)
    db_session.commit()

    assert receita.id is not None

    obj = db_session.query(Receita).filter_by(title="Bolo simples").first()
    assert obj.title == receita.title
    
def test_insert_receita_item(db_session):

    farinha = Item(
        name="Farinha",
        measure_unity="g",
        amount=1000,
        description="Farinha de trigo"
    )

    receita = Receita(
        title="Bolo simples",
        steps="Misture tudo e asse",
        description="Bolo básico"
    )

    db_session.add(farinha)
    db_session.commit()

    receita.receita_itens.append(
        ReceitaItem(item=farinha, amount=200)
    )

    db_session.add(receita)
    db_session.commit()

    assert receita.id is not None
    assert farinha.id is not None
    assert len(receita.receita_itens) == 1

    itens_name = [ri.item.name for ri in farinha.receita_itens]
    assert "Farinha" in itens_name
    
    amount = {ri.item.name: ri.amount for ri in farinha.receita_itens}
    assert amount["Farinha"] == 200

    obj = db_session.query(Receita).filter_by(title="Bolo simples").first()
    assert obj.title == receita.title