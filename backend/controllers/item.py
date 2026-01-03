from typing import List, Dict, Any #####
from fastapi import Depends, HTTPException, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.database import get_db
from models import Item
from repositories import ItemRepository
from schemas import ItemResponse, ItemRequest

class ItemController:
    @staticmethod
    def create(request: ItemRequest, db: Session = Depends(get_db)):
        """Cria um novo item após validações padrão."""
        default_validators(request)
        item = ItemRepository.save(db, Item(**request.model_dump()))
        return ItemResponse.model_validate(item)

    @staticmethod
    def find_all(db: Session = Depends(get_db)):
        """Retorna todos os itens cadastrados."""
        items = ItemRepository.find_all(db)
        return [ItemResponse.model_validate(item) for item in items]

    @staticmethod
    def find_by_id(id: int, db: Session = Depends(get_db)):
        """Retorna um item pelo seu ID."""
        item = ItemRepository.find_by_id(db, id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado"
            )
        return ItemResponse.model_validate(item)

    @staticmethod
    def find_by_name(name: str, db: Session = Depends(get_db)):
        """Retorna itens que correspondem ao nome fornecido."""
        items = ItemRepository.find_by_name(db, name)
        return [ItemResponse.model_validate(item) for item in items]

    @staticmethod
    def delete_by_id(id: int, db: Session = Depends(get_db)):
        """Remove um item pelo seu ID após verificar sua existência."""
        if not ItemRepository.exists_by_id(db, id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado"
            )
        ItemRepository.delete_by_id(db, id)
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT, 
            content={"message": "Item removido com sucesso", "id": id}
        )

    @staticmethod
    def update(id: int, request: ItemRequest, db: Session = Depends(get_db)):
        """Atualiza um item existente após validações padrão."""
        default_validators(request)
        if not ItemRepository.exists_by_id(db, id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado"
            )

        item = ItemRepository.save(db, Item(id=id, **request.model_dump()))
        return ItemResponse.model_validate(item)

    @staticmethod
    def get_low_stock_items(threshold: int, db: Session = Depends(get_db)):
        """Retorna itens com estoque abaixo do limite especificado"""
        try:
            items = ItemRepository.find_low_stock_items(db, threshold)
            return [ItemResponse.model_validate(item) for item in items]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    
    @staticmethod
    def get_items_near_expiration(days: int, db: Session = Depends(get_db)):
        """Retorna itens que vencem nos próximos N dias"""
        try:
            items = ItemRepository.find_items_near_expiration(db, days)
            return [ItemResponse.model_validate(item) for item in items]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    @staticmethod
    def get_expired_items(db: Session = Depends(get_db)):
        """Retorna itens já vencidos"""
        try:
            items = ItemRepository.find_expired_items(db)
            return [ItemResponse.model_validate(item) for item in items]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    @staticmethod
    def get_total_inventory_value(db: Session = Depends(get_db)):
        """Retorna o valor total do estoque atual"""
        try:
            total_value = ItemRepository.find_total_inventory_value(db)
            
            return {"total_value": total_value}
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
    
    @staticmethod
    def get_inventory_summary(db: Session = Depends(get_db)) -> Dict[str, Any]:
        """Retorna resumo completo do estoque"""
        try:
            return ItemRepository.find_inventory_summary(db)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    def get_items_by_value_ranking(limit: int = 10, db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
        """Retorna os itens ordenados pelo valor total em estoque (amount * price)"""
        try:
            return ItemRepository.find_items_by_value_ranking(db, limit)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

def default_validators(request: ItemRequest):
    if request.price < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O preço deve ser maior que zero")
    if request.name == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campo obrigatório vazio")
    if request.measure_unity == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campo obrigatório vazio")
    if request.amount < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Consumindo mais produto do que o disponível")


