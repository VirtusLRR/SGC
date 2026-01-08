from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from database.database import Base
from datetime import datetime

class Bot(Base):
    __tablename__ = "Bot"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    thread_id = Column(String, nullable=False, index=True)
    user_message = Column(String, nullable=False)
    ai_message = Column(String, nullable=False)
    create_at = Column(String, default=str(datetime.now()), nullable=False)