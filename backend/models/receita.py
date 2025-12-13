from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database.database import Base

class Receita(Base):
    __tablename__ = "Receita"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    steps = Column(Text, nullable=False)
    description = Column(Text)

    receita_itens = relationship(
        "ReceitaItem",
        back_populates="receita",
        cascade="all, delete-orphan"
    )
