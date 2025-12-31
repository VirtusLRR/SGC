from sqlalchemy.orm import Session

from models import Item

class ItemRepository:
    @staticmethod
    def find_all(db: Session) -> list[type[Item]]:
        """Recupera todos os itens do banco de dados."""
        return db.query(Item).all()

    @staticmethod
    def save(db: Session, item: Item) -> Item:
        """Salva ou atualiza um item no banco de dados."""
        if item.id:
            db.merge(item)
        else:
            db.add(item)
        db.commit()
        return item

    @staticmethod
    def find_by_id(db: Session, id: int) -> Item | None:
        """Recupera um item pelo seu ID."""
        return db.query(Item).filter(Item.id == id).first()

    @staticmethod
    def find_by_name(db: Session, name: str) -> list[type[Item]]:
        """Recupera itens pelo seu nome."""
        return db.query(Item).filter(Item.name == name).all()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        """Verifica se um item existe pelo seu ID."""
        return db.query(Item).filter(Item.id == id).first() is not None

    @staticmethod
    def exists_by_name(db: Session, name: str) -> bool:
        """Verifica se um item existe pelo seu nome."""
        return db.query(Item).filter(Item.name == name).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        """Remove um item pelo seu ID."""
        item = db.query(Item).filter(Item.id == id).first()
        if item is not None:
            db.delete(item)
            db.commit()

