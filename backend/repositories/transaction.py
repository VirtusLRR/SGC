from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import datetime, timedelta
from decimal import Decimal

from models import Transaction, Item
from utils.unit_converter import calculate_item_total_value


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

    @staticmethod
    def find_transaction_summary_by_period(
            db: Session,
            start_date: datetime = None,
            end_date: datetime = None
    ) -> dict:
        """Resumo de entradas e saídas por período com conversão de unidades"""
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()

        transactions = db.query(Transaction).join(
            Item, Transaction.item_id == Item.id
        ).filter(
            and_(
                Transaction.create_at >= start_date.date(),
                Transaction.create_at <= end_date.date()
            )
        ).all()

        total_entries = Decimal('0')
        total_exits = Decimal('0')
        value_entries = Decimal('0')
        value_exits = Decimal('0')
        count_entries = 0
        count_exits = 0

        for trans in transactions:
            item = trans.item

            price_to_use = trans.price if trans.price is not None else item.price

            trans_value = calculate_item_total_value(
                trans.amount,
                price_to_use,
                item.measure_unity,
                item.price_unit
            )

            if trans.order_type.lower() == 'entrada':
                total_entries += trans.amount
                value_entries += trans_value
                count_entries += 1
            elif trans.order_type.lower() == 'saida' or trans.order_type.lower() == 'saída':
                total_exits += trans.amount
                value_exits += trans_value
                count_exits += 1

        return {
            "period": {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            },
            "entries": {
                "count": count_entries,
                "total_amount": float(total_entries),
                "total_value": float(value_entries)
            },
            "exits": {
                "count": count_exits,
                "total_amount": float(total_exits),
                "total_value": float(value_exits)
            },
            "balance": {
                "amount": float(total_entries - total_exits),
                "value": float(value_entries - value_exits)
            }
        }

    @staticmethod
    def find_most_transacted_items(
            db: Session,
            order_type: str = None,
            limit: int = 10
    ) -> list[dict]:
        """Retorna os itens com mais transações com conversão de unidades"""
        query = db.query(Transaction).join(Item, Transaction.item_id == Item.id)

        if order_type:
            query = query.filter(Transaction.order_type == order_type)

        transactions = query.all()

        item_stats = {}

        for trans in transactions:
            item = trans.item

            if item.id not in item_stats:
                item_stats[item.id] = {
                    "item_id": item.id,
                    "item_name": item.name,
                    "transaction_count": 0,
                    "total_amount": Decimal('0'),
                    "total_value": Decimal('0')
                }

            item_stats[item.id]["transaction_count"] += 1
            item_stats[item.id]["total_amount"] += trans.amount

            price_to_use = trans.price if trans.price is not None else item.price

            trans_value = calculate_item_total_value(
                trans.amount,
                price_to_use,
                item.measure_unity,
                item.price_unit
            )
            item_stats[item.id]["total_value"] += trans_value

        results = sorted(
            item_stats.values(),
            key=lambda x: x["transaction_count"],
            reverse=True
        )[:limit]

        return [
            {
                "item_id": r["item_id"],
                "item_name": r["item_name"],
                "transaction_count": r["transaction_count"],
                "total_amount": float(r["total_amount"]),
                "total_value": float(r["total_value"])
            }
            for r in results
        ]

    @staticmethod
    def find_daily_transactions(
            db: Session,
            days: int = 30
    ) -> list[dict]:
        """Retorna contagem de transações por dia"""
        start_date = datetime.now() - timedelta(days=days)

        results = db.query(
            func.date(Transaction.create_at).label('date'),
            Transaction.order_type,
            func.count(Transaction.id).label('count'),
            func.sum(Transaction.amount).label('total_amount')
        ).filter(
            Transaction.create_at >= start_date.date()
        ).group_by(
            func.date(Transaction.create_at),
            Transaction.order_type
        ).order_by(
            func.date(Transaction.create_at)
        ).all()

        return [
            {
                "date": r.date.strftime("%Y-%m-%d"),
                "order_type": r.order_type,
                "count": r.count,
                "total_amount": float(r.total_amount)
            }
            for r in results
        ]

    @staticmethod
    def find_average_transaction_value_by_item(db: Session) -> list[dict]:
        """Retorna valor médio de transação por item considerando conversão de unidades"""
        items_with_transactions = db.query(Item).join(
            Transaction, Item.id == Transaction.item_id
        ).distinct().all()

        results = []

        for item in items_with_transactions:
            transactions = db.query(Transaction).filter(
                Transaction.item_id == item.id
            ).all()

            prices = []
            for trans in transactions:
                price_to_use = trans.price if trans.price is not None else item.price

                trans_value = calculate_item_total_value(
                    trans.amount,
                    price_to_use,
                    item.measure_unity,
                    item.price_unit
                )
                prices.append(trans_value)

            if prices:
                results.append({
                    "item_id": item.id,
                    "item_name": item.name,
                    "avg_price": float(sum(prices) / len(prices)),
                    "min_price": float(min(prices)),
                    "max_price": float(max(prices)),
                    "transaction_count": len(transactions)
                })

        return results

    @staticmethod
    def find_consumption_rate_by_item(
            db: Session,
            days: int = 30
    ) -> list[dict]:
        """Calcula taxa de consumo (saídas) por item nos últimos N dias"""
        start_date = datetime.now() - timedelta(days=days)

        results = db.query(
            Item.id,
            Item.name,
            Item.amount.label('current_stock'),
            func.sum(Transaction.amount).label('total_consumed')
        ).join(
            Transaction, Item.id == Transaction.item_id
        ).filter(
            and_(
                Transaction.order_type.in_(['saida', 'saída']),
                Transaction.create_at >= start_date.date()
            )
        ).group_by(
            Item.id, Item.name, Item.amount
        ).all()

        return [
            {
                "item_id": r.id,
                "item_name": r.name,
                "current_stock": float(r.current_stock),
                "total_consumed": float(r.total_consumed or 0),
                "daily_average": float((r.total_consumed or 0) / days),
                "days_until_stockout": (
                    int(r.current_stock / ((r.total_consumed or 0) / days))
                    if r.total_consumed and r.total_consumed > 0
                    else None
                )
            }
            for r in results
        ]