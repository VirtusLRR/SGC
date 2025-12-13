from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database.database import Base

class ReceitaItem(Base):
    __tablename__ = "Receita_Item"

    receita_id = Column(
        Integer,
        ForeignKey("Receita.id"),
        primary_key=True
    )
    item_id = Column(
        Integer,
        ForeignKey("Item.id"),
        primary_key=True
    )

    quantidade = Column(Numeric, nullable=False)

    receita = relationship("Receita", back_populates="receita_itens")
    item = relationship("Item", back_populates="receita_itens")
