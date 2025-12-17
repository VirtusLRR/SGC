from fastapi import Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from database.database import get_db
from models import Item
from repositories import ItemRepository
from schemas import ItemResponse, ItemRequest

class ItemController:

    @staticmethod
    def create(request: ItemRequest, db: Session = Depends(get_db)):
        default_validators(request)
        item = ItemRepository.save(db, Item(**request.model_dump()))
        return ItemResponse.model_validate(item)

    @staticmethod
    def find_all(db: Session = Depends(get_db)):
        items = ItemRepository.find_all(db)
        return [ItemResponse.model_validate(item) for item in items]

    @staticmethod
    def find_by_id(id: int, db: Session = Depends(get_db)):
        item = ItemRepository.find_by_id(db, id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado"
            )
        return ItemResponse.model_validate(item)

    @staticmethod
    def find_by_name(name: str, db: Session = Depends(get_db)):
        items = ItemRepository.find_by_name(db, name)
        return [ItemResponse.model_validate(item) for item in items]

    @staticmethod
    def delete_by_id(id: int, db: Session = Depends(get_db)):
        if not ItemRepository.exists_by_id(db, id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado"
            )
        ItemRepository.delete_by_id(db, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def update(id: int, request: ItemRequest, db: Session = Depends(get_db)):
        default_validators(request)
        if not ItemRepository.exists_by_id(db, id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item não encontrado"
            )

        item = ItemRepository.save(db, Item(id=id, **request.model_dump()))
        return ItemResponse.model_validate(item)


def default_validators(request: ItemRequest):
    if request.price < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O preço deve ser maior que zero")
    if request.name == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campo obrigatório vazio")
    if request.measure_unity == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campo obrigatório vazio")
    if request.amount < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Consumindo mais produto do que o disponível")


