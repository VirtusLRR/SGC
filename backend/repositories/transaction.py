from sqlalchemy.orm import Session

from models import Transaction

class TransactionRepository:
    @staticmethod
    def find_all(db: Session) -> list[type[Transaction]]:
        """Recupera todas as transações do banco de dados."""
        return db.query(Transaction).all()

    @staticmethod
    def save(db: Session, transaction: Transaction) -> Transaction:
        """Salva ou atualiza uma transação no banco de dados."""
        if transaction.id:
            db.merge(transaction)
        else:
            db.add(transaction)
        db.commit()
        return transaction

    @staticmethod
    def find_by_id(db: Session, id: int) -> Transaction | None:
        """Recupera uma transação pelo seu ID."""
        return db.query(Transaction).filter(Transaction.id == id).first()

    @staticmethod
    def find_by_item_id(db: Session, item_id: int) -> list[type[Transaction]]:
        """Recupera transações pelo ID do item associado."""
        return db.query(Transaction).filter(Transaction.item_id == item_id).all()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        """Verifica se uma transação existe pelo seu ID."""
        return db.query(Transaction).filter(Transaction.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        """Remove uma transação pelo seu ID."""
        transaction = db.query(Transaction).filter(Transaction.id == id).first()
        if transaction is not None:
            db.delete(transaction)
            db.commit()
