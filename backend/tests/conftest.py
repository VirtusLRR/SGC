import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
from datetime import datetime, timedelta

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from models import Item, Recipe, RecipeItem

from database.database import Base

@pytest.fixture(scope="function")
def db_session():
    
    engine = create_engine("sqlite:///tests/test.db", echo=False)
    
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )


    db = TestingSessionLocal()
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        yield db  
    finally:
        db.close()


@pytest.fixture(scope="function")
def populated_db_session(db_session):
    items = [
        Item(
            name="banana nanica",
            measure_unity="unidade",
            amount=12,
            description="bananas nanicas maduras",
            price=0.50,
            expiration_date=datetime.now().date() + timedelta(days=5)
        ),
        Item(
            name="doce de leite",
            measure_unity="grama",
            amount=800,
            description="doce de leite cremoso",
            price=15.00,
            expiration_date=datetime.now().date() + timedelta(days=180)
        ),
        Item(
            name="biscoito maisena",
            measure_unity="grama",
            amount=400,
            description="biscoito tipo maisena triturado",
            price=5.00,
            expiration_date=datetime.now().date() + timedelta(days=90)
        ),
        Item(
            name="manteiga",
            measure_unity="grama",
            amount=200,
            description="manteiga sem sal",
            price=8.00,
            expiration_date=datetime.now().date() + timedelta(days=30)
        ),
        Item(
            name="creme de leite",
            measure_unity="mililitro",
            amount=1000,
            description="creme de leite fresco",
            price=6.00,
            expiration_date=datetime.now().date() + timedelta(days=15)
        ),
        Item(
            name="açúcar",
            measure_unity="grama",
            amount=2000,
            description="açúcar refinado",
            price=4.50,
            expiration_date=datetime.now().date() + timedelta(days=365)
        ),
        Item(
            name="leite condensado",
            measure_unity="grama",
            amount=800,
            description="leite condensado",
            price=7.00,
            expiration_date=datetime.now().date() + timedelta(days=180)
        ),
        Item(
            name="leite",
            measure_unity="mililitro",
            amount=2000,
            description="leite integral",
            price=5.00,
            expiration_date=datetime.now().date() + timedelta(days=7)
        ),
        Item(
            name="amido de milho",
            measure_unity="grama",
            amount=500,
            description="amido de milho (maisena)",
            price=4.00,
            expiration_date=datetime.now().date() + timedelta(days=365)
        ),
        Item(
            name="gema de ovo",
            measure_unity="unidade",
            amount=12,
            description="gemas de ovos",
            price=0.60,
            expiration_date=datetime.now().date() + timedelta(days=7)
        ),
        Item(
            name="biscoito champanhe",
            measure_unity="grama",
            amount=300,
            description="biscoito tipo champanhe",
            price=6.00,
            expiration_date=datetime.now().date() + timedelta(days=90)
        ),
        Item(
            name="chocolate em pó",
            measure_unity="grama",
            amount=400,
            description="chocolate em pó ou cacau",
            price=8.00,
            expiration_date=datetime.now().date() + timedelta(days=365)
        ),
        Item(
            name="canela em pó",
            measure_unity="grama",
            amount=100,
            description="canela em pó",
            price=3.50,
            expiration_date=datetime.now().date() + timedelta(days=365)
        ),
        Item(
            name="nozes",
            measure_unity="grama",
            amount=300,
            description="nozes",
            price=15.00,
            expiration_date=datetime.now().date() + timedelta(days=90)
        ),
        Item(
            name="farinha de trigo",
            measure_unity="grama",
            amount=1000,
            description="farinha de trigo",
            price=5.00,
            expiration_date=datetime.now().date() + timedelta(days=365)
        ),
        Item(
            name="extrato de baunilha",
            measure_unity="mililitro",
            amount=50,
            description="extrato de baunilha",
            price=12.00,
            expiration_date=datetime.now().date() + timedelta(days=365)
        ),
        Item(
            name="limão",
            measure_unity="unidade",
            amount=5,
            description="limões",
            price=0.80,
            expiration_date=datetime.now().date() + timedelta(days=7)
        ),
    ]

    db_session.add_all(items)
    db_session.commit()

    for item in items:
        db_session.refresh(item)

    recipe1 = Recipe(
        title="torta banoffee",
        description="torta clássica inglesa com banana e doce de leite",
        steps="""1. em uma tigela, misture o biscoito triturado com a manteiga derretida até formar uma farofa úmida.
2. forre o fundo e as laterais de uma forma de fundo removível (cerca de 22 cm de diâmetro), pressionando bem. leve à geladeira por 30 minutos.
3. espalhe o doce de leite de maneira uniforme sobre a base de biscoito já firme.
4. distribua as rodelas de banana sobre o doce de leite, cobrindo toda a superfície.
5. na batedeira, bata o creme de leite fresco com o açúcar até atingir o ponto de chantilly (picos firmes).
6. cubra a torta com o chantilly. decore com raspas de chocolate ou polvilhe cacau em pó.
7. mantenha na geladeira até a hora de servir."""
    )

    recipe2 = Recipe(
        title="pavê de banana com doce de leite",
        description="sobremesa cremosa em camadas com banana e doce de leite",
        steps="""1. em uma panela, dissolva o amido de milho no leite. adicione o leite condensado e as gemas.
2. leve ao fogo médio, mexendo sempre, até engrossar e formar um creme. deixe esfriar.
3. em um refratário, comece com uma camada do creme frio.
4. umedeça os biscoitos no leite e faça uma camada sobre o creme.
5. cubra os biscoitos com uma camada generosa de doce de leite e, por cima, distribua as fatias de banana.
6. repita as camadas, finalizando com o creme.
7. leve à geladeira por no mínimo 4 horas antes de servir.
8. se desejar, decore com mais bananas ou canela em pó."""
    )

    recipe3 = Recipe(
        title="brigadeiro de banana com doce de leite",
        description="brigadeiro cremoso com sabor de banana e doce de leite",
        steps="""1. em uma panela, misture o leite condensado com o doce de leite.
2. adicione as bananas amassadas e leve ao fogo médio.
3. mexa sem parar até desgrudar do fundo da panela.
4. despeje em um refratário untado com manteiga e deixe esfriar.
5. com as mãos untadas com manteiga, modele os brigadeiros.
6. passe no chocolate em pó ou em pedacinhos de banana desidratada.
7. sirva em forminhas de papel."""
    )

    db_session.add_all([recipe1, recipe2, recipe3])
    db_session.commit()

    db_session.refresh(recipe1)
    db_session.refresh(recipe2)
    db_session.refresh(recipe3)

    recipe1_items = [
        RecipeItem(recipe_id=recipe1.id, item_id=items[0].id, amount=4),
        RecipeItem(recipe_id=recipe1.id, item_id=items[1].id, amount=400),
        RecipeItem(recipe_id=recipe1.id, item_id=items[2].id, amount=200),
        RecipeItem(recipe_id=recipe1.id, item_id=items[3].id, amount=100),
        RecipeItem(recipe_id=recipe1.id, item_id=items[4].id, amount=500),
        RecipeItem(recipe_id=recipe1.id, item_id=items[5].id, amount=80),
        RecipeItem(recipe_id=recipe1.id, item_id=items[11].id, amount=30),
    ]

    recipe2_items = [
        RecipeItem(recipe_id=recipe2.id, item_id=items[0].id, amount=4),
        RecipeItem(recipe_id=recipe2.id, item_id=items[1].id, amount=400),
        RecipeItem(recipe_id=recipe2.id, item_id=items[6].id, amount=395),
        RecipeItem(recipe_id=recipe2.id, item_id=items[7].id, amount=480),
        RecipeItem(recipe_id=recipe2.id, item_id=items[8].id, amount=30),
        RecipeItem(recipe_id=recipe2.id, item_id=items[9].id, amount=2),
        RecipeItem(recipe_id=recipe2.id, item_id=items[10].id, amount=200),
        RecipeItem(recipe_id=recipe2.id, item_id=items[12].id, amount=5),
    ]

    recipe3_items = [
        RecipeItem(recipe_id=recipe3.id, item_id=items[0].id, amount=3),
        RecipeItem(recipe_id=recipe3.id, item_id=items[1].id, amount=200),
        RecipeItem(recipe_id=recipe3.id, item_id=items[6].id, amount=395),
        RecipeItem(recipe_id=recipe3.id, item_id=items[3].id, amount=20),
        RecipeItem(recipe_id=recipe3.id, item_id=items[11].id, amount=100),
    ]

    all_recipe_items = recipe1_items + recipe2_items + recipe3_items
    db_session.add_all(all_recipe_items)
    db_session.commit()

    yield db_session