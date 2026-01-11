from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from decimal import Decimal

from models import Item
from utils.unit_converter import calculate_item_total_value

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
        return (
            db.query(Item)
            .filter(Item.name.ilike(f"%{name}%"))
            .all()
        )

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

    @staticmethod
    def find_low_stock_items(db: Session, threshold: Decimal = Decimal('10')) -> list[Item]:
        """Retorna itens com estoque abaixo do limite especificado"""
        return db.query(Item).filter(Item.amount < threshold).all()

    @staticmethod
    def find_items_near_expiration(db: Session, days: int = 7) -> list[Item]:
        """Retorna itens que vencem nos próximos N dias"""
        today = datetime.now().date()
        target_date = today + timedelta(days=days)

        return db.query(Item).filter(
            and_(
                Item.expiration_date.isnot(None),
                Item.expiration_date >= today,
                Item.expiration_date <= target_date
            )
        ).order_by(Item.expiration_date).all()

    @staticmethod
    def find_expired_items(db: Session) -> list[Item]:
        """Retorna itens já vencidos"""
        today = datetime.now().date()
        return db.query(Item).filter(
            and_(
                Item.expiration_date.isnot(None),
                Item.expiration_date < today
            )
        ).all()

    @staticmethod
    def find_total_item_value_by_id(id: int, db: Session) -> Decimal:
        """Retorna o valor total do estoque de um item específico, considerando as unidades"""
        item = db.query(Item).filter(Item.id == id).first()
        
        total = calculate_item_total_value(
                item.amount,
                item.price,
                item.measure_unity,
                item.price_unit
            )
        
        return total

    @staticmethod
    def find_total_inventory_value(db: Session) -> Decimal:
        """Retorna o valor total do estoque atual considerando conversão de unidades"""
        items = db.query(Item).all()
        total = Decimal('0')

        for item in items:
            item_value = calculate_item_total_value(
                item.amount,
                item.price,
                item.measure_unity,
                item.price_unit
            )
            total += item_value

        return total

    @staticmethod
    def find_inventory_summary(db: Session) -> dict:
        """Retorna resumo completo do estoque"""
        total_items = db.query(func.count(Item.id)).scalar()
        total_value = ItemRepository.find_total_inventory_value(db)

        items_with_stock = db.query(func.count(Item.id)).filter(
            Item.amount > 0
        ).scalar()

        items_out_of_stock = db.query(func.count(Item.id)).filter(
            Item.amount == 0
        ).scalar()

        return {
            "total_items": total_items,
            "items_with_stock": items_with_stock,
            "items_out_of_stock": items_out_of_stock,
            "total_inventory_value": float(total_value)
        }

    @staticmethod
    def find_items_by_value_ranking(db: Session, limit: int = 10) -> list[dict]:
        """Retorna os N itens com maior valor em estoque considerando conversão de unidades"""
        items = db.query(Item).filter(Item.amount > 0).all()

        items_with_value = []
        for item in items:
            total_value = calculate_item_total_value(
                item.amount,
                item.price,
                item.measure_unity,
                item.price_unit
            )
            items_with_value.append({
                "id": item.id,
                "name": item.name,
                "amount": float(item.amount),
                "price": float(item.price),
                "price_unit": item.price_unit,
                "total_value": float(total_value)
            })

        items_with_value.sort(key=lambda x: x['total_value'], reverse=True)
        return items_with_value[:limit]