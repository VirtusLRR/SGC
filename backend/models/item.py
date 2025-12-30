from sqlalchemy import Column, Integer, String, Text, Numeric, Date
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class Item(Base):
    __tablename__ = "Item"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    measure_unity = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    description = Column(Text)
    price = Column(Numeric, default=0)
    expiration_date = Column(Date)
    create_at = Column(Date, default=datetime.now(), nullable=False)
    update_at = Column(Date)

    recipe_itens = relationship(
        "RecipeItem",
        back_populates="item",
        cascade="all, delete-orphan"
    )

    transactions = relationship(
        "Transaction",
        back_populates="item",
        cascade="all, delete-orphan"
    )
