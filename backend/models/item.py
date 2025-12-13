from sqlalchemy import Column, Integer, String, Text, Numeric
from sqlalchemy.orm import relationship
from app.database.database import Base

class Item(Base):
    __tablename__ = "Item"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    measure_unity = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    description = Column(Text)

    receita_itens = relationship(
        "Receita_Item",
        back_populates="item"
    )
