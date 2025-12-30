from sqlalchemy import Column, Integer, String, Float, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = "Transaction"

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("Item.id"), nullable=False)
    order_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    create_at = Column(Date, default=datetime.now(), nullable=False)
    amount = Column(Numeric, nullable=False)
    price = Column(Numeric, nullable=True)

    item = relationship("Item", back_populates="transactions")
