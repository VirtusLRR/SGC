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

