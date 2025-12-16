from sqlalchemy.orm import Session

from models import Item

class ItemRepository:
    @staticmethod
    def find_all(db: Session) -> list[type[Item]]:
        return db.query(Item).all()

    @staticmethod
    def save(db: Session, item: Item) -> Item:
        if item.id:
            db.merge(item)
        else:
            db.add(item)
        db.commit()
        return item

    @staticmethod
    def find_by_id(db: Session, id: int) -> Item | None:
        return db.query(Item).filter(Item.id == id).first()

    @staticmethod
    def find_by_name(db: Session, name: str) -> list[type[Item]]:
        return db.query(Item).filter(Item.name == name).all()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Item).filter(Item.id == id).first() is not None

    @staticmethod
    def exists_by_name(db: Session, name: str) -> bool:
        return db.query(Item).filter(Item.name == name).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        item = db.query(Item).filter(Item.id == id).first()
        if item is not None:
            db.delete(item)
            db.commit()