from typing import Optional, Dict, Any, List
from fastapi import Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.database import get_db
from models import Transaction
from repositories import TransactionRepository, ItemRepository
from schemas import TransactionResponse, TransactionRequest
from datetime import datetime
from fastapi import Query

class TransactionController:
    @staticmethod
    def create(request: TransactionRequest, db: Session = Depends(get_db)):
        """Cria uma nova transação após validações padrão."""
        default_validators(request, db)
        transaction = TransactionRepository.save(db, Transaction(**request.model_dump()))
        return TransactionResponse.model_validate(transaction)

    @staticmethod
    def find_all(db: Session = Depends(get_db)):
        """Retorna todas as transações cadastradas."""
        transactions = TransactionRepository.find_all(db)
        return [TransactionResponse.model_validate(transaction) for transaction in transactions]

    @staticmethod
    def find_by_id(id: int, db: Session = Depends(get_db)):
        """Retorna uma transação pelo seu ID."""
        transaction = TransactionRepository.find_by_id(db, id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada"
            )
        return TransactionResponse.model_validate(transaction)

    @staticmethod
    def find_by_item_id(item_id: int, db: Session = Depends(get_db)):
        """Retorna todas as transações associadas a um item específico."""
        transactions = TransactionRepository.find_by_item_id(db, item_id)
        return [TransactionResponse.model_validate(transaction) for transaction in transactions]

    @staticmethod
    def delete_by_id(id: int, db: Session = Depends(get_db)):
        """Remove uma transação pelo seu ID após verificar sua existência."""
        if not TransactionRepository.exists_by_id(db, id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada"
            )
        TransactionRepository.delete_by_id(db, id)
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT, 
            content={"message": "Transação removida com sucesso", "id": id}
        )

    @staticmethod
    def update(id: int, request: TransactionRequest, db: Session = Depends(get_db)):
        """Atualiza uma transação existente após validações padrão."""
        default_validators(request, db)
        if not TransactionRepository.exists_by_id(db, id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada"
            )

        transaction = TransactionRepository.save(db, Transaction(id=id, **request.model_dump()))
        return TransactionResponse.model_validate(transaction)
    
    @staticmethod
    def get_transaction_summary_by_period(
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        db: Session = Depends(get_db)
    ) -> Dict[str, Any]:
        """
        Retorna o resumo financeiro (Entradas vs Saídas) por período.
        Se as datas não forem informadas, o Repository assume os últimos 30 dias.
        """
        try:
            
            summary = TransactionRepository.find_transaction_summary_by_period(
                db, 
                start_date, 
                end_date
            )
            
            return summary
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=str(e)
            )
    
    @staticmethod
    def get_most_transacted_items(
        order_type: Optional[str] = None,
        limit: int = 10,
        db: Session = Depends(get_db)
    ) -> List[Dict[str, Any]]:
        """
        Retorna o ranking de itens com maior número de transações.
        Pode filtrar por tipo ('entrada' ou 'saida') e definir um limite.
        """
        try:
            results = TransactionRepository.find_most_transacted_items(
                db, 
                order_type, 
                limit
            )
            
            return results
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=str(e)
            )
    
    @staticmethod
    def get_daily_transactions(
        days: int = Query(30, gt=0, description="Número de dias para analisar (padrão: 30)"),
        db: Session = Depends(get_db)
    ) -> List[Dict[str, Any]]:
        """
        Retorna o volume de transações agrupado por dia e tipo (entrada/saída).
        Útil para montar gráficos de linha ou barras.
        """
        try:
            return TransactionRepository.find_daily_transactions(db, days)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=str(e)
            )

    @staticmethod
    def get_average_transaction_value_by_item(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
        """
        Retorna estatísticas de preço (média, mínimo, máximo) para cada item
        baseado no histórico de transações.
        """
        try:
            return TransactionRepository.find_average_transaction_value_by_item(db)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=str(e)
            )
    
    @staticmethod
    def get_consumption_rate_by_item(
        days: int = Query(30, gt=0, description="Dias para análise (deve ser maior que 0)"),
        db: Session = Depends(get_db)
    ) -> List[Dict[str, Any]]:
        """
        Retorna a taxa de consumo e previsão de dias até o estoque acabar 
        (Stockout) baseada na média de saídas do período informado.
        """
        try:
            return TransactionRepository.find_consumption_rate_by_item(db, days)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail=str(e)
            )

def default_validators(request: TransactionRequest, db: Session):
    if request.price and request.price < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O preço não pode ser negativo")
    if request.order_type == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campo obrigatório vazio")
    if request.description == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campo obrigatório vazio")
    if request.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A quantidade deve ser maior que zero")
    if not ItemRepository.exists_by_id(db, request.item_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item não encontrado")
