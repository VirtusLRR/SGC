def test_transaction_schema_validation():
    """Testa se os schemas Transaction funcionam corretamente"""
    from schemas.transaction import TransactionRequest, TransactionResponse
    from datetime import datetime
    
    request_data = {
        "item_id": 1,
        "order_type": "compra",
        "description": "Compra de teste",
        "amount": 100.0,
        "price": 10.50
    }
    
    request = TransactionRequest(**request_data)
    assert request.item_id == 1
    assert request.order_type == "compra"
    assert request.description == "Compra de teste"
    assert request.amount == 100.0
    assert request.price == 10.50
    
    response_data = {
        "id": 1,
        "item_id": 1,
        "order_type": "compra",
        "description": "Compra de teste",
        "amount": 100.0,
        "price": 10.50,
        "create_at": str(datetime.now())
    }
    
    response = TransactionResponse(**response_data)
    assert response.id == 1
    assert response.item_id == 1
    assert response.order_type == "compra"
    
    print("✅ Schemas Transaction validados com sucesso!")

def test_transaction_model_structure():
    """Testa se o modelo Transaction foi criado corretamente"""
    from models.transaction import Transaction
    from sqlalchemy import inspect
    
    assert hasattr(Transaction, '__tablename__')
    assert Transaction.__tablename__ == "Transaction"
    
    mapper = inspect(Transaction)
    column_names = [column.key for column in mapper.columns]
    
    expected_columns = ['id', 'item_id', 'order_type', 'description', 'create_at', 'amount', 'price']
    for col in expected_columns:
        assert col in column_names, f"Coluna {col} não encontrada no modelo Transaction"
    
    print("Modelo Transaction estruturado corretamente!")

def test_transaction_repository_methods():
    """Testa se o repository Transaction tem todos os métodos necessários"""
    from repositories.transaction import TransactionRepository
    
    expected_methods = [
        'find_all',
        'save', 
        'find_by_id',
        'find_by_item_id',
        'exists_by_id',
        'delete_by_id'
    ]
    
    for method in expected_methods:
        assert hasattr(TransactionRepository, method), f"Método {method} não encontrado no repository"
        assert callable(getattr(TransactionRepository, method)), f"Método {method} não é chamável"
    
    print("Repository Transaction com todos os métodos necessários!")

def test_transaction_controller_methods():
    """Testa se o controller Transaction tem todos os métodos necessários"""
    from controllers.transaction import TransactionController
    
    expected_methods = [
        'create',
        'find_all',
        'find_by_id', 
        'find_by_item_id',
        'delete_by_id',
        'update'
    ]
    
    for method in expected_methods:
        assert hasattr(TransactionController, method), f"Método {method} não encontrado no controller"
        assert callable(getattr(TransactionController, method)), f"Método {method} não é chamável"
    
    print("Controller Transaction com todos os métodos necessários!")

if __name__ == "__main__":
    print("🧪 Executando testes simples da entidade Transaction...\n")
    
    try:
        test_transaction_schema_validation()
        test_transaction_model_structure()
        test_transaction_repository_methods()
        test_transaction_controller_methods()
        print("\n✅ Todos os testes passaram! A entidade Transaction foi implementada corretamente.")
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()