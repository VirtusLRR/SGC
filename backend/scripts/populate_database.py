import sys
from pathlib import Path
from datetime import datetime, timedelta

backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from database.database import SessionLocal, engine, Base
from models.item import Item
from models.recipe import Recipe
from models.recipe_item import RecipeItem
from models.bot import Bot
from models.transaction import Transaction


def populate_database():
    """
    Popula o banco de dados com dados de teste incluindo itens, receitas,
    vínculos de ingredientes, conversas do bot e transações
    """

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print("Criando itens...")
        items = [
            Item(
                name="banana nanica",
                measure_unity="unidade",
                amount=12,
                description="bananas nanicas maduras",
                price=0.50,
                price_unit="unidade",
                expiration_date=datetime.now().date() + timedelta(days=5)
            ),
            Item(
                name="doce de leite",
                measure_unity="grama",
                amount=800,
                description="doce de leite cremoso",
                price=15.00,
                price_unit="kg",
                expiration_date=datetime.now().date() + timedelta(days=180)
            ),
            Item(
                name="biscoito maisena",
                measure_unity="grama",
                amount=400,
                description="biscoito tipo maisena triturado",
                price=10.00,
                price_unit="kg",
                expiration_date=datetime.now().date() + timedelta(days=90)
            ),
            Item(
                name="manteiga",
                measure_unity="grama",
                amount=200,
                description="manteiga sem sal",
                price=40.00,
                price_unit="kg",
                expiration_date=datetime.now().date() + timedelta(days=30)
            ),
            Item(
                name="creme de leite",
                measure_unity="mililitro",
                amount=1000,
                description="creme de leite fresco",
                price=6.00,
                price_unit="litro",
                expiration_date=datetime.now().date() + timedelta(days=15)
            ),
            Item(
                name="açúcar",
                measure_unity="grama",
                amount=2000,
                description="açúcar refinado",
                price=4.50,
                price_unit="kg",
                expiration_date=datetime.now().date() + timedelta(days=365)
            ),
            Item(
                name="leite condensado",
                measure_unity="grama",
                amount=800,
                description="leite condensado",
                price=7.00,
                price_unit="kg",
                expiration_date=datetime.now().date() + timedelta(days=180)
            ),
            Item(
                name="leite",
                measure_unity="mililitro",
                amount=2000,
                description="leite integral",
                price=5.00,
                price_unit="litro",
                expiration_date=datetime.now().date() + timedelta(days=7)
            ),
            Item(
                name="amido de milho",
                measure_unity="grama",
                amount=500,
                description="amido de milho (maisena)",
                price=8.00,
                price_unit="kg",
                expiration_date=datetime.now().date() + timedelta(days=365)
            ),
            Item(
                name="gema de ovo",
                measure_unity="unidade",
                amount=12,
                description="gemas de ovos",
                price=0.60,
                price_unit="unidade",
                expiration_date=datetime.now().date() + timedelta(days=7)
            ),
            Item(
                name="biscoito champanhe",
                measure_unity="grama",
                amount=300,
                description="biscoito tipo champanhe",
                price=20.00,
                price_unit="kg",
                expiration_date=datetime.now().date() + timedelta(days=90)
            ),
            Item(
                name="chocolate em pó",
                measure_unity="grama",
                amount=400,
                description="chocolate em pó ou cacau",
                price=40.00,
                price_unit="kg",
                expiration_date=datetime.now().date() + timedelta(days=365)
            ),
            Item(
                name="canela em pó",
                measure_unity="grama",
                amount=100,
                description="canela em pó",
                price=35.00,
                price_unit="kg",
                expiration_date=datetime.now().date() + timedelta(days=365)
            ),
            Item(
                name="nozes",
                measure_unity="grama",
                amount=300,
                description="nozes",
                price=50.00,
                price_unit="kg",
                expiration_date=datetime.now().date() + timedelta(days=90)
            ),
            Item(
                name="farinha de trigo",
                measure_unity="grama",
                amount=1000,
                description="farinha de trigo",
                price=5.00,
                price_unit="kg",
                expiration_date=datetime.now().date() + timedelta(days=365)
            ),
            Item(
                name="extrato de baunilha",
                measure_unity="mililitro",
                amount=50,
                description="extrato de baunilha",
                price=240.00,
                price_unit="litro",
                expiration_date=datetime.now().date() + timedelta(days=365)
            ),
            Item(
                name="limão",
                measure_unity="unidade",
                amount=5,
                description="limões",
                price=0.80,
                price_unit="unidade",
                expiration_date=datetime.now().date() + timedelta(days=7)
            ),
        ]
        db.add_all(items)
        db.commit()
        for item in items:
            db.refresh(item)
        print(f"{len(items)} itens criados!")

        print("\nCriando receitas...")
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

        recipe4 = Recipe(
            title="risoto de camarão",
            description="risoto cremoso com camarões frescos e vinho branco",
            steps="""1. em uma panela, aqueça o azeite e refogue a cebola até ficar transparente.
2. adicione o alho e refogue por mais 1 minuto.
3. acrescente o arroz arbóreo e mexa bem até os grãos ficarem nacarados.
4. adicione o vinho branco e deixe evaporar.
5. aos poucos, adicione o caldo quente, mexendo sempre até o arroz absorver o líquido.
6. quando o arroz estiver quase pronto, adicione os camarões limpos.
7. finalize com manteiga, queijo parmesão ralado e salsinha picada.
8. sirva imediatamente."""
        )

        db.add_all([recipe1, recipe2, recipe3, recipe4])
        db.commit()

        db.refresh(recipe1)
        db.refresh(recipe2)
        db.refresh(recipe3)
        db.refresh(recipe4)

        print(f"4 receitas criadas!")

        print("\nCriando ingredientes para risoto (indisponíveis)...")

        risoto_items = [
            Item(
                name="arroz arbóreo",
                measure_unity="grama",
                amount=0,
                description="arroz para risoto",
                price=12.00,
                price_unit="kg",
                expiration_date=datetime.now().date() + timedelta(days=365)
            ),
            Item(
                name="camarão",
                measure_unity="grama",
                amount=0,
                description="camarões limpos e frescos",
                price=60.00,
                price_unit="kg",
                expiration_date=datetime.now().date() + timedelta(days=3)
            ),
            Item(
                name="vinho branco",
                measure_unity="mililitro",
                amount=0,
                description="vinho branco seco para culinária",
                price=25.00,
                price_unit="litro",
                expiration_date=datetime.now().date() + timedelta(days=730)
            ),
            Item(
                name="caldo de legumes",
                measure_unity="mililitro",
                amount=0,
                description="caldo de legumes caseiro",
                price=8.00,
                price_unit="litro",
                expiration_date=datetime.now().date() + timedelta(days=5)
            ),
            Item(
                name="queijo parmesão",
                measure_unity="grama",
                amount=0,
                description="queijo parmesão ralado",
                price=80.00,
                price_unit="kg",
                expiration_date=datetime.now().date() + timedelta(days=30)
            ),
        ]

        db.add_all(risoto_items)
        db.commit()

        for item in risoto_items:
            db.refresh(item)

        items.extend(risoto_items)
        print(f"{len(risoto_items)} ingredientes do risoto criados (todos indisponíveis)!")

        print("\nVinculando ingredientes às receitas...")

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

        recipe4_items = [
            RecipeItem(recipe_id=recipe4.id, item_id=items[17].id, amount=300),
            RecipeItem(recipe_id=recipe4.id, item_id=items[18].id, amount=400),
            RecipeItem(recipe_id=recipe4.id, item_id=items[19].id, amount=150),
            RecipeItem(recipe_id=recipe4.id, item_id=items[20].id, amount=1000),
            RecipeItem(recipe_id=recipe4.id, item_id=items[21].id, amount=50),
            RecipeItem(recipe_id=recipe4.id, item_id=items[3].id, amount=30),
        ]

        all_recipe_items = recipe1_items + recipe2_items + recipe3_items + recipe4_items
        db.add_all(all_recipe_items)
        db.commit()

        print(f"{len(all_recipe_items)} vínculos criados!")

        print("\nCriando conversas do bot...")

        bot_conversations = [
            Bot(
                thread_id="thread_001",
                user_message="quais receitas posso fazer com banana?",
                ai_message="você pode fazer torta banoffee, pavê de banana com doce de leite e brigadeiro de banana com doce de leite. todas essas receitas utilizam banana nanica como ingrediente principal.",
                create_at=datetime.now().isoformat()
            ),
            Bot(
                thread_id="thread_001",
                user_message="tenho todos os ingredientes para a torta banoffee?",
                ai_message="sim, você tem todos os ingredientes necessários para fazer a torta banoffee. você precisa de 4 bananas nanicas, 400g de doce de leite, 200g de biscoito maisena, 100g de manteiga, 500ml de creme de leite, 80g de açúcar e 30g de chocolate em pó.",
                create_at=(datetime.now() + timedelta(minutes=2)).isoformat()
            ),
            Bot(
                thread_id="thread_002",
                user_message="quanto de leite tenho no estoque?",
                ai_message="você tem 2000 mililitros de leite integral em estoque.",
                create_at=(datetime.now() - timedelta(days=1)).isoformat()
            ),
            Bot(
                thread_id="thread_002",
                user_message="quando vence o leite?",
                ai_message=f"o leite vence em {(datetime.now().date() + timedelta(days=7)).strftime('%d/%m/%Y')}, daqui a 7 dias.",
                create_at=(datetime.now() - timedelta(days=1) + timedelta(minutes=1)).isoformat()
            ),
            Bot(
                thread_id="thread_003",
                user_message="posso fazer risoto de camarão?",
                ai_message="infelizmente não é possível fazer o risoto de camarão no momento. faltam os seguintes ingredientes: arroz arbóreo (300g), camarão (400g), vinho branco (150ml), caldo de legumes (1000ml) e queijo parmesão (50g). todos estes ingredientes estão indisponíveis no estoque.",
                create_at=(datetime.now() - timedelta(hours=3)).isoformat()
            ),
            Bot(
                thread_id="thread_004",
                user_message="quais ingredientes estão com validade próxima?",
                ai_message="os ingredientes com validade mais próxima são: banana nanica (vence em 5 dias), leite (vence em 7 dias), gema de ovo (vence em 7 dias) e limão (vence em 7 dias). recomendo usar estes ingredientes primeiro.",
                create_at=(datetime.now() - timedelta(hours=6)).isoformat()
            ),
            Bot(
                thread_id="thread_005",
                user_message="me mostre receitas doces",
                ai_message="tenho três receitas doces disponíveis: torta banoffee, pavê de banana com doce de leite e brigadeiro de banana com doce de leite. todas utilizam banana e doce de leite como ingredientes principais.",
                create_at=(datetime.now() - timedelta(days=2)).isoformat()
            ),
        ]

        db.add_all(bot_conversations)
        db.commit()

        print(f"{len(bot_conversations)} conversas do bot criadas!")

        print("\nCriando transações...")

        transactions = [
            Transaction(
                item_id=items[0].id,
                order_type="entrada",
                description="compra inicial de estoque",
                create_at=(datetime.now() - timedelta(days=5)).date(),
                amount=20,
                price=0.50
            ),
            Transaction(
                item_id=items[0].id,
                order_type="saída",
                description="uso em receita: torta banoffee",
                create_at=(datetime.now() - timedelta(days=2)).date(),
                amount=4,
                price=None
            ),
            Transaction(
                item_id=items[0].id,
                order_type="saída",
                description="uso em receita: pavê de banana",
                create_at=(datetime.now() - timedelta(days=1)).date(),
                amount=4,
                price=None
            ),
            Transaction(
                item_id=items[1].id,
                order_type="entrada",
                description="compra inicial de estoque",
                create_at=(datetime.now() - timedelta(days=10)).date(),
                amount=1000,
                price=15.00
            ),
            Transaction(
                item_id=items[1].id,
                order_type="saída",
                description="uso em receita: brigadeiro de banana",
                create_at=(datetime.now() - timedelta(days=1)).date(),
                amount=200,
                price=None
            ),
            Transaction(
                item_id=items[3].id,
                order_type="entrada",
                description="compra inicial de estoque",
                create_at=(datetime.now() - timedelta(days=15)).date(),
                amount=500,
                price=40.00
            ),
            Transaction(
                item_id=items[3].id,
                order_type="saída",
                description="uso em receita: torta banoffee",
                create_at=(datetime.now() - timedelta(days=2)).date(),
                amount=100,
                price=None
            ),
            Transaction(
                item_id=items[3].id,
                order_type="saída",
                description="uso em receita: brigadeiro de banana",
                create_at=(datetime.now() - timedelta(days=1)).date(),
                amount=20,
                price=None
            ),
            Transaction(
                item_id=items[3].id,
                order_type="saída",
                description="venda direta ao cliente",
                create_at=(datetime.now() - timedelta(days=3)).date(),
                amount=180,
                price=40.00
            ),
            Transaction(
                item_id=items[5].id,
                order_type="entrada",
                description="compra inicial de estoque",
                create_at=(datetime.now() - timedelta(days=20)).date(),
                amount=5000,
                price=4.50
            ),
            Transaction(
                item_id=items[5].id,
                order_type="saída",
                description="uso geral na cozinha",
                create_at=(datetime.now() - timedelta(days=10)).date(),
                amount=3000,
                price=None
            ),
            Transaction(
                item_id=items[7].id,
                order_type="entrada",
                description="compra inicial de estoque",
                create_at=(datetime.now() - timedelta(days=3)).date(),
                amount=3000,
                price=5.00
            ),
            Transaction(
                item_id=items[7].id,
                order_type="saída",
                description="uso em receita: pavê de banana",
                create_at=(datetime.now() - timedelta(days=1)).date(),
                amount=480,
                price=None
            ),
            Transaction(
                item_id=items[7].id,
                order_type="saída",
                description="consumo direto",
                create_at=(datetime.now() - timedelta(days=2)).date(),
                amount=520,
                price=None
            ),
            Transaction(
                item_id=items[11].id,
                order_type="entrada",
                description="compra inicial de estoque",
                create_at=(datetime.now() - timedelta(days=30)).date(),
                amount=1000,
                price=40.00
            ),
            Transaction(
                item_id=items[11].id,
                order_type="saída",
                description="uso em receita: brigadeiro de banana",
                create_at=(datetime.now() - timedelta(days=1)).date(),
                amount=100,
                price=None
            ),
            Transaction(
                item_id=items[11].id,
                order_type="saída",
                description="uso em decorações diversas",
                create_at=(datetime.now() - timedelta(days=15)).date(),
                amount=500,
                price=None
            ),
            Transaction(
                item_id=items[6].id,
                order_type="entrada",
                description="compra inicial de estoque",
                create_at=(datetime.now() - timedelta(days=25)).date(),
                amount=1590,
                price=7.00
            ),
            Transaction(
                item_id=items[6].id,
                order_type="saída",
                description="uso em receita: pavê de banana",
                create_at=(datetime.now() - timedelta(days=1)).date(),
                amount=395,
                price=None
            ),
            Transaction(
                item_id=items[6].id,
                order_type="saída",
                description="uso em receita: brigadeiro de banana",
                create_at=(datetime.now() - timedelta(days=1)).date(),
                amount=395,
                price=None
            ),
        ]

        db.add_all(transactions)
        db.commit()

        print(f"{len(transactions)} transações criadas!")

        print("\n" + "=" * 50)
        print("BANCO DE DADOS POPULADO COM SUCESSO!")
        print("=" * 50)
        print(f"\nResumo:")
        print(f"   - {len(items)} itens criados")
        print(f"   - 4 receitas criadas")
        print(f"   - {len(all_recipe_items)} ingredientes vinculados")
        print(f"   - {len(bot_conversations)} conversas do bot criadas")
        print(f"   - {len(transactions)} transações criadas")
        print("\nReceitas disponíveis:")
        print(f"   1. {recipe1.title} (ingredientes disponíveis)")
        print(f"   2. {recipe2.title} (ingredientes disponíveis)")
        print(f"   3. {recipe3.title} (ingredientes disponíveis)")
        print(f"   4. {recipe4.title} (ingredientes INDISPONÍVEIS)")

    except Exception as e:
        print(f"\nErro ao popular banco de dados: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    populate_database()